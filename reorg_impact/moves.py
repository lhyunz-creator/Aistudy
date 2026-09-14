# -*- coding: utf-8 -*-
"""3단계. 발령 필터 + 인원 이동 매트릭스.

- 조직개편 발령만 사용하고 전배는 전량 제외한다 (섞이면 비율이 오염된다)
- 개편 기준일 ±N일 범위만 인정
- 동일 사번 복수 발령 시 최신 건
"""
from __future__ import annotations

import logging
from datetime import date, timedelta

log = logging.getLogger("reorg")


# 'YYYY-MM-DD' → date
def _d(v: str) -> date:
    y, m, dd = v.split("-")
    return date(int(y), int(m), int(dd))


# 조직개편 발령만 남긴다. 스킵 사유는 전부 로그에 남긴다.
def filter_reorg_assignments(assigns: list, cfg) -> list:
    reorg_code = cfg.reorg["REASON_CODE_REORG"]
    transfer_code = cfg.reorg["REASON_CODE_TRANSFER"]
    base = _d(cfg.reorg["REORG_DATE"])
    tol = timedelta(days=int(cfg.th("REORG_DATE_TOLERANCE")))
    lo, hi = base - tol, base + tol

    kept: dict[str, object] = {}
    counts = {"transfer": 0, "other_reason": 0, "out_of_range": 0, "kept": 0}
    for a in assigns:
        if a.reasonCode == transfer_code:
            counts["transfer"] += 1
            continue
        if a.reasonCode != reorg_code:
            counts["other_reason"] += 1
            log.debug("발령 제외(사유코드 %s): %s", a.reasonCode, a.userId)
            continue
        if not (lo <= _d(a.effectiveDate) <= hi):
            counts["out_of_range"] += 1
            log.warning(
                "발령 제외(기준일 ±%d일 범위 밖, %s): 사번 %s",
                int(cfg.th("REORG_DATE_TOLERANCE")), a.effectiveDate, a.userId,
            )
            continue
        prev = kept.get(a.userId)
        # 동일 사번 복수 발령 → 최신 발령일자 기준 (동일 일자면 나중 행)
        if prev is None or a.effectiveDate >= prev.effectiveDate:
            if prev is not None:
                log.info("사번 %s 복수 발령 — 최신 건(%s) 채택", a.userId, a.effectiveDate)
            kept[a.userId] = a
    counts["kept"] = len(kept)
    log.info(
        "발령 필터: 채택 %d건 / 전배제외 %d건 / 타사유 %d건 / 기간밖 %d건",
        counts["kept"], counts["transfer"], counts["other_reason"], counts["out_of_range"],
    )
    return [kept[k] for k in sorted(kept)]


# 조직코드 간 인원 이동 매트릭스 { from: { to: count } }
def build_move_matrix(reorg_assigns: list) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for a in reorg_assigns:
        if not a.beforeOrgCode or not a.afterOrgCode:
            log.warning("발령 스킵(조직코드 누락): 사번 %s", a.userId)
            continue
        if a.beforeOrgCode == a.afterOrgCode:
            continue
        matrix.setdefault(a.beforeOrgCode, {})
        matrix[a.beforeOrgCode][a.afterOrgCode] = matrix[a.beforeOrgCode].get(a.afterOrgCode, 0) + 1
    return matrix
