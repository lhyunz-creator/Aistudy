# -*- coding: utf-8 -*-
"""설정값 · 컬럼명 상수.

03 데이터딕셔너리가 미완성이므로 컬럼명과 코드값은 전부 여기에 상수로 모아 둔다.
아래 DEFAULT 값은 03 문서의 '가칭'을 그대로 옮긴 것이며, 실제 값이 확인되면
config.json 으로 덮어쓰거나 이 파일의 값을 교체한다.
"""
from __future__ import annotations

import json
from pathlib import Path

# TODO: 정의 필요 — 실제 CSV 헤더 확보 후 교체 (03 데이터딕셔너리 2~5장)
DEFAULT_COLUMNS = {
    "orgs": {"orgCode": "orgCode", "orgName": "orgName", "parentCode": "parentCode"},
    "members": {"userId": "userId", "orgCode": "orgCode", "jobCode": "jobCode"},
    "assignments": {
        "userId": "userId",
        "effectiveDate": "effectiveDate",
        "reasonCode": "reasonCode",
        "beforeOrgCode": "beforeOrgCode",
        "afterOrgCode": "afterOrgCode",
    },
    "rules": {
        "ruleId": "ruleId",
        "permissionId": "permissionId",
        "ruleType": "ruleType",
        "orgCode": "orgCode",
        "includeSubDept": "includeSubDept",
        "jobCodes": "jobCodes",
    },
}

# 각 파일의 필수 컬럼 (누락 시 중단)
REQUIRED_COLUMNS = {
    "orgs": ["orgCode", "parentCode"],
    "members": ["userId", "orgCode"],
    "assignments": ["userId", "effectiveDate", "reasonCode", "beforeOrgCode", "afterOrgCode"],
    "rules": ["ruleId", "permissionId", "ruleType", "orgCode", "includeSubDept"],
}

DEFAULT_VALUES = {
    # TODO: 정의 필요 — 실제 불리언 표기 확인 (Y/N, true/false, 1/0 중 무엇인지)
    "BOOL_TRUE": ["Y", "y", "TRUE", "true", "True", "1"],
    "BOOL_FALSE": ["N", "n", "FALSE", "false", "False", "0", ""],
    # TODO: 정의 필요 — ruleType 실제 코드값. 왼쪽이 CSV 값, 오른쪽이 내부값(AUTO|BLOCK)
    "RULE_TYPE_MAP": {"AUTO": "AUTO", "BLOCK": "BLOCK", "자동화": "AUTO", "통제": "BLOCK"},
    # TODO: 정의 필요 — 직무코드/조직코드 복수 표기 구분자 (03 문서 5장 형태 B)
    "MULTI_VALUE_SEP": ";",
}

DEFAULT_THRESHOLDS = {
    "MEMBER_THRESHOLD": 0.9,       # 단일 코드 수렴 판정 임계치
    "SPLIT_MIN_RATIO": 0.1,        # 분할 판정 시 유효 분기 최소 비율
    "CHILD_MATCH_RATIO": 0.5,      # 하위조직 구성 일치로 인정할 최소 겹침 비율
    "REORG_DATE_TOLERANCE": 3,     # 개편 발령 인정 일자 범위(±일)
}

DEFAULT_REORG = {
    "REORG_DATE": None,            # 필수 입력 (YYYY-MM-DD)
    "REASON_CODE_REORG": None,     # 필수 입력 — TODO: 실제 조직개편 발령사유코드
    "REASON_CODE_TRANSFER": None,  # 필수 입력 — TODO: 실제 전배 발령사유코드
}


class Config:
    """설정 묶음. config.json 이 있으면 기본값 위에 덮어쓴다."""

    def __init__(self, data: dict | None = None):
        data = data or {}
        self.columns = _merge(DEFAULT_COLUMNS, data.get("columns", {}))
        self.values = _merge(DEFAULT_VALUES, data.get("values", {}))
        self.thresholds = dict(DEFAULT_THRESHOLDS, **data.get("thresholds", {}))
        self.reorg = dict(DEFAULT_REORG, **data.get("reorg", {}))

    # 임계치 접근자 — 하드코딩 금지 원칙에 따라 코드에서는 이 경로로만 읽는다
    def th(self, key: str):
        return self.thresholds[key]

    def col(self, kind: str, logical: str) -> str:
        return self.columns[kind][logical]

    def is_true(self, raw: str) -> bool | None:
        """불리언 파싱. 정의되지 않은 표기는 None 을 돌려 호출부에서 경고하게 한다."""
        v = (raw or "").strip()
        if v in self.values["BOOL_TRUE"]:
            return True
        if v in self.values["BOOL_FALSE"]:
            return False
        return None

    def rule_type(self, raw: str) -> str | None:
        return self.values["RULE_TYPE_MAP"].get((raw or "").strip())

    def split_multi(self, raw: str) -> list[str]:
        sep = self.values["MULTI_VALUE_SEP"]
        return [v.strip() for v in (raw or "").split(sep) if v.strip()]

    def missing_required_settings(self) -> list[str]:
        return [k for k, v in self.reorg.items() if v in (None, "")]


def _merge(base: dict, override: dict) -> dict:
    out = {k: (dict(v) if isinstance(v, dict) else v) for k, v in base.items()}
    for k, v in override.items():
        if isinstance(out.get(k), dict) and isinstance(v, dict):
            out[k].update(v)
        else:
            out[k] = v
    return out


# 설정 파일 로드 (없으면 기본값)
def load_config(path: str | Path | None) -> Config:
    if not path:
        return Config()
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"설정 파일이 없습니다: {p}")
    return Config(json.loads(p.read_text(encoding="utf-8-sig")))
