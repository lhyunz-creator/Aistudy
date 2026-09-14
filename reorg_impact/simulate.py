# -*- coding: utf-8 -*-
"""7단계. 대상자 시뮬레이션.

기존 운영 판정 로직(01 문서 4장)을 그대로 재현한다. 변경 금지.
  includeSubDept=false → 직속 인원만
  includeSubDept=true  → 해당 조직 + 말단까지 전체 하위
  부서조건끼리 OR, 부서조건 ↔ 직무조건 AND, jobCodes 비어 있으면 직무 미검사
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

log = logging.getLogger("reorg")


@dataclass
class RuleImpact:
    ruleId: str
    permissionId: str
    ruleType: str
    before_count: int = 0
    after_count: int = 0
    added: list = field(default_factory=list)
    removed: list = field(default_factory=list)


# 조직코드 → 직속 인원 색인
def index_members(members: list) -> dict[str, list]:
    idx: dict[str, list] = {}
    for m in members:
        idx.setdefault(m.orgCode, []).append(m)
    return idx


# 룰 1건의 대상자 사번 집합
def rule_targets(rule, tree, member_idx: dict) -> set[str]:
    orgs: set[str] = set()
    for code, include_sub in rule.deptConditions:
        if code not in tree.orgs:
            continue  # 고아 조건 — 아무도 걸리지 않는다 (고아 룰 검출기가 별도로 잡는다)
        orgs |= tree.subtree(code) if include_sub else {code}
    jobs = set(rule.jobCodes)
    out: set[str] = set()
    for code in orgs:
        for m in member_idx.get(code, []):
            if jobs and m.jobCode not in jobs:
                continue
            out.add(m.userId)
    return out


# 룰별 개편 전/후 대상자를 산출하고 차집합을 낸다.
def simulate(rules: list, tree_b, tree_a, members_before: list, members_after: list) -> list[RuleImpact]:
    idx_b, idx_a = index_members(members_before), index_members(members_after)
    out: list[RuleImpact] = []
    for rule in rules:
        before = rule_targets(rule, tree_b, idx_b)
        after = rule_targets(rule, tree_a, idx_a)
        impact = RuleImpact(
            rule.ruleId, rule.permissionId, rule.ruleType,
            len(before), len(after), sorted(after - before), sorted(before - after),
        )
        out.append(impact)
        if impact.added or impact.removed:
            log.info(
                "룰 %s (%s %s): 신규 %d명 / 이탈 %d명",
                rule.ruleId, rule.permissionId, rule.ruleType, len(impact.added), len(impact.removed),
            )
    out.sort(key=lambda i: i.ruleId)
    return out
