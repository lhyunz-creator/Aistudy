# -*- coding: utf-8 -*-
"""5·6단계. 고아 룰 검출 + 룰 영향도 분석.

고아 룰 검출은 다른 단계와 무관하게 단독으로 동작한다. 최종 안전망이다.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

log = logging.getLogger("reorg")


@dataclass
class OrphanRule:
    ruleId: str
    permissionId: str
    ruleType: str
    orgCode: str
    code: str = "OR-01"   # OR-01 | OR-02
    reason: str = ""


@dataclass
class RuleAction:
    ruleId: str
    permissionId: str
    ruleType: str
    orgCode_current: str
    orgCode_proposed: str = ""
    scenarioCode: str = ""
    confidenceCode: str = ""
    actionType: str = "NONE"        # NONE|REPLACE_CODE|REVIEW_TRANSFER|REVIEW_DELETE|REVIEW_DUPLICATE|MANUAL
    requiresApproval: str = "N"
    reason: str = ""


@dataclass
class ConflictItem:
    orgCode: str
    permissionId: str
    autoRules: list = field(default_factory=list)
    blockRules: list = field(default_factory=list)


@dataclass
class DuplicateItem:
    orgCode: str
    permissionId: str
    ruleType: str
    jobCodes: str
    ruleIds: list = field(default_factory=list)


# 5단계. 전체 룰을 스캔해 개편 후 조직에 없는 코드를 참조하는 룰을 뽑는다. 단독 동작.
def detect_orphans(rules: list, orgs_after: dict) -> list[OrphanRule]:
    out: list[OrphanRule] = []
    for rule in rules:
        for code, _inc in rule.deptConditions:
            if code not in orgs_after:
                out.append(
                    OrphanRule(
                        rule.ruleId, rule.permissionId, rule.ruleType, code,
                        "OR-01", "개편 후 조직 목록에 없는 조직코드를 참조",
                    )
                )
                log.warning("고아 룰 OR-01: 룰 %s 가 없는 조직코드 %s 참조", rule.ruleId, code)
    return out


# 조직코드별로 걸려 있는 룰 목록
def rules_by_org(rules: list) -> dict[str, list]:
    idx: dict[str, list] = {}
    for rule in rules:
        for code, _inc in rule.deptConditions:
            idx.setdefault(code, []).append(rule)
    return idx


# 6단계. 룰별 조치 제안. 조직 판정(SC/CF)을 룰 단위로 전개한다.
def build_rule_actions(rules: list, changes: dict, orgs_after: dict,
                       duplicates: list) -> list[RuleAction]:
    dup_rule_ids = {rid for d in duplicates for rid in d.ruleIds}
    actions: list[RuleAction] = []
    for rule in rules:
        for code, _inc in rule.deptConditions:
            ch = changes.get(code)
            act = RuleAction(rule.ruleId, rule.permissionId, rule.ruleType, code)
            if ch is None:
                act.scenarioCode, act.confidenceCode = "SC-09", "CF-L"
                act.actionType, act.requiresApproval = "MANUAL", "Y"
                act.reason = "조직코드가 개편 전/후 어느 목록에도 없음 — 수동 확인 필요"
                actions.append(act)
                continue
            act.scenarioCode, act.confidenceCode = ch.sc, ch.cf
            act.reason = ch.reason
            if ch.sc == "SC-02":
                act.orgCode_proposed = ch.code_after
                act.actionType = "REPLACE_CODE"
                act.requiresApproval = "N" if ch.cf == "CF-H" else "Y"
            elif ch.sc in ("SC-06", "SC-07"):
                act.orgCode_proposed = ch.target or ch.code_after
                act.actionType = "REVIEW_TRANSFER"
                act.requiresApproval = "Y"
            elif ch.sc == "SC-05":
                act.actionType = "REVIEW_TRANSFER"
                act.requiresApproval = "Y"
                act.reason = ch.reason + " (룰 복제 여부 포함)"
            elif ch.sc == "SC-04":
                act.actionType = "REVIEW_DELETE"
                act.requiresApproval = "Y"
            elif ch.sc == "SC-09":
                act.actionType = "MANUAL"
                act.requiresApproval = "Y"
            else:
                # SC-00 / SC-01 / SC-03 / SC-08 — 룰 수정 대상 아님
                act.actionType = "NONE"
                act.requiresApproval = "N"
                if rule.ruleId in dup_rule_ids:
                    act.actionType = "REVIEW_DUPLICATE"
                    act.requiresApproval = "Y"
                    act.reason = (ch.reason + " / 동일 권한·종류·직무 룰 중복 — 병합 후보").strip(" /")
            actions.append(act)
    actions.sort(key=lambda a: (a.ruleId, a.orgCode_current))
    return actions


# OR-02 — 고아인데 조치 제안이 없는(짝짓기 실패) 룰
def mark_unresolved_orphans(orphans: list, actions: list) -> list[OrphanRule]:
    resolved = {
        (a.ruleId, a.orgCode_current)
        for a in actions
        if a.actionType in ("REPLACE_CODE", "REVIEW_TRANSFER")
    }
    for o in orphans:
        if (o.ruleId, o.orgCode) not in resolved:
            o.code = "OR-02"
            o.reason = "짝짓기 실패로 조치 제안 없음 — 방치 시 룰이 아무에게도 걸리지 않음"
            log.warning("고아 룰 OR-02: 룰 %s (%s) 조치 미정", o.ruleId, o.orgCode)
    return orphans


# 통합 대상 조직 단위로 묶이는 룰 집합 { 대상코드: [rule...] }
def _merged_groups(changes: dict, idx: dict) -> dict[str, list]:
    groups: dict[str, list] = {}
    for code, ch in changes.items():
        if ch.sc in ("SC-06", "SC-07") and (ch.target or ch.code_after):
            target = ch.target or ch.code_after
            groups.setdefault(target, [])
            groups[target].extend(idx.get(code, []))
    for target in list(groups):
        groups[target] = list(idx.get(target, [])) + groups[target]
        # 결정론적 순서 + 중복 제거
        seen, uniq = set(), []
        for r in groups[target]:
            if r.ruleId not in seen:
                seen.add(r.ruleId)
                uniq.append(r)
        groups[target] = sorted(uniq, key=lambda r: r.ruleId)
    return groups


# 충돌 룰 — 동일 권한에 AUTO 와 BLOCK 이 함께 딸려오는 경우 (판단하지 않고 검토 대상으로만 제시)
def detect_conflicts(changes: dict, rules: list) -> list[ConflictItem]:
    idx = rules_by_org(rules)
    out: list[ConflictItem] = []
    for target, group in sorted(_merged_groups(changes, idx).items()):
        by_perm: dict[str, dict[str, list]] = {}
        for r in group:
            by_perm.setdefault(r.permissionId, {"AUTO": [], "BLOCK": []})[r.ruleType].append(r.ruleId)
        for perm, kinds in sorted(by_perm.items()):
            if kinds["AUTO"] and kinds["BLOCK"]:
                out.append(ConflictItem(target, perm, kinds["AUTO"], kinds["BLOCK"]))
                log.info("충돌 룰: %s 권한 %s — AUTO %s / BLOCK %s", target, perm, kinds["AUTO"], kinds["BLOCK"])
    return out


# 중복 룰 — 동일 권한 + 동일 종류 + 동일 직무 조합
def detect_duplicates(changes: dict, rules: list) -> list[DuplicateItem]:
    idx = rules_by_org(rules)
    out: list[DuplicateItem] = []
    for target, group in sorted(_merged_groups(changes, idx).items()):
        buckets: dict[tuple, list] = {}
        for r in group:
            key = (r.permissionId, r.ruleType, ",".join(sorted(r.jobCodes)))
            buckets.setdefault(key, []).append(r.ruleId)
        for (perm, rtype, jobs), ids in sorted(buckets.items()):
            if len(ids) >= 2:
                out.append(DuplicateItem(target, perm, rtype, jobs or "(전체)", sorted(ids)))
                log.info("중복 룰: %s 권한 %s %s — %s", target, perm, rtype, ids)
    return out
