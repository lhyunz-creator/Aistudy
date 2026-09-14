# 조직개편 권한 룰 영향도 분석 도구

조직개편 전후 데이터를 비교해 **영향받는 IAM 권한 룰을 빠짐없이 찾아내고, 조치 판단 근거를 제시**한다.
읽기 전용이며 룰을 직접 수정하지 않는다. 출력은 변경 제안까지다.

- 요구사항·판정 규칙은 [`docs/`](docs/) 참조 (01 요구사항 · 02 시나리오코드 · 03 데이터딕셔너리 · 04 화면 · 05 개발요청서)
- 외부 의존성 없음 (Python 3.10+ 표준 라이브러리만 사용)

## 실행

```bash
# 1) 샘플 데이터 생성 (SC-00~SC-09 전 케이스 포함)
python3 -m reorg_impact.gen_samples ./reorg_impact/sample_data

# 2) 분석
python3 -m reorg_impact \
    --in  ./reorg_impact/sample_data \
    --out ./out \
    --config ./reorg_impact/sample_data/config.json

# 설정 파일 없이 필수값만 넘겨도 된다
python3 -m reorg_impact --in ./data --out ./out \
    --reorg-date 2026-04-01 --reason-reorg ORG --reason-transfer TRF
```

입력 디렉터리에 `orgs_before.csv` `orgs_after.csv` `members_before.csv` `members_after.csv`
`assignments.csv` `rules.csv` 6종이 있어야 한다. 전부 UTF-8.

## 출력

| 파일 | 내용 | 인코딩 |
|---|---|---|
| `summary.md` | 사람이 읽는 요약. 최상단에 고아 룰 건수 | UTF-8 |
| `org_changes.csv` | 조직코드별 SC/CF 판정 + evidence | UTF-8 with BOM |
| `rule_actions.csv` | 룰별 조치 제안 (`decision` 칸은 검토자 기입용 공란) | UTF-8 with BOM |
| `member_impact.csv` | 룰별 신규/이탈 대상자 | UTF-8 with BOM |
| `orphan_rules.csv` | 고아 룰 단독 리포트 (최종 안전망) | UTF-8 with BOM |
| `analysis.log` | 스킵·경고 전체 기록 | UTF-8 |

## 모듈 구성

| 파일 | 단계 | 역할 |
|---|---|---|
| `config.py` | — | 임계치·컬럼명·코드값 상수. 하드코딩 금지 지점을 전부 모아 둔 곳 |
| `loader.py` | 1 | CSV 로드, UTF-8 검증, 필수 컬럼·조직코드 중복 검사, 룰 그룹핑 |
| `tree.py` | 2 | 조직 트리 (깊이 제한 없음, 순환참조는 해당 경로만 스킵) |
| `moves.py` | 3 | 발령 필터(전배 제외·기준일 ±N일), 인원 이동 매트릭스 |
| `classify.py` | 4 | SC/CF 분류기 (02 문서 5장 판정 순서) |
| `rules_impact.py` | 5·6 | 고아 룰 검출, 룰별 조치 제안, 충돌·중복 검출 |
| `simulate.py` | 7 | 기존 판정 로직 재현 → before/after 대상자 차집합 |
| `report.py` | 8 | CSV 4종 + summary.md |
| `gen_samples.py` | 9 | 테스트 데이터 생성 |

## 판정 요약

- 판정에는 `orgCode` / `parentCode` / 조직개편 발령 인원 이동만 사용한다. **조직명은 표시 전용**이다.
- 자동 반영 제안은 `SC-02 / CF-H` 조합에서만 나온다 (`requiresApproval=N`). 나머지는 전부 승인 또는 수동.
- `SC-01`, `SC-08` 은 룰 수정 대상이 아니다. 대상자 증감만 보여준다.
- 고아 룰 검출은 분류 결과와 무관하게 단독 수행된다. 분류가 무엇을 놓쳐도 여기에 걸린다.
- 인원 0명 조직은 CF-L 을 넘지 못하고 자동 확정되지 않는다.

`evidence_member_ratio` 의 분모는 **개편 전 직속 인원수**이며, 인원이 0명이면 추적된 이동 건수를 쓴다.
SC-08(범위확대)의 비율은 `유입 인원 / 기존 직속 인원` 이라 100%를 넘을 수 있다.

## 테스트

```bash
python3 -m unittest discover -s reorg_impact/tests -t .
```

샘플 데이터로 SC-00~SC-09 판정, 전배 필터링, 기준일 범위 필터, 순환참조 안전성,
부서·직무 매칭(OR/AND), 인코딩 중단 메시지를 검증한다.

## 아직 확정되지 않은 것 (추측해서 구현하지 않은 부분)

03 데이터딕셔너리가 채워지면 `config.py` / `config.sample.json` 만 고치면 된다.

- [ ] CSV 6종의 실제 컬럼명 — 현재는 03 문서의 가칭을 기본값으로 둠
- [ ] 발령사유코드 실제 값 (조직개편 / 전배) — 필수 입력, 없으면 실행이 중단된다
- [ ] `ruleType` 실제 코드값 — `RULE_TYPE_MAP` 으로 매핑
- [ ] 불리언 표기 (Y/N, true/false, 1/0) — 해석 불가한 값은 스킵하고 경고
- [ ] 복수값 구분자 (직무코드, 형태 B 조직코드)
- [ ] 겸직자 처리 규칙 — 현재는 모든 행을 유지하고 경고만 남긴다
- [ ] 휴직·파견·퇴직예정자 제외 여부 — 현재는 입력에 있는 그대로 집계
- [ ] 04 화면설계서의 검토 UI — 이번 범위에 넣지 않았다. CLI 출력(CSV/md)으로 검토한다
