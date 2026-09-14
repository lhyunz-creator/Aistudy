# -*- coding: utf-8 -*-
"""1단계. 입력 로더 + 검증.

- 인코딩 검증: UTF-8 이 아니면 자동 변환하지 않고 즉시 중단
- 필수 컬럼 / 조직코드 중복 검증
- 경고는 전부 로그에 남긴다 (조용한 실패 금지)
"""
from __future__ import annotations

import csv
import io
import logging
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config, REQUIRED_COLUMNS

log = logging.getLogger("reorg")

# 입력 파일 논리명 → 컬럼 정의 종류
FILE_KINDS = {
    "orgs_before": "orgs",
    "orgs_after": "orgs",
    "members_before": "members",
    "members_after": "members",
    "assignments": "assignments",
    "rules": "rules",
}


class InputError(Exception):
    """중단 사유 (인코딩·필수컬럼·중복)."""


@dataclass(frozen=True)
class Org:
    orgCode: str
    orgName: str
    parentCode: str


@dataclass(frozen=True)
class Member:
    userId: str
    orgCode: str
    jobCode: str


@dataclass(frozen=True)
class Assign:
    userId: str
    effectiveDate: str  # YYYY-MM-DD 로 정규화
    reasonCode: str
    beforeOrgCode: str
    afterOrgCode: str


@dataclass
class Rule:
    ruleId: str
    permissionId: str
    ruleType: str  # AUTO | BLOCK
    deptConditions: list = field(default_factory=list)  # [(orgCode, includeSubDept)]
    jobCodes: list = field(default_factory=list)


# 파일을 UTF-8 로 읽는다. 아니면 감지된 인코딩과 해결 방법을 담아 중단한다.
def read_text_utf8(path: Path) -> str:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        guess = _guess_encoding(raw)
        raise InputError(
            f"[입력 오류] {path.name} 가 UTF-8이 아닙니다 (감지: {guess})\n"
            '  → 메모장에서 열어 "다른 이름으로 저장 > 인코딩: UTF-8" 로 다시 저장한 뒤 올려주세요.'
        )
    return text.lstrip("﻿")  # BOM 제거


# 참고용 인코딩 추정. 변환에는 절대 쓰지 않는다.
def _guess_encoding(raw: bytes) -> str:
    for enc in ("cp949", "euc-kr", "utf-16"):
        try:
            raw.decode(enc)
            return enc.upper()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "알 수 없음"


# CSV 를 dict 목록으로 읽고 필수 컬럼을 확인한다.
def read_csv(path: Path, kind: str, cfg: Config) -> list[dict]:
    text = read_text_utf8(path)
    reader = csv.DictReader(io.StringIO(text))
    headers = [h.strip() for h in (reader.fieldnames or [])]
    missing = [
        cfg.col(kind, logical)
        for logical in REQUIRED_COLUMNS[kind]
        if cfg.col(kind, logical) not in headers
    ]
    if missing:
        raise InputError(
            f"[입력 오류] {path.name} 에 필수 컬럼이 없습니다: {', '.join(missing)}\n"
            f"  → 헤더: {', '.join(headers)}\n"
            "  → 실제 컬럼명이 다르면 config.json 의 columns 설정을 맞춰주세요."
        )
    rows = []
    for row in reader:
        rows.append({(k or "").strip(): (v or "").strip() for k, v in row.items()})
    log.info("%s 로드: %d행", path.name, len(rows))
    return rows


# 조직 목록 로드. 조직코드 중복은 중단 사유.
def load_orgs(path: Path, cfg: Config) -> dict[str, Org]:
    rows = read_csv(path, "orgs", cfg)
    c = cfg.columns["orgs"]
    orgs: dict[str, Org] = {}
    for row in rows:
        code = row.get(c["orgCode"], "")
        if not code:
            log.warning("%s: 조직코드가 비어 있어 스킵 (row=%s)", path.name, row)
            continue
        if code in orgs:
            raise InputError(f"[입력 오류] {path.name} 에 조직코드가 중복됩니다: {code}")
        orgs[code] = Org(code, row.get(c.get("orgName", ""), ""), row.get(c["parentCode"], ""))
    return orgs


# 임직원 목록 로드. 조직 목록에 없는 소속은 경고 후 집계 제외.
def load_members(path: Path, cfg: Config, orgs: dict[str, Org]) -> list[Member]:
    rows = read_csv(path, "members", cfg)
    c = cfg.columns["members"]
    members: list[Member] = []
    seen: set[str] = set()
    for row in rows:
        uid = row.get(c["userId"], "")
        code = row.get(c["orgCode"], "")
        if not uid:
            log.warning("%s: 사번이 비어 있어 스킵 (row=%s)", path.name, row)
            continue
        if code not in orgs:
            log.warning("%s: 사번 %s 의 조직코드 %s 가 조직 목록에 없어 집계 제외", path.name, uid, code)
            continue
        if uid in seen:
            # TODO: 정의 필요 — 겸직자 처리 규칙 미확정. 현재는 모든 행을 유지한다.
            log.warning("%s: 사번 %s 가 중복 등장 (겸직 처리 규칙 미정)", path.name, uid)
        seen.add(uid)
        members.append(Member(uid, code, row.get(c.get("jobCode", ""), "")))
    return members


# 발령 내역 로드. 날짜는 YYYY-MM-DD 로 정규화한다.
def load_assignments(path: Path, cfg: Config) -> list[Assign]:
    rows = read_csv(path, "assignments", cfg)
    c = cfg.columns["assignments"]
    out: list[Assign] = []
    for row in rows:
        date = normalize_date(row.get(c["effectiveDate"], ""))
        if date is None:
            log.warning("%s: 발령일자 형식을 해석할 수 없어 스킵 (row=%s)", path.name, row)
            continue
        out.append(
            Assign(
                row.get(c["userId"], ""),
                date,
                row.get(c["reasonCode"], ""),
                row.get(c["beforeOrgCode"], ""),
                row.get(c["afterOrgCode"], ""),
            )
        )
    return out


# YYYY-MM-DD / YYYYMMDD 둘 다 허용
def normalize_date(raw: str):
    v = (raw or "").strip()
    if len(v) == 10 and v[4] == "-" and v[7] == "-":
        head = v.replace("-", "")
        return v if head.isdigit() else None
    if len(v) == 8 and v.isdigit():
        return f"{v[0:4]}-{v[4:6]}-{v[6:8]}"
    return None


# 룰 로드. ruleId 기준으로 그룹핑해 1룰 1객체로 재구성한다.
# 03 문서 5장의 형태 A(행 분리) / 형태 B(한 셀 나열) 를 모두 받는다.
def load_rules(path: Path, cfg: Config) -> list[Rule]:
    rows = read_csv(path, "rules", cfg)
    c = cfg.columns["rules"]
    rules: dict[str, Rule] = {}
    for row in rows:
        rid = row.get(c["ruleId"], "")
        if not rid:
            log.warning("%s: 룰 ID가 비어 있어 스킵 (row=%s)", path.name, row)
            continue
        rtype = cfg.rule_type(row.get(c["ruleType"], ""))
        if rtype is None:
            log.warning(
                "%s: 룰 %s 의 종류값 '%s' 를 AUTO/BLOCK 으로 해석할 수 없어 스킵",
                path.name, rid, row.get(c["ruleType"], ""),
            )
            continue
        codes = cfg.split_multi(row.get(c["orgCode"], ""))
        flags_raw = cfg.split_multi(row.get(c["includeSubDept"], ""))
        if len(codes) != len(flags_raw):
            # 형태 B 에서 순서·개수가 어긋나면 전혀 다른 룰이 된다. 추측하지 않고 스킵.
            log.warning(
                "%s: 룰 %s 의 조직코드(%d개)와 하위포함 플래그(%d개) 개수가 달라 해당 행 스킵",
                path.name, rid, len(codes), len(flags_raw),
            )
            continue
        conds = []
        for code, flag in zip(codes, flags_raw):
            inc = cfg.is_true(flag)
            if inc is None:
                log.warning("%s: 룰 %s 의 하위부서포함 값 '%s' 를 해석할 수 없어 해당 조건 스킵", path.name, rid, flag)
                continue
            conds.append((code, inc))
        rule = rules.get(rid)
        if rule is None:
            rule = Rule(rid, row.get(c["permissionId"], ""), rtype, [], cfg.split_multi(row.get(c.get("jobCodes", ""), "")))
            rules[rid] = rule
        elif rule.ruleType != rtype or rule.permissionId != row.get(c["permissionId"], ""):
            log.warning("%s: 룰 %s 의 권한/종류가 행마다 달라 첫 행 기준으로 유지", path.name, rid)
        rule.deptConditions.extend(conds)
        for job in cfg.split_multi(row.get(c.get("jobCodes", ""), "")):
            if job not in rule.jobCodes:
                rule.jobCodes.append(job)

    out = []
    for rid, rule in rules.items():
        if not rule.deptConditions:
            log.warning("룰 %s: 부서 조건이 비어 있어 잘못된 룰로 스킵", rid)
            continue
        # 중복 조건 제거 (결정론적 순서 유지)
        seen, conds = set(), []
        for cond in rule.deptConditions:
            if cond not in seen:
                seen.add(cond)
                conds.append(cond)
        rule.deptConditions = conds
        out.append(rule)
    out.sort(key=lambda r: r.ruleId)
    return out


@dataclass
class InputSet:
    orgs_before: dict
    orgs_after: dict
    members_before: list
    members_after: list
    assignments: list
    rules: list


# 입력 6종을 한 번에 로드한다.
def load_all(indir: Path, cfg: Config) -> InputSet:
    paths = {name: indir / f"{name}.csv" for name in FILE_KINDS}
    missing = [p.name for p in paths.values() if not p.exists()]
    if missing:
        raise InputError(f"[입력 오류] 필요한 파일이 없습니다: {', '.join(missing)}")
    orgs_before = load_orgs(paths["orgs_before"], cfg)
    orgs_after = load_orgs(paths["orgs_after"], cfg)
    return InputSet(
        orgs_before=orgs_before,
        orgs_after=orgs_after,
        members_before=load_members(paths["members_before"], cfg, orgs_before),
        members_after=load_members(paths["members_after"], cfg, orgs_after),
        assignments=load_assignments(paths["assignments"], cfg),
        rules=load_rules(paths["rules"], cfg),
    )
