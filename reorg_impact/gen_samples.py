# -*- coding: utf-8 -*-
"""9단계. 테스트 데이터 생성.

SC-00 ~ SC-09 전 케이스 + 전배 혼입 + 기간 밖 발령 + 순환참조 + 인원 0명 조직을 담는다.
전부 UTF-8 (BOM 없음) 로 생성한다.

  python3 -m reorg_impact.gen_samples ./sample_data
"""
from __future__ import annotations

import sys
from pathlib import Path

# 기대 판정:
#   A001 SC-08(B001 흡수) / A002 SC-00 / B002 SC-01(상위변경) / B001 SC-07
#   B003→C003 SC-02 CF-H / B004 SC-05(C004·C005 분산) / B005 SC-04(유입처 없음)
#   B006·B007→C006 SC-06 / B008 SC-09(인원 0명) / C007 SC-03 / X001·X002 순환참조
FILES = {
"orgs_before": """orgCode,orgName,parentCode
HQ,본사,
A000,경영지원본부,HQ
B000,기술본부,HQ
A001,정보보안운영팀,A000
A002,인사팀,A000
B001,정보보안기획팀,B000
B002,플랫폼팀,B000
B003,데이터팀,B000
B004,인프라운영팀,B000
B005,구매팀,B000
B006,감사팀,B000
B007,준법팀,B000
B008,신설대기팀,B000
X001,순환테스트1팀,X002
X002,순환테스트2팀,X001
""",
"orgs_after": """orgCode,orgName,parentCode
HQ,본사,
A000,경영지원본부,HQ
B000,기술본부,HQ
A001,정보보안운영팀,A000
A002,인사팀,A000
B002,플랫폼팀,A000
C003,데이터플랫폼팀,B000
C004,인프라1팀,B000
C005,인프라2팀,B000
C006,감사준법팀,B000
C007,AI서비스팀,B000
X001,순환테스트1팀,X002
X002,순환테스트2팀,X001
""",
"members_before": """userId,orgCode,jobCode
u101,A001,SEC
u102,A001,SEC
u103,A001,DEV
u201,A002,HR
u202,A002,HR
u301,B001,SEC
u302,B001,SEC
u303,B001,SEC
u304,B001,DEV
u401,B002,DEV
u402,B002,DEV
u501,B003,DATA
u502,B003,DATA
u503,B003,DATA
u504,B003,DATA
u601,B004,INFRA
u602,B004,INFRA
u603,B004,INFRA
u604,B004,INFRA
u701,B005,BUY
u702,B005,BUY
u703,B005,BUY
u801,B006,AUDIT
u802,B006,AUDIT
u901,B007,LEGAL
u902,B007,LEGAL
ux01,X001,DEV
ux02,X002,DEV
""",
"members_after": """userId,orgCode,jobCode
u101,A001,SEC
u102,A001,SEC
u103,A001,DEV
u301,A001,SEC
u302,A001,SEC
u303,A001,SEC
u304,A001,DEV
u201,A002,HR
u202,A002,HR
u401,B002,DEV
u402,B002,DEV
u501,C003,DATA
u502,C003,DATA
u503,C003,DATA
u504,C003,DATA
u601,C004,INFRA
u602,C004,INFRA
u603,C005,INFRA
u604,C005,INFRA
u801,C006,AUDIT
u802,C006,AUDIT
u901,C006,LEGAL
u902,C006,LEGAL
u1001,C007,DEV
ux01,X001,DEV
ux02,X002,DEV
""",
# ORG=조직개편, TRF=전배(제외 대상), PRO=승진(무관)
"assignments": """userId,effectiveDate,reasonCode,beforeOrgCode,afterOrgCode
u301,2026-04-01,ORG,B001,A001
u302,2026-04-01,ORG,B001,A001
u303,2026-04-01,ORG,B001,A001
u304,2026-04-01,ORG,B001,A001
u501,2026-04-01,ORG,B003,C003
u502,2026-04-01,ORG,B003,C003
u503,2026-04-01,ORG,B003,C003
u504,20260401,ORG,B003,C003
u601,2026-04-01,ORG,B004,C004
u602,2026-04-01,ORG,B004,C004
u603,2026-04-01,ORG,B004,C005
u604,2026-04-01,ORG,B004,C005
u801,2026-04-01,ORG,B006,C006
u802,2026-04-01,ORG,B006,C006
u901,2026-04-01,ORG,B007,C006
u902,2026-04-01,ORG,B007,C006
u604,2026-04-01,TRF,B004,A002
u504,2026-04-01,TRF,B003,A002
u201,2026-04-01,TRF,A002,A001
u701,2026-05-20,ORG,B005,A001
u103,2026-03-30,PRO,A001,A001
""",
# 형태 A (1룰-1부서조건 1행). R-011 은 부서조건이 2개인 룰.
"rules": """ruleId,permissionId,ruleType,orgCode,includeSubDept,jobCodes
R-001,PERM_X,AUTO,A001,N,
R-002,PERM_X,AUTO,B001,N,
R-003,PERM_Y,BLOCK,B001,N,
R-004,PERM_Y,AUTO,A001,N,
R-005,PERM_Z,AUTO,B000,Y,
R-006,PERM_W,AUTO,B003,Y,DATA
R-007,PERM_V,BLOCK,B005,N,
R-008,PERM_U,AUTO,B008,Y,
R-009,PERM_T,AUTO,B006,N,
R-010,PERM_T,BLOCK,B007,N,
R-011,PERM_S,AUTO,A002,N,
R-011,PERM_S,AUTO,B004,Y,
R-012,PERM_R,AUTO,X001,Y,
""",
}

SAMPLE_CONFIG = """{
  "reorg": {
    "REORG_DATE": "2026-04-01",
    "REASON_CODE_REORG": "ORG",
    "REASON_CODE_TRANSFER": "TRF"
  }
}
"""


# 샘플 CSV 6종과 config.json 을 생성한다.
def generate(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    for name, body in FILES.items():
        (outdir / f"{name}.csv").write_text(body, encoding="utf-8")
    (outdir / "config.json").write_text(SAMPLE_CONFIG, encoding="utf-8")
    print(f"샘플 생성 완료: {outdir} ({len(FILES)}개 CSV + config.json)")


if __name__ == "__main__":
    generate(Path(sys.argv[1] if len(sys.argv) > 1 else "./sample_data"))
