# -*- coding: utf-8 -*-
"""가벼운 회귀 테스트.

  python3 -m unittest discover -s reorg_impact/tests
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from reorg_impact.classify import classify
from reorg_impact.config import Config
from reorg_impact.gen_samples import generate
from reorg_impact.loader import InputError, Rule, load_all, read_text_utf8
from reorg_impact.moves import build_move_matrix, filter_reorg_assignments
from reorg_impact.rules_impact import (build_rule_actions, detect_conflicts,
                                       detect_duplicates, detect_orphans,
                                       mark_unresolved_orphans)
from reorg_impact.simulate import rule_targets, simulate
from reorg_impact.tree import OrgTree


def build_context():
    tmp = Path(tempfile.mkdtemp())
    generate(tmp)
    cfg = Config({"reorg": {"REORG_DATE": "2026-04-01",
                            "REASON_CODE_REORG": "ORG",
                            "REASON_CODE_TRANSFER": "TRF"}})
    data = load_all(tmp, cfg)
    tree_b, tree_a = OrgTree(data.orgs_before, "b"), OrgTree(data.orgs_after, "a")
    matrix = build_move_matrix(filter_reorg_assignments(data.assignments, cfg))
    changes = classify(data.orgs_before, data.orgs_after, tree_b, tree_a,
                       data.members_before, matrix, cfg)
    return tmp, cfg, data, tree_b, tree_a, matrix, changes


class TestPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (cls.tmp, cls.cfg, cls.data, cls.tree_b, cls.tree_a,
         cls.matrix, cls.changes) = build_context()

    def test_scenario_codes(self):
        expected = {
            "A002": "SC-00", "B002": "SC-01", "B003": "SC-02", "C007": "SC-03",
            "B005": "SC-04", "B004": "SC-05", "B006": "SC-06", "B007": "SC-06",
            "B001": "SC-07", "A001": "SC-08", "B008": "SC-09",
        }
        for code, sc in expected.items():
            self.assertEqual(self.changes[code].sc, sc, f"{code} 판정이 {sc} 가 아님")

    def test_confidence(self):
        self.assertEqual(self.changes["B003"].cf, "CF-H")   # 인원 100% + 상위조직 일치
        self.assertEqual(self.changes["B001"].cf, "CF-M")   # 인원 근거만
        self.assertEqual(self.changes["B008"].cf, "CF-L")   # 인원 0명 → CF-L 초과 불가

    def test_transfer_excluded(self):
        # 전배(TRF)로 A002 로 간 인원이 이동 매트릭스에 섞이면 안 된다
        self.assertNotIn("A002", self.matrix.get("B003", {}))
        self.assertNotIn("A002", self.matrix.get("B004", {}))
        # 기준일 ±3일 밖 발령도 제외
        self.assertNotIn("B005", self.matrix)

    def test_orphans_standalone(self):
        orphans = detect_orphans(self.data.rules, self.data.orgs_after)
        codes = {(o.ruleId, o.orgCode) for o in orphans}
        self.assertIn(("R-002", "B001"), codes)
        self.assertIn(("R-008", "B008"), codes)
        self.assertNotIn(("R-001", "A001"), codes)

    def test_or02_marks_unresolved(self):
        dups = detect_duplicates(self.changes, self.data.rules)
        actions = build_rule_actions(self.data.rules, self.changes, self.data.orgs_after, dups)
        orphans = mark_unresolved_orphans(detect_orphans(self.data.rules, self.data.orgs_after), actions)
        by_rule = {o.ruleId: o.code for o in orphans}
        self.assertEqual(by_rule["R-002"], "OR-01")  # 이관 제안 있음
        self.assertEqual(by_rule["R-008"], "OR-02")  # 조치 없이 방치

    def test_actions(self):
        dups = detect_duplicates(self.changes, self.data.rules)
        actions = {(a.ruleId, a.orgCode_current): a
                   for a in build_rule_actions(self.data.rules, self.changes, self.data.orgs_after, dups)}
        a = actions[("R-006", "B003")]
        self.assertEqual((a.actionType, a.orgCode_proposed, a.requiresApproval), ("REPLACE_CODE", "C003", "N"))
        self.assertEqual(actions[("R-007", "B005")].actionType, "REVIEW_DELETE")
        self.assertEqual(actions[("R-008", "B008")].actionType, "MANUAL")
        self.assertEqual(actions[("R-004", "A001")].actionType, "NONE")  # SC-08 은 룰 수정 대상 아님

    def test_conflict_and_duplicate(self):
        conflicts = {(c.orgCode, c.permissionId) for c in detect_conflicts(self.changes, self.data.rules)}
        self.assertIn(("A001", "PERM_Y"), conflicts)   # AUTO 와 BLOCK 공존
        dups = {(d.orgCode, d.permissionId, tuple(d.ruleIds))
                for d in detect_duplicates(self.changes, self.data.rules)}
        self.assertIn(("A001", "PERM_X", ("R-001", "R-002")), dups)

    def test_simulation(self):
        impacts = {i.ruleId: i for i in simulate(self.data.rules, self.tree_b, self.tree_a,
                                                 self.data.members_before, self.data.members_after)}
        self.assertEqual(len(impacts["R-001"].added), 4)     # B001 인원 유입
        self.assertEqual(len(impacts["R-002"].removed), 4)   # 고아 룰은 대상자 0명
        self.assertEqual(impacts["R-002"].after_count, 0)
        self.assertIn("u401", impacts["R-005"].removed)      # SC-01 로 하위포함 룰에서 이탈

    def test_multi_dept_rule_grouped(self):
        r011 = next(r for r in self.data.rules if r.ruleId == "R-011")
        self.assertEqual(sorted(c[0] for c in r011.deptConditions), ["A002", "B004"])


class TestTreeAndMatching(unittest.TestCase):
    def test_cycle_does_not_hang(self):
        tmp, cfg, data, tree_b, _, _, _ = build_context()
        self.assertNotIn("X001", tree_b.descendants("X001"))  # 순환 경로는 스킵된다

    def test_match_rules(self):
        from reorg_impact.loader import Member
        orgs = {"P": type("O", (), {"orgCode": "P", "orgName": "", "parentCode": ""})(),
                "C": type("O", (), {"orgCode": "C", "orgName": "", "parentCode": "P"})()}
        tree = OrgTree(orgs, "t")
        members = [Member("u1", "P", "DEV"), Member("u2", "C", "DEV"), Member("u3", "C", "HR")]
        idx = {"P": [members[0]], "C": members[1:]}
        # 하위 미포함 → 직속만
        self.assertEqual(rule_targets(Rule("r", "p", "AUTO", [("P", False)], []), tree, idx), {"u1"})
        # 하위 포함 → 말단까지
        self.assertEqual(rule_targets(Rule("r", "p", "AUTO", [("P", True)], []), tree, idx), {"u1", "u2", "u3"})
        # 직무 조건 AND
        self.assertEqual(rule_targets(Rule("r", "p", "AUTO", [("P", True)], ["HR"]), tree, idx), {"u3"})
        # 부서조건끼리 OR
        self.assertEqual(rule_targets(Rule("r", "p", "AUTO", [("P", False), ("C", False)], []), tree, idx),
                         {"u1", "u2", "u3"})


class TestEncoding(unittest.TestCase):
    def test_non_utf8_aborts_with_guidance(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "orgs_before.csv"
            p.write_bytes("orgCode,orgName,parentCode\nA001,인사팀,\n".encode("cp949"))
            with self.assertRaises(InputError) as ctx:
                read_text_utf8(p)
            msg = str(ctx.exception)
            self.assertIn("UTF-8이 아닙니다", msg)
            self.assertIn("CP949", msg)
            self.assertIn("다시 저장", msg)   # 해결 방법을 함께 안내

    def test_bom_is_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.csv"
            p.write_text("orgCode\nA001\n", encoding="utf-8-sig")
            self.assertTrue(read_text_utf8(p).startswith("orgCode"))


if __name__ == "__main__":
    unittest.main()
