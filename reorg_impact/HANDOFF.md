# 사내 반입 후 작업 순서

실제 CSV 는 사내에서만 볼 수 있으므로, 이 도구는 **컬럼명·코드값을 설정으로 분리한 상태**로 만들어져 있다.
반입 후에는 코드를 고칠 필요 없이 `config.json` 만 채우면 동작한다.

## 0. 반입 전 확인

| 항목 | 값 |
|---|---|
| 실행 요건 | Python 3.10 이상. 그 외 설치 필요 없음 |
| 외부 의존성 | 없음 (표준 라이브러리만) |
| 네트워크 통신 | 없음 |
| DB 접근 | 없음. 입력은 CSV 파일, 출력은 파일 |
| 쓰기 작업 | `--out` 으로 지정한 디렉터리에만 |

```bash
python3 --version          # 3.10 이상인지
python3 -m unittest discover -s reorg_impact/tests -t .   # 13 tests OK 면 정상 반입
```

## 1. 실제 CSV 6종 확보

`orgs_before` `orgs_after` `members_before` `members_after` `assignments` `rules` — 전부 UTF-8.
받은 뒤 **헤더 첫 줄만** 확인하면 된다.

```bash
for f in orgs_before orgs_after members_before members_after assignments rules; do
  echo "== $f"; head -1 ./data/$f.csv
done
```

## 2. config.json 채우기

`config.sample.json` 을 복사해 쓴다. 고칠 곳은 세 군데다.

```bash
cp reorg_impact/config.sample.json ./config.json
```

**(1) `reorg` — 이게 비면 실행이 중단된다**

| 키 | 넣을 값 |
|---|---|
| `REORG_DATE` | 개편 기준일 `YYYY-MM-DD` |
| `REASON_CODE_REORG` | 조직개편 발령사유코드 실제 값 |
| `REASON_CODE_TRANSFER` | 전배 발령사유코드 실제 값 |

> 전배 코드가 틀리면 인원 이동 비율이 오염되어 **조직 변경 판정이 통째로 틀어진다.** 가장 먼저 확인할 값이다.

**(2) `columns` — 1단계에서 확인한 실제 헤더로 교체**

왼쪽(논리명)은 그대로 두고 오른쪽 값만 바꾼다.
`rules` 의 부서조건이 한 셀에 여러 개 나열되는 형태(형태 B)면 `values.MULTI_VALUE_SEP` 도 실제 구분자로 맞춘다.

**(3) `values` — 코드값 표기**

| 키 | 확인할 것 |
|---|---|
| `RULE_TYPE_MAP` | ruleType 실제 값 → `AUTO` / `BLOCK` 매핑. 예: `{"1":"AUTO","2":"BLOCK"}` |
| `BOOL_TRUE` / `BOOL_FALSE` | 하위부서포함 표기 (Y/N, true/false, 1/0) |
| `MULTI_VALUE_SEP` | 직무코드·조직코드 복수값 구분자 |

## 3. 실행

```bash
python3 -m reorg_impact --in ./data --out ./out --config ./config.json
```

먼저 **일부 룰만 넣은 축소 CSV** 로 한 번 돌려보고 결과가 예상과 맞는지 확인한 뒤 전체를 돌리는 걸 권한다.

## 4. 결과 확인 순서

1. `out/summary.md` 최상단 **고아 룰 건수** — 지금 고장난 룰이다. 여기부터 본다
2. `out/analysis.log` 의 WARNING — 스킵된 행이 있으면 데이터 문제다. 건수가 예상보다 많으면 config 설정이 틀렸을 가능성이 높다
3. `out/org_changes.csv` — SC/CF 판정과 evidence(이동비율·상위조직 일치·하위구성 일치). 판정이 이상하면 evidence 로 원인을 추적한다
4. `out/rule_actions.csv` — 룰별 조치 제안. **`decision` 칸이 비어 있으니 검토자가 이관/폐기/보류를 직접 기입**한다
5. `out/member_impact.csv` — 룰별 신규·이탈 대상자

## 5. 자주 나는 오류

| 메시지 | 원인 · 조치 |
|---|---|
| `UTF-8이 아닙니다 (감지: CP949)` | 메모장에서 열어 "다른 이름으로 저장 > 인코딩: UTF-8" 로 다시 저장. 도구가 자동 변환하지 않는 건 의도된 동작이다 |
| `필수 컬럼이 없습니다` | `config.json` 의 `columns` 값이 실제 헤더와 다름 |
| `조직코드가 중복됩니다` | 조직 목록에 같은 코드가 두 번. 원본 추출 조건 확인 (폐지 조직 포함 여부 등) |
| `필수 설정값이 비어 있습니다` | `reorg` 3개 값 미입력 |
| `종류값 '...' 를 AUTO/BLOCK 으로 해석할 수 없어 스킵` | `RULE_TYPE_MAP` 에 실제 코드값 추가 |
| 고아 룰이 비정상적으로 많음 | 조직코드 컬럼 매핑이 틀렸거나 `orgs_after` 추출 범위가 잘못됐을 가능성 |

## 6. 실데이터 보고 확정할 것 (03 데이터딕셔너리)

- [ ] 발령사유코드 전체 목록 — 조직개편/전배 외에 승진·입사·퇴직이 섞여 들어오는지
- [ ] 조직개편 발령이 하루에 몰리는지, 며칠에 걸쳐 나오는지 → `REORG_DATE_TOLERANCE` 조정
- [ ] 폐지 조직이 `orgs_after` 에 남는지 (남으면 고아 룰이 안 잡힌다)
- [ ] 겸직자 — 한 사번이 여러 행인지 (현재는 모든 행 유지 + 경고)
- [ ] 휴직·파견·퇴직예정자를 룰 대상에서 빼야 하는지 (현재는 입력 그대로 집계)
- [ ] 비활성 상태 룰이 `rules.csv` 에 포함되는지 (포함되면 상태 컬럼으로 필터 필요)
- [ ] 룰에 직무 외 다른 조건(직급·재직상태)이 있는지

위 항목이 확정되면 `config.py` 상단의 `TODO` 주석 지점만 손보면 된다.

## 7. 보안 주의

`member_impact.csv` 에는 **사번이 그대로 들어간다.** 출력 디렉터리는 사내 밖으로 반출하지 않는다.
공유가 필요하면 `summary.md` 의 집계 수치만 쓰거나, `added_userIds` / `removed_userIds` 컬럼을 지우고 공유한다.
