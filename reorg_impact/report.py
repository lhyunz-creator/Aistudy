# -*- coding: utf-8 -*-
"""8단계. 리포트 생성.

출력 CSV 는 UTF-8 with BOM (Excel 한글 깨짐 방지), md/로그는 BOM 없는 UTF-8.
"""
from __future__ import annotations

import csv
import logging
from pathlib import Path

from .classify import AUTO_APPLICABLE, MANUAL_REVIEW, SC_NAMES, SIMULATION_ONLY

log = logging.getLogger("reorg")


# UTF-8 with BOM 으로 CSV 를 쓴다.
def write_csv(path: Path, header: list[str], rows: list[list]):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    log.info("출력: %s (%d행)", path.name, len(rows))


def _b(v):
    return "" if v is None else ("Y" if v else "N")


def _r(v):
    return "" if v is None else f"{v:.4f}"


# org_changes.csv
def write_org_changes(path: Path, changes: dict, orgs_before: dict, orgs_after: dict, rule_idx: dict):
    header = [
        "orgCode_before", "orgCode_after", "orgName_before", "orgName_after",
        "parentCode_before", "parentCode_after", "scenarioCode", "scenarioName",
        "confidenceCode", "evidence_member_ratio", "evidence_parent_match",
        "evidence_child_match", "affected_rule_count", "reason",
    ]
    rows = []
    for key in sorted(changes):
        ch = changes[key]
        ob = orgs_before.get(ch.code_before)
        oa = orgs_after.get(ch.code_after)
        n_rules = len({r.ruleId for c in (ch.code_before, ch.code_after) if c for r in rule_idx.get(c, [])})
        rows.append([
            ch.code_before, ch.code_after,
            ob.orgName if ob else "", oa.orgName if oa else "",
            ob.parentCode if ob else "", oa.parentCode if oa else "",
            ch.sc, SC_NAMES.get(ch.sc, ""), ch.cf,
            _r(ch.member_ratio), _b(ch.parent_match), _b(ch.child_match),
            n_rules, ch.reason,
        ])
    write_csv(path, header, rows)


# rule_actions.csv
def write_rule_actions(path: Path, actions: list):
    header = [
        "ruleId", "permissionId", "ruleType", "orgCode_current", "orgCode_proposed",
        "scenarioCode", "confidenceCode", "actionType", "requiresApproval", "reason", "decision",
    ]
    rows = [
        [a.ruleId, a.permissionId, a.ruleType, a.orgCode_current, a.orgCode_proposed,
         a.scenarioCode, a.confidenceCode, a.actionType, a.requiresApproval, a.reason, ""]
        for a in actions
    ]
    write_csv(path, header, rows)


# member_impact.csv
def write_member_impact(path: Path, impacts: list):
    header = ["ruleId", "permissionId", "ruleType", "before_count", "after_count",
              "added_count", "removed_count", "added_userIds", "removed_userIds"]
    rows = [
        [i.ruleId, i.permissionId, i.ruleType, i.before_count, i.after_count,
         len(i.added), len(i.removed), ";".join(i.added), ";".join(i.removed)]
        for i in impacts
    ]
    write_csv(path, header, rows)


# orphan_rules.csv — 고아 룰 단독 리포트 (최종 안전망)
def write_orphans(path: Path, orphans: list):
    header = ["orphanCode", "ruleId", "permissionId", "ruleType", "orgCode", "reason"]
    rows = [[o.code, o.ruleId, o.permissionId, o.ruleType, o.orgCode, o.reason] for o in orphans]
    write_csv(path, header, rows)


# summary.md — 사람이 읽는 요약. 고아 룰 건수를 최상단에 둔다.
def write_summary(path: Path, ctx: dict):
    changes = ctx["changes"]
    actions = ctx["actions"]
    orphans = ctx["orphans"]
    impacts = {i.ruleId: i for i in ctx["impacts"]}
    conflicts = ctx["conflicts"]
    duplicates = ctx["duplicates"]

    auto_ok = [a for a in actions if (a.scenarioCode, a.confidenceCode) in AUTO_APPLICABLE and a.requiresApproval == "N"]
    need_approval = [a for a in actions if a.requiresApproval == "Y" and a.actionType != "MANUAL"]
    manual = [a for a in actions if a.actionType == "MANUAL"]
    sim_only = [c for c in changes.values() if c.sc in SIMULATION_ONLY]

    L = []
    L.append("# 조직개편 권한 룰 영향도 요약")
    L.append("")
    L.append(f"- 개편 기준일: {ctx['reorg_date']}")
    L.append(f"- 분석 대상 룰: {ctx['rule_count']}건 / 조직 판정: {len(changes)}건")
    L.append("")
    L.append("```")
    L.append(f"■ 고아 룰                  {len(orphans):>4}건   ← 최우선 확인")
    L.append(f"■ 자동 반영 가능            {len(auto_ok):>4}건")
    L.append(f"■ 승인 필요                {len(need_approval):>4}건")
    L.append(f"■ 수동 검토 필수            {len(manual):>4}건")
    L.append(f"■ 룰 수정 없이 대상자만 변동  {len(sim_only):>4}건")
    L.append("```")
    L.append("")

    L.append("## 1. 고아 룰 (OR)")
    if not orphans:
        L.append("")
        L.append("고장난 룰 없음.")
    else:
        L.append("")
        L.append("개편 후 사라진 조직코드를 가리키는 룰이다. 아무도 대상에 걸리지 않아 자동 부여도 신청 차단도 동작하지 않는다.")
        L.append("")
        L.append("| 코드 | 룰 | 권한 | 종류 | 조직코드 | 사유 |")
        L.append("|---|---|---|---|---|---|")
        for o in orphans:
            L.append(f"| {o.code} | {o.ruleId} | {o.permissionId} | {o.ruleType} | {o.orgCode} | {o.reason} |")
    L.append("")

    L.append("## 2. 조직 변경 건별 상세")
    L.append("")
    order = {"SC-06": 0, "SC-07": 1, "SC-05": 2, "SC-04": 3, "SC-09": 4, "SC-02": 5, "SC-08": 6, "SC-01": 7}
    targets = [c for c in changes.values() if c.sc in order]
    targets.sort(key=lambda c: (order[c.sc], c.code_before or c.code_after))
    if not targets:
        L.append("검토가 필요한 변경 건이 없다.")
    for ch in targets:
        key = ch.code_before or ch.code_after
        arrow = f"{ch.code_before} → {ch.code_after}" if ch.code_before and ch.code_after and ch.code_before != ch.code_after else key
        names = ctx["org_label"](ch)
        L.append("")
        L.append(f"### [{ch.sc}] [{ch.cf}] {arrow}  {names}")
        L.append("")
        L.append(f"- 근거: {ch.reason}")
        ev = []
        if ch.member_ratio is not None:
            label = "유입비율(기존 인원 대비)" if ch.sc == "SC-08" else "인원이동비율"
            ev.append(f"{label} {ch.member_ratio:.0%}")
        if ch.parent_match is not None:
            ev.append(f"상위조직일치 {'○' if ch.parent_match else '✕'}")
        if ch.child_match is not None:
            ev.append(f"하위구성일치 {'○' if ch.child_match else '✕'}")
        if ev:
            L.append(f"- evidence: {' · '.join(ev)}")

        # 소멸 예정 코드에 걸린 룰 / 존속 코드에 걸린 룰을 나눠서 본다
        dying_actions = [a for a in actions if ch.code_before and a.orgCode_current == ch.code_before
                         and ch.code_before != ch.code_after]
        standing_actions = [a for a in actions if a.orgCode_current == (ch.code_after or ch.code_before)]
        if ch.sc in MANUAL_REVIEW or ch.sc == "SC-02":
            lines = [a for a in dying_actions if a.actionType != "NONE"]
            if lines:
                L.append(f"- 대상 조직이 사라진 룰 {len(lines)}건")
                for a in lines:
                    proposed = f" → {a.orgCode_proposed}" if a.orgCode_proposed else ""
                    L.append(f"    - {a.ruleId}  {a.permissionId} {a.ruleType}{proposed}  [{a.actionType}]")
            moving_in = [a for a in standing_actions if a.actionType == "REVIEW_DUPLICATE"]
            if moving_in:
                L.append(f"- 이관 시 중복이 되는 기존 룰 {len(moving_in)}건")
                for a in moving_in:
                    L.append(f"    - {a.ruleId}  {a.permissionId} {a.ruleType}  [{a.actionType}]")
        if ch.sc in SIMULATION_ONLY:
            rows = []
            for a in standing_actions:
                im = impacts.get(a.ruleId)
                if im and (im.added or im.removed):
                    rows.append(f"    - {a.ruleId}  {a.permissionId} {a.ruleType}  신규 {len(im.added)}명 / 이탈 {len(im.removed)}명")
            if rows:
                L.append(f"- 대상자가 바뀌는 기존 룰 {len(rows)}건")
                L.extend(rows)
        conf = [c for c in conflicts if c.orgCode in (ch.code_before, ch.code_after)]
        for c in conf:
            L.append(f"- 충돌 감지: {c.permissionId} 권한에 AUTO({', '.join(c.autoRules)}) 와 BLOCK({', '.join(c.blockRules)}) 공존 — 검토 필요")
        dup = [d for d in duplicates if d.orgCode in (ch.code_before, ch.code_after)]
        for d in dup:
            L.append(f"- 중복 룰: {d.permissionId} {d.ruleType} 직무 {d.jobCodes} — {', '.join(d.ruleIds)} 병합 후보")
    L.append("")
    L.append("## 3. 대상자 변동이 있는 룰 전체")
    L.append("")
    moved = [i for i in ctx["impacts"] if i.added or i.removed]
    if not moved:
        L.append("대상자 변동 없음.")
    else:
        L.append("| 룰 | 권한 | 종류 | 개편전 | 개편후 | 신규 | 이탈 |")
        L.append("|---|---|---|---|---|---|---|")
        for i in moved:
            L.append(f"| {i.ruleId} | {i.permissionId} | {i.ruleType} | {i.before_count} | {i.after_count} | +{len(i.added)} | -{len(i.removed)} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("이 도구는 룰을 직접 수정하지 않는다. 위 내용은 변경 제안이며, 반영은 IAM 포털에서 별도로 수행한다.")
    L.append("")
    path.write_text("\n".join(L), encoding="utf-8")
    log.info("출력: %s", path.name)
