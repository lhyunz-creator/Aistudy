# -*- coding: utf-8 -*-
"""실행 진입점.

  python3 -m reorg_impact --in ./data --out ./out \
      --reorg-date 2026-04-01 --reason-reorg R01 --reason-transfer R02
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .classify import classify
from .config import load_config
from .loader import InputError, load_all
from .moves import build_move_matrix, filter_reorg_assignments
from .report import (write_member_impact, write_org_changes, write_orphans,
                     write_rule_actions, write_summary)
from .rules_impact import (build_rule_actions, detect_conflicts, detect_duplicates,
                           detect_orphans, mark_unresolved_orphans, rules_by_org)
from .simulate import simulate
from .tree import OrgTree

log = logging.getLogger("reorg")


# 로그는 파일과 콘솔 양쪽에 남긴다 (전 구간 UTF-8)
def setup_logging(outdir: Path, level: str):
    outdir.mkdir(parents=True, exist_ok=True)
    log.setLevel(getattr(logging, level.upper(), logging.INFO))
    log.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%H:%M:%S")
    fh = logging.FileHandler(outdir / "analysis.log", encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(sh)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="reorg_impact", description="조직개편 권한 룰 영향도 분석 (읽기 전용)")
    p.add_argument("--in", dest="indir", required=True, help="입력 CSV 6종이 있는 디렉터리")
    p.add_argument("--out", dest="outdir", default="./out", help="출력 디렉터리 (기본 ./out)")
    p.add_argument("--config", help="config.json 경로 (컬럼명·임계치 override)")
    p.add_argument("--reorg-date", help="개편 기준일 YYYY-MM-DD")
    p.add_argument("--reason-reorg", help="조직개편 발령사유코드")
    p.add_argument("--reason-transfer", help="전배 발령사유코드")
    p.add_argument("--log-level", default="INFO")
    p.add_argument("--version", action="version", version=__version__)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    indir, outdir = Path(args.indir), Path(args.outdir)
    setup_logging(outdir, args.log_level)

    try:
        cfg = load_config(args.config)
        for key, val in (("REORG_DATE", args.reorg_date),
                         ("REASON_CODE_REORG", args.reason_reorg),
                         ("REASON_CODE_TRANSFER", args.reason_transfer)):
            if val:
                cfg.reorg[key] = val
        missing = cfg.missing_required_settings()
        if missing:
            raise InputError(
                "[설정 오류] 필수 설정값이 비어 있습니다: " + ", ".join(missing) + "\n"
                "  → --reorg-date / --reason-reorg / --reason-transfer 로 넘기거나 config.json 에 넣어주세요."
            )

        # Step 0. 입력 로드 · 검증
        data = load_all(indir, cfg)
        # Step 1. 조직 트리
        tree_b = OrgTree(data.orgs_before, "before")
        tree_a = OrgTree(data.orgs_after, "after")
        # Step 2. 발령 필터 (전배 제외)
        reorg_assigns = filter_reorg_assignments(data.assignments, cfg)
        matrix = build_move_matrix(reorg_assigns)
        # Step 3. 조직 변경 분류
        changes = classify(data.orgs_before, data.orgs_after, tree_b, tree_a,
                           data.members_before, matrix, cfg)
        # Step 4-1. 고아 룰 (다른 단계와 무관하게 단독 수행)
        orphans = detect_orphans(data.rules, data.orgs_after)
        # Step 4-3/4-4. 충돌 · 중복
        conflicts = detect_conflicts(changes, data.rules)
        duplicates = detect_duplicates(changes, data.rules)
        # Step 4-2. 룰별 조치 제안
        actions = build_rule_actions(data.rules, changes, data.orgs_after, duplicates)
        orphans = mark_unresolved_orphans(orphans, actions)
        # Step 5. 대상자 시뮬레이션
        impacts = simulate(data.rules, tree_b, tree_a, data.members_before, data.members_after)

        # Step 6. 리포트
        idx = rules_by_org(data.rules)
        write_org_changes(outdir / "org_changes.csv", changes, data.orgs_before, data.orgs_after, idx)
        write_rule_actions(outdir / "rule_actions.csv", actions)
        write_member_impact(outdir / "member_impact.csv", impacts)
        write_orphans(outdir / "orphan_rules.csv", orphans)

        def org_label(ch):
            nb = tree_b.name_of(ch.code_before)
            na = tree_a.name_of(ch.code_after)
            if nb and na and nb != na:
                return f"{nb} → {na}"
            return nb or na or ""

        write_summary(outdir / "summary.md", {
            "changes": changes, "actions": actions, "orphans": orphans,
            "impacts": impacts, "conflicts": conflicts, "duplicates": duplicates,
            "reorg_date": cfg.reorg["REORG_DATE"], "rule_count": len(data.rules),
            "org_label": org_label,
        })

        log.info("완료 — 고아 룰 %d건 / 룰 조치 %d건 / 결과: %s", len(orphans), len(actions), outdir)
        print(f"\n고아 룰 {len(orphans)}건. 자세한 내용은 {outdir / 'summary.md'} 를 확인하세요.")
        return 0
    except InputError as e:
        log.error("%s", e)
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
