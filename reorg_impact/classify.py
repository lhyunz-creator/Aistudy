# -*- coding: utf-8 -*-
"""4단계. SC 분류기 (02 문서 5장 판정 순서 그대로).

- 판정에는 orgCode / parentCode 와 조직개편 발령 인원 이동만 사용한다
- 조직명은 절대 사용하지 않는다
- 모든 판정은 evidence 값을 함께 반환한다
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

log = logging.getLogger("reorg")

SC_NAMES = {
    "SC-00": "UNCHANGED",
    "SC-01": "MOVED",
    "SC-02": "RECODED",
    "SC-03": "CREATED",
    "SC-04": "ABOLISHED",
    "SC-05": "SPLIT",
    "SC-06": "MERGED_NEW",
    "SC-07": "MERGED_INTO",
    "SC-08": "EXPANDED",
    "SC-09": "UNDETERMINED",
}

# 자동 반영 가능한 조합은 SC-02/CF-H 뿐이다 (02 문서 7장)
AUTO_APPLICABLE = {("SC-02", "CF-H")}
# 룰 수정 없이 대상자만 바뀌는 시나리오
SIMULATION_ONLY = {"SC-01", "SC-08"}
# 사람이 직접 결정해야 하는 시나리오
MANUAL_REVIEW = {"SC-04", "SC-05", "SC-06", "SC-07", "SC-09"}


@dataclass
class OrgChange:
    """조직코드 1건의 판정 결과 + 근거."""
    code_before: str = ""
    code_after: str = ""
    sc: str = "SC-09"
    cf: str = "CF-L"
    member_ratio: float | None = None
    parent_match: bool | None = None
    child_match: bool | None = None
    reason: str = ""
    sources: list = field(default_factory=list)   # 유입 소멸코드
    target: str = ""                              # 수렴 대상 코드


# 조직별 직속 인원수
def _count_members(members: list) -> dict[str, int]:
    counts: dict[str, int] = {}
    for m in members:
        counts[m.orgCode] = counts.get(m.orgCode, 0) + 1
    return counts


# 하위조직 구성 일치 여부 — before 의 직속 하위가 after 로 얼마나 따라갔는가
def _child_match(tree_b, tree_a, code_b: str, code_a: str, min_ratio: float):
    before_children = tree_b.direct_children(code_b)
    if not before_children:
        return None  # 근거 없음
    after_children = tree_a.direct_children(code_a)
    overlap = len(before_children & after_children) / len(before_children)
    return overlap >= min_ratio


# 인원 이동 근거 + 보조 근거로 확신도를 매긴다. 인원 0명이면 CF-L 을 넘지 못한다.
def _confidence(ratio, parent_match, child_match, has_member_basis: bool) -> str:
    if not has_member_basis or ratio is None:
        return "CF-L"
    if parent_match or child_match:
        return "CF-H"
    return "CF-M"


def classify(orgs_before: dict, orgs_after: dict, tree_b, tree_a,
             members_before: list, matrix: dict, cfg) -> dict[str, OrgChange]:
    """조직코드별 SC/CF 판정. 키는 대표 코드(존속·소멸은 before 코드, 신설은 after 코드)."""
    th_member = float(cfg.th("MEMBER_THRESHOLD"))
    th_split = float(cfg.th("SPLIT_MIN_RATIO"))
    th_child = float(cfg.th("CHILD_MATCH_RATIO"))

    before_codes = set(orgs_before)
    after_codes = set(orgs_after)
    survivors = sorted(before_codes & after_codes)
    created = sorted(after_codes - before_codes)
    abolished = sorted(before_codes - after_codes)
    counts_b = _count_members(members_before)

    # 소멸코드 기준 유출 비율 — 분모는 개편 전 직속 인원, 0명이면 추적된 이동건수
    def outflow(code: str) -> tuple[dict[str, float], int]:
        moves = matrix.get(code, {})
        total_moves = sum(moves.values())
        denom = counts_b.get(code, 0) or total_moves
        if denom == 0:
            return {}, 0
        return {t: n / denom for t, n in moves.items()}, denom

    # 신설코드로 유입된 소멸코드 목록
    inflow_sources: dict[str, list[str]] = {}
    for a in abolished:
        for t, n in matrix.get(a, {}).items():
            if n > 0:
                inflow_sources.setdefault(t, []).append(a)
    for t in inflow_sources:
        inflow_sources[t].sort()

    result: dict[str, OrgChange] = {}

    # --- 신설코드 중 통합(SC-06) 먼저 확정. 통합 판정이 코드변경보다 우선한다 ---
    merged_new: dict[str, list[str]] = {
        c: inflow_sources[c] for c in created if len(inflow_sources.get(c, [])) >= 2
    }

    # --- SC-02 짝짓기 (1:1, 이미 짝지어진 신설코드는 후보에서 제외) ---
    pairs: dict[str, str] = {}   # 소멸코드 -> 신설코드
    claimed: set[str] = set()
    for a in abolished:
        ratios, denom = outflow(a)
        if denom == 0 or not ratios:
            continue
        target, ratio = max(sorted(ratios.items()), key=lambda kv: kv[1])
        if ratio < th_member:
            continue
        if target in created and target not in merged_new and target not in claimed:
            if len(inflow_sources.get(target, [])) == 1:
                pairs[a] = target
                claimed.add(target)

    # --- 존속코드 ---
    for s in survivors:
        sources = [a for a in inflow_sources.get(s, []) if a in abolished]
        parent_b, parent_a = orgs_before[s].parentCode, orgs_after[s].parentCode
        parent_match = parent_b == parent_a
        ch = OrgChange(code_before=s, code_after=s, parent_match=parent_match)
        if sources:
            # 1. 타 소멸코드로부터 인원 유입 → SC-08 (유입원은 아래에서 SC-07)
            inflow_n = sum(matrix.get(a, {}).get(s, 0) for a in sources)
            base = counts_b.get(s, 0) or inflow_n
            ch.sc = "SC-08"
            ch.sources = sources
            ch.member_ratio = round(inflow_n / base, 4) if base else None
            ch.child_match = None
            ch.cf = _confidence(ch.member_ratio, parent_match, None, inflow_n > 0)
            ch.reason = f"소멸코드 {', '.join(sources)} 에서 {inflow_n}명 유입 — 기존 룰 범위확대 경고"
        elif not parent_match:
            # 2. parentCode 변경 → SC-01 (룰 수정 대상 아님, 시뮬레이션만)
            ch.sc = "SC-01"
            ch.cf = "CF-H"
            ch.reason = f"상위조직 {parent_b or '(없음)'} → {parent_a or '(없음)'} 변경 — 룰은 그대로, 대상자만 변동"
        else:
            ch.sc = "SC-00"
            ch.cf = "CF-H"
            ch.reason = "코드 존속, 상위조직 동일"
        result[s] = ch

    # --- 신설코드 ---
    for c in created:
        parent_a = orgs_after[c].parentCode
        ch = OrgChange(code_after=c)
        if c in merged_new:
            ch.sc = "SC-06"
            ch.sources = merged_new[c]
            inflow_n = sum(matrix.get(a, {}).get(c, 0) for a in ch.sources)
            ch.member_ratio = None
            ch.cf = "CF-L" if inflow_n == 0 else "CF-M"
            ch.reason = f"소멸코드 {', '.join(ch.sources)} 가 신설코드로 수렴 ({inflow_n}명) — 룰 이관 여부 결정 필요"
        elif c in claimed:
            a = next(k for k, v in pairs.items() if v == c)
            ratios, denom = outflow(a)
            ratio = ratios.get(c, 0.0)
            parent_match = orgs_before[a].parentCode == parent_a
            child_match = _child_match(tree_b, tree_a, a, c, th_child)
            ch = OrgChange(
                code_before=a, code_after=c, sc="SC-02",
                member_ratio=round(ratio, 4), parent_match=parent_match, child_match=child_match,
                target=c, sources=[a],
            )
            ch.cf = _confidence(ch.member_ratio, parent_match, child_match, counts_b.get(a, 0) > 0)
            ch.reason = f"{a} 인원의 {ratio:.0%} 가 {c} 로 이동 — 조직코드 치환 후보"
            result[a] = ch
            continue
        elif inflow_sources.get(c):
            a = inflow_sources[c][0]
            ratios, _ = outflow(a)
            ch.sc = "SC-09"
            ch.member_ratio = round(ratios.get(c, 0.0), 4)
            ch.sources = [a]
            ch.cf = "CF-L"
            ch.reason = f"유입 소멸코드 {a} 의 이동비율 {ratios.get(c, 0.0):.0%} 가 임계치({th_member:.0%}) 미만 — 수동 검토"
        else:
            ch.sc = "SC-03"
            ch.cf = "CF-H"
            ch.reason = "신설 조직, 대응 소멸코드 없음 — 신규 룰은 별도 수립"
        result[c] = ch

    # --- 소멸코드 ---
    for a in abolished:
        if a in result:      # SC-02 짝으로 이미 확정
            continue
        ratios, denom = outflow(a)
        parent_b = orgs_before[a].parentCode
        ch = OrgChange(code_before=a, sources=[])
        member_n = counts_b.get(a, 0)
        if member_n == 0 and not ratios:
            # 1. 인원 0명 → 근거 없음. 룰이 걸려 있을 수 있으므로 반드시 수동 검토
            ch.sc = "SC-09"
            ch.cf = "CF-L"
            ch.reason = "개편 전 인원 0명 — 인원 근거로 유입처를 추적할 수 없음"
            result[a] = ch
            continue

        target, ratio = (max(sorted(ratios.items()), key=lambda kv: kv[1]) if ratios else ("", 0.0))
        merged_target = next((c for c, srcs in merged_new.items() if a in srcs), "")
        if merged_target:
            # 통합(SC-06) 의 유입원 — 코드변경보다 통합 판정이 우선
            ch.sc = "SC-06"
            ch.code_after = merged_target
            ch.target = merged_target
            ch.member_ratio = round(ratios.get(merged_target, 0.0), 4)
            ch.parent_match = parent_b == orgs_after[merged_target].parentCode
            ch.child_match = _child_match(tree_b, tree_a, a, merged_target, th_child)
            ch.cf = "CF-M" if member_n else "CF-L"
            ch.reason = f"{a} 인원이 신설코드 {merged_target} 로 수렴 (통합) — 룰 이관 여부 결정 필요"
        elif ratio >= th_member and target:
            if target in survivors:
                # 2. 존속코드로 수렴 → SC-07 (대상 존속코드는 SC-08 로 이미 기록됨)
                parent_match = parent_b == orgs_after[target].parentCode
                child_match = _child_match(tree_b, tree_a, a, target, th_child)
                ch.sc = "SC-07"
                ch.code_after = target
                ch.target = target
                ch.member_ratio = round(ratio, 4)
                ch.parent_match = parent_match
                ch.child_match = child_match
                ch.cf = _confidence(ch.member_ratio, parent_match, child_match, member_n > 0)
                ch.reason = f"{a} 인원의 {ratio:.0%} 가 존속코드 {target} 로 흡수 — 룰 이관 여부 결정 필요"
            else:
                # 신설코드지만 짝짓기에 실패한 경우 (이미 다른 소멸코드에 배정됨 등)
                ch.sc = "SC-09"
                ch.member_ratio = round(ratio, 4)
                ch.target = target
                ch.cf = "CF-L"
                ch.reason = f"{a} 인원이 {target} 로 수렴하나 짝짓기 제약으로 확정 불가 — 수동 검토"
        else:
            branches = sorted([t for t, r in ratios.items() if r >= th_split])
            if len(branches) >= 2:
                # 3. 유의미하게 분산 → SC-05
                ch.sc = "SC-05"
                ch.member_ratio = round(ratio, 4)
                ch.sources = branches
                ch.cf = "CF-M" if member_n else "CF-L"
                ch.reason = f"{a} 인원이 {', '.join(branches)} 로 분산 — 룰 복제 여부 결정 필요"
            else:
                # 4. 유입처 식별 불가 / 흩어짐 → SC-04
                ch.sc = "SC-04"
                ch.member_ratio = round(ratio, 4) if ratios else None
                ch.cf = "CF-M" if member_n and ratios else "CF-L"
                ch.reason = "소멸 후 유입처를 식별할 수 없음 — 룰 삭제 또는 비활성 검토"
        result[a] = ch

    log.info(
        "SC 분류: 존속 %d · 신설 %d · 소멸 %d → 판정 %d건",
        len(survivors), len(created), len(abolished), len(result),
    )
    return result
