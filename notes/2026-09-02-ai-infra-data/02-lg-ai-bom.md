# AI-BOM: AI 공급망 투명성 — 세션 정리

**행사**: AI Infrastructure & Data 2026 (CIO / ITWORLD)
**일시·장소**: 2026-09-02(수), 서울 드래곤시티 그랜드볼룸 한라(3F)
**발표**: LG AI연구원 (LG AI Research) — 학습데이터 컴플라이언스 담당 (법률 전문가)
**한 줄 요약**: **"신뢰는 한 번도 맹목적인 믿음이었던 적이 없다. 언제나 '보이는가'의 문제였다"** — SBOM이 코드의 투명성을 풀었듯, AI-BOM은 **학습 데이터의 계보**를 풀어야 한다.
**자료**: 슬라이드 p.6~28 + **발표 녹취록 반영** (녹취에서만 나온 내용은 본문에 별도 표기)

---

## 0. 발표사 소개 — How LG AI Research Builds AI Leadership

독자 파운데이션 모델과 산업 전문 역량을 결합해 현장 중심의 AI 혁신 달성.

| # | 축 | 내용 |
|---|---|---|
| 01 | 파운데이션 모델 선제적 개발 | 2021년 5월 '초거대 AI 개발 선언'을 시작으로 잠재력을 조기 인식, 선제적 R&D 착수 |
| 02 | Expert AI 지향 | 깊이 있는 전문 도메인 지식 학습과 실사용성에 중점을 둔 산업 특화형 AI |
| 03 | 산업 현장 중심의 실질적 적용 | 전자·화학·통신·서비스 등 다양한 산업에 적용해 가시적 성과 창출 |
| 04 | Trust & Safety | 글로벌 AI 거버넌스 리더십 강화, 책임 있는 AI 개발 주도 |

*(녹취 보강: 5년간의 모델 개발 이력 — **EXAONE 1.0을 2021년 12월 시작**, 최근 독자 파운데이션 모델 **EXAONE 2.0을 Apache 2.0 오픈소스 라이선스로 출시**. 현재 기준 **750B 파라미터로 국내 최대 규모**의 파운데이션 모델. 제조업 현장 시설에 자사 AI 모델이 탑재되어 산업 현장에서 사용 중.)*

*(현장 메모: 멀티모달 VLM. 가장 많은 리소스를 쏟는 것이 **학습 데이터**)*

---

## 1. 왜 AI-BOM인가 (p.6)

**"공급망이 단절되지 않게 어떻게 지킬 것인가?"**

| 시대 | 명세서 | 무엇을 보장하나 |
|---|---|---|
| 하드웨어의 시대 | **부품 명세서 (BOM)** | 제조 공급망 투명성 + 제품 구성요소 추적성 |
| 소프트웨어의 시대 | **소프트웨어 명세서 (SBOM)** | 소프트웨어 공급망 투명성 + 의존성·라이선스 추적성 |
| 인공지능의 시대 | **AI 명세서 (AI-BOM)** | AI의 투명성은 어떻게 추적할 것인가? |

> 블랙박스인 AI의 투명성은 어떻게 보장할 수 있을까요? 지금의 SBOM 도구로 그 상자를 열 수 있을까요?

*(비유 메모: BOM은 건설·제조의 자재명세서. **케첩의 성분표** — 무엇이 들어갔고 안전한가를 아는 것과 같은 문제.)*

**왜 지금 입법이 몰리는가 (녹취 보강)**
EU AI Act, 한국 AI 기본법 등은 공통적으로 "AI를 어떻게 만들고 무슨 데이터를 썼는지 기록하라"고 요구한다. 왜 기록하라고 했는가를 끝까지 따라가면 이 질문에 닿는다:

> **AI가 로봇에 탑재되어 사람에게 위해를 가했을 때, 대체 무엇 때문에 이 문제가 발생했는가?**

한국은 **2026년 1월 AI 기본법 발효**. 발효 이후 각 기업에서 — LG 그룹 내부에서도 — 상당한 혼란이 있었고, 그 해결책으로 AI-BOM을 만들고 있다.

---

## 2. 왜 SBOM 도구로는 안 되는가

### 2-1. 소프트웨어 코드 vs AI 코드 (p.7)

| | 소프트웨어 | AI |
|---|---|---|
| 동작 방식 | 개발자가 정의한 로직 그대로 동작 (입력 → 출력) | 학습한 패턴을 바탕으로 **확률적으로** 결과 생성 (입력 → 출력 1/2/3) |
| 스캔 결과 | `source_code.py`의 `import flask` → 스캐너 탐지: flask 3.1.0, BSD-3-Clause | `train.py`의 `load_model('weights.h5')`, `load_dataset("./corpus/")` → **스캐너에는 파일 이름만 보임** |
| 결론 | 위험이 특정 코드 라인에 분명히 드러남 → **소스코드로 추적 가능** | 어떤 코드 한 줄로도 위험을 알아낼 수 없음 → **AI 모델 소스코드로는 추적 불가** |

### 2-2. AI BOM이 반드시 해결해야 할 세 가지 (p.8)

| 구성요소 | 스캐너로 잡히나 |
|---|---|
| **베이스 모델 아키텍처** | ✅ SBOM 스캐너가 찾아낼 수 있는 **유일한** 항목 |
| **모델 파라미터 및 가중치** | ❌ |
| **학습 데이터셋** | ❌ |

> 세 가지 중 두 가지는 코드에 아무 흔적도 남기지 않습니다. 그럼에도 AI BOM은 이를 기록해야 합니다.

### 2-3. 이미 한 번 풀어낸 문제, 구성요소만 바뀌었다 (p.9)

| | 소프트웨어 (SBOM) | AI (AI-BOM) |
|---|---|---|
| 구성요소는 무엇인가 | 패키지, 라이브러리, 버전 | 데이터셋, 모델, 가중치 |
| 누가 선언하는가 | 빌드 시스템이 자동으로 선언 | **아무도 하지 않는다** |
| 얼마나 깊은가 | 해석 가능하고, 대체로 깊지 않다 | 끝없이 깊고, 해석이 어렵다 |
| 무슨 질문에 답하는가 | 이 바이너리 안에 무엇이 있는가? | 이 모델 안에 무엇이 있는가? |
| 표준 | SPDX — 리눅스재단 · ISO/IEC 5962 | **SPDX 3.0 & OpenChain AI System BOM** — 리눅스재단 |

> 명세서에는 이미 그 자리가 마련되어 있습니다. **그 자리를 채울 방법이 없을 뿐입니다.**

---

## 3. 투명성은 '연결' 속에 있다 (p.11~12)

### 3-1. 세 개의 질문
| # | 항목 | 질문 |
|---|---|---|
| 1 | **모델 출처** | 이 모델을 처음부터 직접 만들었는가? 사전학습된 파운데이션 모델을 파인튜닝하거나 파생된 것인가? |
| 2 | **학습 데이터 계보** | 학습에 정확히 어떤 데이터셋을 사용했는가? |
| 3 | **데이터셋 출처** | 이 데이터는 어디서 비롯되었고, 적법하게 확보되었는가? |

베이스 모델 알고리즘 → 모델 파라미터·가중치 → 학습 데이터셋 → 데이터 출처(복수)

### 3-2. 모델은 형태를 남기지만, 데이터는 남기지 않는다

| 계보 | 상태 |
|---|---|
| **모델 계보** — "이 모델은 저 모델에서 파생되었다" | 표현 가능하고, 구조화되며, **기록으로 남는다** |
| **데이터셋 계보** — "이 데이터셋은… 어디서 왔는가?" | **선택 항목**. 그래서 요구되지 않고, 채워지지 않고, 존재하지 않는다 |

> 모델도 중요합니다. 하지만 우리가 여전히 볼 수 없는 쪽은 **데이터**입니다.

---

## 4. 법적 리스크는 이미 현실 (p.13~17)

### 4-1. 학습데이터 관련 주요 판례 (2024~)

**분쟁의 규모 (녹취 보강)**
현재 시점 기준 전 세계 **약 130~150건**의 AI 학습데이터 관련 분쟁이 존재하고, **100건 이상이 진행 중**. AI 관련 분쟁의 대부분이 학습데이터 이슈이며, 쟁점은 ① **저작권 침해**가 있었는가 ② **개인정보보호법 침해**가 있었는가로 모인다.
미국은 연방 차원의 통일된 개인정보보호법이 없어, 대부분 **원저작물의 권리자가 AI 회사를 상대로 손해배상 청구 + 금지명령**을 구하는 구조로 간다.

| 사건 | 국가 | 년도 | 승소 | 법적 배경 |
|---|---|---|---|---|
| Li v. Liu | China | 2024 | Plaintiff | Copyright law |
| Sin Changhwa Cultural Development LLC v. AI Company | China | 2024 | Plaintiff | Copyright law |
| Thomson Reuters v. ROSS Intelligence | U.S. | 2025 | Plaintiff | Copyright law (Fair use) |
| Andrea Bartz v. Anthropic | U.S. | 2025 | Plaintiff | Copyright law (Fair use) |
| Kadrey v. Meta | U.S. | 2025 | Defendant (AI Company) | Copyright law (Fair use) |
| Getty Images v. Stability AI | United Kingdom | 2025 | Defendant (AI Company) | Copyright law |
| GEMA v. OpenAI | Germany | 2025 | Plaintiff | Copyright law |
| GEMA v. Suno | Germany | 2026 | Plaintiff | Copyright law (US, Germany) |

**녹취에서 강조된 지점**
- **Andrea Bartz v. Anthropic** — 손해배상 **합의금 약 2조 원**. 결정적 원인은 오픈 데이터셋에 포함되어 있던 **불법 복제본 다운로드분**이 공정이용으로 인정되지 않은 것.
- **독일 GEMA(음악 저작권 신탁관리단체) v. OpenAI** — 저작권법상 법리적으로 OpenAI 완패. 이후 음악 생성 모델 **Suno도 독일에서 연쇄 패소** → "학습데이터 라이선스 컴플라이언스가 굉장히 중요하다"는 함의.

### 4-2. Open Source vs Open Data (p.14)

| | Source Code | AI Training Data |
|---|---|---|
| 형태 | 코드 | 코드, 텍스트, 이미지, 영상, 오디오 등 |
| 이용 목적 | 소프트웨어 개발 | **본래 저작물의 목적과 다른 목적** |
| 컴플라이언스 | Open Source Compliance (표준화되어 준수됨) | 표준화되지 않음 |
| 고지의 의무 | 표준화되어 준수됨 | 표준화되지 않음 |

- Source Code → *compile* → Software
- **Data + Source Code → *train* → AI Model** (데이터가 결과물의 일부가 된다)

### 4-3. 컴플라이언스 성숙도의 격차 (p.15)

- **Open Source**: AFPA v. Edu4 → SCO v. IBM($1B, 2003) → BusyBox(2007) → Jacobsen v. Katzer(2008) → Google v. Oracle(2018) → 현재. **20년 넘게 다듬어져 준비되어 있음**
- **Open Data**: Getty Image v. Stable Diffusion($1.8T, 2023) → 중국 2건(2024) → Thomson Reuters v. ROSS / Bartz v. Anthropic / GEMA v. OpenAI(2025) → 현재 → 미래. **아직 준비되지 않음**

### 4-4. 국가별 면책 규정 — 파편화 (p.16)

| 국가 | 항변 근거 | 핵심 조항 |
|---|---|---|
| 미국 | Fair Use | 17 U.S.C. § 107 (4요소 형량) |
| 한국 | 공정이용 | 저작권법 제35조의5 |
| EU | TDM 예외 | DSM Directive Arts. 3 & 4 |
| 일본 | 정보분석 예외 | 저작권법 제30조의4 |
| 싱가포르 | 전산데이터분석(CDA) 예외 | Copyright Act 2021 §§ 243–244 |
| 영국 | Fair Dealing | CDPA 1988 §§ 29–30 |

> 국가별로 저작권법상의 면책은 파편화되고 있고, **예측 가능성은 줄어들고 있습니다.**

**녹취 보강**
- 한국의 공정이용 조항은 **2012년 한미 FTA 당시 미국 저작권법의 공정이용 범위를 거의 그대로 차용**한 것. 여기에 공정위 가이드라인 등도 별도로 나오고 있다.
- 문제는 **글로벌 배포**. EXAONE 같은 모델을 허깅페이스에 올리면 지구 반대편까지 도달하는데, 그 국가의 저작권법은 어떤지, 항변 근거는 무엇인지를 매번 리서치해야 한다. 파편화가 심해질수록 **기업 내부 컴플라이언스 체계에 소모되는 에너지가 급증**한다.
- 규제 측면: **EU AI Act**, **캘리포니아 AB 2013** 등이 "이 관할에서 서비스되는 AI는 무엇으로 학습했는지 요약을 공개하라"고 요구. 한국도 학습데이터 요약본 명세화 규제가 있다.
- 고객 요구: AI 모델을 제3자·고객사에 제공할 때 **"학습데이터를 뭘로 썼는지 공개해 달라"**는 요청이 실제로 꽤 들어온다 (그룹사 포함).

### 4-5. Andrea Bartz v. Anthropic — 같은 학습, 다른 결론 (p.17)

같은 AI 학습이라도 **데이터를 어떻게 취득했는가**에 따라 공정이용 판단이 갈렸다.

| 공정이용 4요소 | ① LLM 학습을 위한 복제 | ② 구매한 책의 복제(디지털화) | ③ 불법 다운로드 도서 복제(저장) |
|---|---|---|---|
| 제1요소: 이용의 목적과 성격 | 피고 유리 | 피고 유리 | 원고 유리 |
| 제2요소: 원저작물의 성격 | 원고 유리 | 원고 유리 | 원고 유리 |
| 제3요소: 이용된 부분의 양과 중요성 | 피고 유리 | 피고 유리 | 원고 유리 |
| 제4요소: 잠재적 시장·가치에 미치는 영향 | 피고 유리 | 중립 | 원고 유리 |
| **공정이용?** | **O** | **O** | **X** |

> 문제는, **우리가 사용하는 데이터셋이 어디서 온 데이터인지 모른다**는 데 있습니다.

---

## 5. LG AI연구원이 만들고 있는 것 (p.19~)

### 5-1. 빠진 고리를 정의한다 — 데이터셋 계보 (p.19)

대한민국 정부의 **국가 AI-BOM 프로파일 과제**로 수행 중이며, **SPDX 3.0을 수정 없이 확장**.

| 법적 의무 | 문제 | 우리가 정의하는 필드 |
|---|---|---|
| **인공지능 기본법** — 학습에 사용된 데이터의 개요 | **문장은 기록이 아니다** — "공개 웹데이터로 학습함" 식으로는 검증할 수 있는 것이 없다 | **데이터셋 계보** — 문장이 아닌 **그래프**. 기계 판독 가능하고 검증 가능 |

구조: 모델 ← 데이터셋 ← 데이터 소스 1~4 ← 소스 1-1, 1-2… ← 소스 1-2-1… (**더 이상 새로운 소스가 나오지 않을 때까지**)
각 엣지에 담기는 정보: **출처 · 라이선스 · 취득 방법 · 용도**

> 한 나라의 법적 의무를 국제 표준의 언어로 옮겼습니다. 대한민국은 신뢰가 국경을 넘는 첫걸음입니다.

### 5-2. 왜 공급망의 '끝'까지 추적해야 하는가 (p.20)

실제 사례 체인:

**Bibliotik**(비공개 트래커, 시작점) → **Books3**(파생된 도서 컬렉션, 복제) → **The Pile**(이를 포함한 오픈 데이터셋, 재포장) → **RedPajama**(다운스트림 코퍼스, Permissive 라이선스, 재라벨링) → **어떤 모델**(「오픈」데이터로 학습, 전부 상속)

- 중복 제거와 필터링은 데이터를 더 깨끗하게 만들 뿐, **그 출처를 알려주지는 않는다.**
- 모든 단계가 기술적으로는 정당했지만, 최종 모델에 이르렀을 때 진짜 출처는 네 단계 위 데이터셋에 묻혀 상위 라벨에서는 전혀 보이지 않는다.

> **결함은 최종 데이터셋에 있지 않습니다. 아무도 더 이상 들여다보지 않는 그 출발점에 있습니다.**

**왜 이런 체인이 생기는가 (녹취 보강)**
A 개발자가 미국에서 학습데이터를 배포한다 → 지구 반대편 인도의 개발자가 그걸 받아 "이 데이터셋 좋네, 여기에 뉴욕타임스 에디션을 좀 포함시켜 재배포해볼까" 한다 → 이런 식으로 데이터셋이 **합쳐지고, 분할되고, 증류되고, 재배포되는** 현상이 무한히 반복된다.
Bibliotik은 **불법 저작물 도서 유통 사이트**이고, 여기서 스크래핑해 Books3가 만들어졌으며, 그것이 The Pile → RedPajama를 거쳐 최종 모델까지 학습되었다. **Anthropic이 2조 원을 배상하게 된 바로 그 데이터셋 계보다.**

### 5-3. 21%만 살아남았다 (p.22)

스스로 「상업적 이용 가능」이라 밝힌 **2,852개** 데이터셋을 모든 하위 소스까지 추적한 결과:

| 기준 | 결과 |
|---|---|
| 라벨 기준 (최상단이 말한 그대로) | **2,852개** |
| 추적 이후 (공급망을 실제로 따라간 결과) | **605개 (21.2%)** |

리스크 등급: A-1 > A-2 > A-3 (상업적 이용 가능) > B-1 > B-2 (연구 목적 한정) > C-1 > C-2 (이용 불가)

> 이 숫자는 누구도 탓하지 않습니다. **우리가 얼마나 몰랐는지를 보여 줍니다.**
> 우리가 「오픈」이라 부르는 것의 **78.8%는 단 한 번도 그 사슬이 추적된 적이 없습니다.** 배포자도, 사용자도 하지 않았습니다. 그것을 해낼 도구를 만들기 전까지는 우리도 하지 않았습니다.

**FineVision 추적 사례 (녹취 보강)**
개발자들은 "이 데이터셋은 Apache / MIT / CC-BY 4.0으로 배포되어 있으니 써도 문제없겠죠?"라고 법무팀에 묻는다. 그래서 **FineVision이라는 단일 데이터셋 하나를 에이전트로 끝까지 추적**해봤다.

- 그 아래에 **약 3,000개의 서로 다른 라이선스 텀**이 존재
- 그중에는 **"이 데이터를 절대 AI 학습에 사용하지 마세요"**, "non-commercial(비상업) 용도로만 사용 가능" 같은 조건이 다수
- 이미 **소송에 걸려 있거나 판결을 앞둔 위험 데이터셋**도 포함

**개발자들은 출처를 알고 쓰는가? — 아니다**
> 이게 **SNS의 '좋아요'와 같습니다.**

허깅페이스의 *Most Downloaded / Most Liked* 목록이 그 역할을 한다. "이 데이터를 썼더니 성능이 많이 올라간다"는 좋아요가 쌓인 데이터셋이 널리 쓰이고, 출처는 추적되지 않는다. 그래서 위험한 데이터셋인지 — 심지어 **로봇이 사람을 때리게 만드는 악용 데이터가 섞여 있는지** — 전혀 모르는 상태로, **벤치마크 성능에 도움 되는 데이터셋 위주로** 사용·배포되고 있다.

### 5-4. 노력의 문제가 아니라 규모의 문제 (p.24)

데이터셋 하나를 정직하게 검토하려면:
1. 검토 대상 데이터셋 확인
2. 루트 데이터셋의 라이선스 조건 분석
3. 루트 데이터셋 내 모든 하위 소스 발견 (메타데이터 파싱 → 중첩 하위 소스 추출)
4. 개별 하위 소스별 조건 분석
5. 하위의 하위 소스까지 **재귀적으로** 추적
6. 최하위 소스의 조건까지 평가 → 라이선스를 종합해 총체적 리스크 평가 → **AI 데이터 리스크 등급**

> 사람의 속도로는 끝에 닿을 수 없습니다. **게을러서가 아니라, 숫자가 허락하지 않기 때문입니다.**

**규모의 실체 (녹취 보강)**
데이터셋 하나 안에 서로 다른 라이선스 노드가 많은 경우 **1만 8천 개**까지 병존한다. 이걸 전부 수집하고 노드별로 평가해야만 최종 AI 데이터 리스크 등급을 낼 수 있다.

### 5-4b. 그래서 에이전트로 풀었다 (녹취 보강 — 슬라이드에 없던 핵심)

**에이전트가 하는 일**
1. 데이터 카드·데이터셋 메타데이터를 열어 출처 단서를 찾는다
2. 개발자가 **논문·개인 블로그·허깅페이스 페이지에 남긴 단서**를 웹을 돌아다니며 샅샅이 뒤진다 ("어떤 소스를 풀링했다", "보호기간이 만료된 저작물만 썼다", "Bibliotik 데이터셋 일부를 가져왔다" 등)
3. **더 이상 새로운 소스가 나오지 않을 때까지** 재귀적으로 추적
4. 각 소스 노드의 라이선스 텀을 수집해, "사용 가능"인지 "AI 학습 금지 조항이 있는지"를 판단

**결과: 사람 대비 약 45배 빠르고, 더 정확하다.**
> 저 같은 변호사보다 오히려 에이전트가 더 정확하게 소스를 찾고 라이선스 텀을 읽고 판단하는 상황까지 와 있습니다.

**⭐ 다만 자동화한 것은 '판단'이 아니라 '추적'이다**
> 저희는 **판단을 자동화한 게 아니라 추적을 자동화**했고, **인간이 최종 의사결정 권한을 남겨두되** 에이전트의 힘을 빌리지 않으면 도저히 해결할 수 없는 문제를 푸는 방식입니다.

이 체계는 LG AI연구원 내부를 넘어 **LG DX 그룹에도 배포**되었고, **국내 로펌들과 협업**해 복잡하게 트리화된 학습데이터의 평가 기준을 만들고 있다.

### 5-5. 추적의 끝에서 드러나는 것 — UltraFeedback 사례 (p.26)

INPUT: `openbmb/UltraFeedback` (Dataset, Text, **License: MIT**)
14개 기준(데이터 라이선스의 존재, 산출물에 대한 권리, 알려진 분쟁 등)으로 스코어링.

| 평가 | 결과 |
|---|---|
| **Individual Assessment (A-3)** | 상업적 이용 가능 (Low Risk) |
| **Aggregate Assessment (C-2)** | **Common Crawl과 GPT-4를 사용했기 때문에 상업적·내부 이용 모두 불가 (High Risk)** |

의존 체인: UltraFeedback ← GPT-4 / UltraChat / ShareGPT / Evol-Instruct ← ChatGPT Turbo API / C4 Dataset / dolly-15k / Falcon 40B ← Common Crawl / Wikipedia / Databricks employees…
※ 의존 대상의 등급이 파생물보다 낮은 **역전(inversion)** 이 발생하는 지점에서 오류가 드러남.
※ 등급 체계: **A = 안전(상업적 이용 가능) ↔ C = 위험(이용 불가)**

**녹취 설명**: 최상단 노드만 보면 MIT 라이선스로 배포된 오픈소스이므로 처음에는 **A-3(안전)** 으로 평가했다. 그런데 에이전트로 끝까지 추적하니 말단에서 **웹 크롤링·웹 데이터를 무단으로 크롤링한 소스**가 드러났고, 최종 리스크는 **C-2**로 뒤집혔다.

> **법적 리스크는 데이터 라이프사이클 추적을 통해서만 탐지 가능하다.**

### 5-6. 핵심은 증빙가능성 (p.27)

산출물 두 가지:
- **Data Provenance (Dependency List)** — 의존성 목록
- **Data Compliance Results and Report** — 리스크 등급(C-2 / A-1), 점수(예: 2.43/5), 컴플라이언스 체크리스트

> **증빙 가능한 AI-BOM 문서화가 공급망 투명성의 핵심입니다.**

### 5-7. K-AI BOM은 공급망 전체를 따라 이동한다 (p.28)

계보·출처·역할·제약조건이 **모델이 거치는 모든 손을 따라** 전달된다.

| 주체 | 역할 |
|---|---|
| **데이터셋** | 자신의 출처와 계보를 선언한다 |
| **AI 모델** | 이를 상속하고 자신의 기록을 더한다 |
| **서비스** | 모델과 그 기록을 함께 제공한다 |
| **사용자** | 무엇을 실행하고 있는지 검증할 수 있다 |

- **이해관계는 달라도, 근거는 하나** — 네 주체가 원하는 바는 서로 다르지만, 이제는 같은 기록 위에서 각자 스스로 판단하고 결정할 수 있다.
- **하나의 기록, 여러 개의 결정** — 누구도 다른 사람의 판단을 받아들일 필요는 없다. 같은 것을 볼 수 있고, 그다음 스스로 결정할 수 있으면 충분하다.

> LG AI연구원은 기술의 공급자에 그치지 않습니다. **우리 역시 공급망의 참여자입니다.**

**왜 기록해야 하는가 — 로봇 비유 전문 (녹취)**
> 몇 년 후에는 우리 집에도 가사 로봇이 있고 길거리에도 로봇이 걸어 다닐 것 같습니다. **AI 로봇이 나를 때린다면, 나는 누구에게 소송을 걸어야 합니까?**
> AI 배포자인가, 로봇을 만든 사람인가, 아니면 **데이터셋을 무단으로 여러 번 재배포한 사람**인가?
> 공급망에서 학습데이터와 AI 모델이 다음 이해관계자에게 전달될 때 **증빙 가능한 정보가 함께 들어간다면**, 그 판단의 근거가 됩니다.

**K-AI BOM의 현황 (녹취)**
- **SPDX를 차용한 한국형 AI-BOM**으로 개발 중이며, **NIPA 과제**를 통해 수행
- 결과물이 공개되면, 공급망에서 AI 모델의 ① 데이터셋 보안 ② 사람에 대한 리스크 ③ 컴플라이언스 리스크를 판단하려면 **어떤 정보를 입력하고 무엇을 이해관계자에게 전달해야 하는지**의 기준이 된다
- 별도로 **학습데이터를 직접 추적해볼 수 있는 플랫폼**도 제공 중 — 열어보면 "AI가 대체 뭘 먹고 자랐는지 인간이 도저히 이해할 수 없는 세상이 됐구나"를 확인하게 된다
- 목적은 사후 수습이 아니라 **사전 대체(對處)** — 다 만들어놓고 나서 2조 원짜리 데이터셋을 썼다는 걸 알게 되는 상황을 막는 것

---

## 6. 현장 메모 (원문)

- 오픈소스 컴플라이언스는 원래 많이 하던 업무. **AI 시대에는?** → 무슨 데이터를 쓰고 어떻게 학습했는지 잘 추적해야만 한다. 그래서 관련 입법이 많이 진행 중 (**2026년 1월 시행**)
- 기존 SBOM은 **코드 레벨 only**. AI 모델은 학습 후 가중치·파라미터로 작동 → 데이터셋의 구체적 내용을 알 수가 없음
- **증명 가능한 문서화**를 해야 함. AI 개발자가 봐도 원본에는 저장되어 있지 않음
- 모델 개발 이후의 AI 리스크·위해에 대한 분석 → 어떻게? **기반 데이터에서부터** 리스크를 논할 수 있음
- 표준: **SPDX**
- **제3자에게 전달되었을 때의 리스크**가 핵심
- 분쟁은 결국 학습데이터 이슈. **침해가 없었나**가 포인트이고, 원저작자가 증명해야 함 → 판례상 Plaintiff(원저작자) 승소 사례가 다수
- 좋은 비유: **"로봇이 나를 때렸다. 그럼 누구에게 소송을 걸어야 하는가"** — 그것을 가리기 위한 증빙이 AI-BOM

---

## 7. 무신사 세션(오전)과의 대비

| | 무신사 (이현주) | LG AI연구원 |
|---|---|---|
| 관점 | **도입 판단** — 살까 만들까 포기할까 | **공급망 신뢰** — 무엇으로 만들어졌는지 증명 가능한가 |
| 기준을 언제 쓰나 | 시작 전에 '멈출 기준'을 계약서보다 먼저 | 학습 전에 데이터 계보를 그래프로 |
| 공통점 | 둘 다 **"기록되지 않은 것은 판단할 수 없다"** — 사후 논쟁을 없애기 위해 사전에 기준·기록을 문서로 확정 |

**바로 써먹을 5가지**
1. 외부 모델·데이터셋 도입 시 **라벨(MIT, Apache 등)을 그대로 믿지 않는다** — 상위 라벨과 실제 상속 리스크는 다를 수 있음 (2,852 → 605 / FineVision 아래 3,000개 라이선스 / UltraFeedback A-3 → C-2)
2. 벤더 계약서에 **학습 데이터 출처·라이선스·취득 방법 고지** 조항을 넣을 근거 (SPDX 3.0 / OpenChain AI System BOM)
3. 2026년 1월 AI 기본법 시행 대응 — "공개 웹데이터로 학습함" 같은 **문장이 아니라 검증 가능한 기록**을 요구
4. 데이터셋 선택 기준이 **허깅페이스의 다운로드·좋아요 수**가 되고 있지 않은지 점검. 인기 = 안전이 아니다
5. 규모 문제는 **에이전트로 추적을 자동화하되 판단은 사람이** — LG의 방식(45배 속도, 최종 의사결정권은 인간)이 그대로 참고 모델

---

## 8. 🌐 웹 리서치 보강 (2026-09-07 검색 기준)

> 아래는 **발표에 없던 외부 근거 + 발표 내용의 팩트체크**다. 녹취 기반 정리(0~7장)와 섞이지 않도록 분리했다. 번호는 이 장 마지막 「출처」와 연결된다.

### 8-1. 팩트체크 — 발표 수치와 공개 자료의 대조

| 발표/녹취 내용 | 공개 자료로 확인한 것 | 판정 |
|---|---|---|
| "EXAONE 2.0을 Apache 2.0 오픈소스로 출시, **750B 파라미터로 국내 최대**" | LG AI연구원이 **7,500억(750B) 파라미터 'K-EXAONE 2.0'**을 공개, 누구나 **상업적 활용 가능하도록 오픈소스로 전면 개방** [1] | ✅ 맞음. 다만 정식 명칭은 **K-EXAONE 2.0** (국가대표 AI 프로젝트 라인) |
| (배경) EXAONE 4.0 | 전문가 모델 **32B** + 온디바이스 **1.2B** 듀얼 라인업, 허깅페이스 공개. **국내 최초 하이브리드 추론 모델** [2][3] | ✅ 별개 라인업. 750B와 혼동 주의 |
| "국가 AI-BOM 프로파일 과제 / NIPA 과제로 수행" | LG AI연구원은 과기정통부 **독자 AI 파운데이션 모델(독파모)** 사업 1차 평가를 통과해 2차 진출한 3개 팀 중 하나 [4]. 데이터 프로버넌스 기반 **18개 데이터 컴플라이언스 평가 기준**을 수립했고, 이를 AI-BOM과 결합해 데이터 리스크가 모델·서비스로 전파되는 경로를 공급망 수준에서 추적하는 구조 [5] | ✅ 맞음. 다만 발표의 "14개 기준"(UltraFeedback 스코어링)과 공개 자료의 "18개 기준"은 **다른 시점/다른 층위의 숫자**로 보임 — 인용 시 출처를 명시할 것 |
| "Andrea Bartz v. Anthropic 합의금 **약 2조 원**" | **$1.5B(15억 달러)** 합의. 약 50만 건의 저작물 대상, **작품당 약 $3,000**, 해적판 데이터셋 폐기 의무, 120일 옵트아웃 [6][7][8] | ✅ 맞음 (환율 1,330원 가정 시 약 2조 원). 미국 사상 최대 규모 저작권 합의 [8] |
| "GEMA v. OpenAI 독일에서 OpenAI 완패" | 2025-11-11 **뮌헨 지방법원 I**, OpenAI가 독일 저명 아티스트의 저작권을 침해했다고 판결. 부작위·손해배상·정보제공 명령 [9][10][11] | ✅ 맞음 |
| "GEMA v. Suno도 독일에서 연쇄 패소 (2026)" | 이번 검색으로는 **확인하지 못함** | ⚠️ **미검증** — 인용 시 "발표자 언급" 단서를 달 것 |
| "Getty Images v. Stability AI — 피고(AI사) 승" | 2025-11-04 영국 고등법원(Joanna Smith 판사). **2차적 침해 주장 기각** — 모델 가중치가 원저작물을 저장하지 않으므로 '침해 복제물'이 아님. Getty는 **재판 중 학습 과정 침해·산출물 침해 주장을 스스로 철회** [12][13][14] | ✅ 결론은 맞으나, **"AI사가 이겼다"보다 "Getty가 두 개의 핵심 주장을 포기했고 남은 것도 기각됐다"**가 정확 |
| "Thomson Reuters v. ROSS — 원고 승" | 2025-02 델라웨어 연방법원 Bibas 판사, 헤드노트 2,243건에 대해 직접침해 인정 + **공정이용 항변 배척**. AI 학습데이터에 공정이용을 판단한 **미국 최초 판결** [15][16] | ✅ 맞음. **단, 항소 진행 중** — 제3연방항소법원이 2025-06 상고 허가(AI·저작권 사건 최초의 항소심), **2026-07 구두변론** [15][17] |
| "전 세계 약 130~150건 분쟁, 100건 이상 진행 중" | 개별 건수는 이번 검색으로 확인 못 함. 다만 주요 판결이 2025년에만 최소 4건(ROSS·Bartz·Getty·GEMA) 나온 것은 확인됨 | ⚠️ 규모 수치는 발표자 집계로 표기 |

### 8-2. 규제 캘린더 — "무엇을 언제까지 기록해야 하는가"

발표에서 "입법이 몰린다"고 한 부분을 실제 날짜로 고정하면:

| 관할 | 근거 | 시점 | 요구 사항 |
|---|---|---|---|
| **한국** | 인공지능 발전과 신뢰 기반 조성 등에 관한 기본법(AI 기본법) + 시행령 | **2026-01-22 시행** [18][19] | 고영향 AI·생성형 AI 기반이라는 사실의 **사전 고지**, 학습용 데이터 시책 등. **규제 적용은 최소 1년 이상 유예**되며 유예 기간에는 계도 중심 운영, 극히 예외적인 경우에만 사실조사 [18] |
| **EU** | AI Act **제53조 (1)(d)** | 의무 발효 **2025-08-02**, 집행(AI Office 검증·시정) **2026-08-02**부터, 기존 모델은 **2027-08-02**까지 유예 [20][21][22] | AI Office가 배포한 **공식 템플릿**(2025-07-24 공개)으로 학습 콘텐츠 요약 공개. **오픈소스·무료 라이선스 모델도 대상**. 위반 시 **최대 1,500만 유로 또는 전 세계 매출 3%** 중 큰 금액 [20][22] |
| **미국(캘리포니아)** | AB 2013 (Generative AI Training Data Transparency Act) | **2026-01-01 시행** [23][24] | **2022-01-01 이후** 공개된 생성형 AI에 대해 학습 데이터셋 고수준 요약을 **웹사이트에 사전 게시**, 중대 변경 시 갱신. **12개 항목**(데이터 출처·소유자, 데이터 포인트 수, 저작물 포함 여부, 개인정보 포함 여부 등). **영업비밀 보호 규정이 없음** → xAI가 위헌(수정헌법 5조 수용조항) 소송 제기 [23][25] |
| **한국(저작권법)** | TDM 면책 조항 | **미입법** | AI 학습 목적 복제를 조건부 허용하는 개정안이 발의됐으나 **국회 미통과**. 한편 문체부는 **AI 학습에 사용된 데이터 목록 공개 의무**를 포함한 개정을 예고 [26][27] |

**⭐ 여기서 발표의 논지가 강화된다**: EU는 "요약을 공개하라", 캘리포니아는 "출처·소유자·저작물 포함 여부를 12개 항목으로 공개하라"고 한다. 그런데 발표가 보여준 것은 — **UltraFeedback을 끝까지 추적해야 그 답이 A-3이 아니라 C-2라는 걸 알 수 있다**는 사실이다. 즉 **추적 없이는 공시 자체가 부정확한 진술이 된다.** 규제는 "요약"을 요구하지만, 정확한 요약을 쓰려면 계보 그래프가 선행되어야 한다.

**추가 리스크**: 캘리포니아 AB 2013에 영업비밀 예외가 없다는 점 [23]과, 한국·EU·미국의 요구 항목이 서로 다르다는 점이 겹치면, 발표자가 말한 **"글로벌 배포 시 관할마다 리서치해야 한다"**는 부담이 규제 측면에서도 그대로 반복된다.

### 8-3. "라벨을 믿지 마라"에 대한 독립적 근거 — Data Provenance Initiative

LG의 **2,852 → 605 (21.2%)** 는 자체 산출이라 외부 검증이 안 된다. 그런데 **동일한 현상을 다른 팀이 독립적으로 측정한 연구**가 있다.

**Data Provenance Initiative** (MIT 등, 논문 arXiv:2310.16787 / *Nature Machine Intelligence* 게재) [28][29]:

| 측정 항목 | 결과 |
|---|---|
| 감사 대상 | 44개 instruction/alignment 파인튜닝 컬렉션, **1,858개 개별 데이터셋**의 계보 추적 |
| 라이선스 **누락률** | GitHub·허깅페이스 인기 데이터셋의 **70% 이상이 "unspecified"** |
| 라이선스 **오류율** | **50% 이상**. 허깅페이스 라이선스의 **66%가 실제와 다른 이용 카테고리**로 표기 |
| 오류의 방향 | 대부분 **원저자의 실제 라이선스보다 더 관대(permissive)하게** 표기됨 |
| 개선 결과 | 미지정 라이선스를 72% → **30%**로 낮추고 라이선스 URL을 부착. Data Provenance Explorer 공개 |

**⭐ 이게 왜 결정적인가**: "허깅페이스 라벨이 실제보다 **관대한 쪽으로** 틀린다"는 건, 발표의 UltraFeedback 사례(MIT라 적혀 있으나 실제는 C-2)가 **예외가 아니라 구조적 패턴**임을 뜻한다. LG의 21.2%와 DPI의 66% 오분류는 서로 다른 방법론으로 같은 방향을 가리킨다.

### 8-4. AI-BOM 표준의 현재 위치

발표가 "명세서에는 이미 자리가 마련되어 있다"고 한 그 자리:

- **SPDX 3.0**은 **2024-04-16 정식 릴리스**되었고, **AI Profile**과 **Dataset Profile**을 분리해 담았다 [30][31]
- 산업계·학계 워킹그룹이 모델 카드·데이터시트·팩트시트를 분석해 두 프로파일에 걸쳐 **36개 필드**를 선정 [30][31]
- AI Profile = 알고리즘·신경망 등 AI 기능 관련 구성요소 / Dataset Profile = 데이터 처리·저장·관리 구성요소. **프로파일을 분리한 덕에 모델의 출처·학습 방법과 데이터셋의 특성·한계를 각각 정밀하게 문서화**할 수 있다 [31]
- 이 프레임워크는 **EU AI Act, FDA 의료기기 규제 등 규제 요건에 매핑**되도록 설계되었고, 기존 SPDX 툴체인과 호환된다 [30][31]
- Linux Foundation Research가 실무 가이드(`Implementing AI Bill of Materials (AI BOM) with SPDX 3.0`)를 공개 [32][33]

**즉 발표의 표현은 정확하다** — 스펙에는 데이터셋 계보를 담을 필드가 이미 있다. 없는 것은 **그 필드를 채울 데이터**이고, LG가 만든 것은 표준이 아니라 **그 필드를 채우는 에이전트**다.

**다만 짚어둘 한계**: SPDX 3.0의 Dataset Profile은 "이 데이터셋이 무엇인가"를 기술하는 데는 충분하지만, **"이 데이터셋이 어디서 왔는가"를 재귀적으로 강제하지는 않는다.** 발표에서 "데이터셋 계보는 선택 항목이라 채워지지 않는다"고 한 지점이 정확히 여기다. LG의 한국형 프로파일 확장이 노리는 빈칸도 이것이다.

### 8-5. Bartz 판결의 4요소 표를 다시 읽기

발표 슬라이드 p.17의 표(① 학습 복제 ○ / ② 구매서적 디지털화 ○ / ③ 불법 다운로드 보관 ✗)는 공개 자료와 정확히 일치한다:

> Alsup 판사는 **적법하게 취득한 책으로 AI를 학습시키는 것은 공정이용**이라고 약식판결했으나, **해적 사이트에서 내려받아 중앙 라이브러리에 보관한 부분에 대해서는 공정이용을 인정하지 않았다.** Anthropic은 Books3·LibGen·PiLiMi 등에서 **700만 권 이상**의 전문(full-text) 도서를 내려받은 것으로 나타났다. [6][7][8]

**⭐ 발표의 핵심 논지가 여기서 완성된다**: 판결을 가른 것은 *무엇을 학습했는가*가 아니라 **어떻게 취득했는가**다. 그리고 취득 방법은 **모델 가중치에도, 소스코드에도, 최종 데이터셋 라벨에도 남지 않는다.** 오직 계보 기록에만 남는다. 발표에서 든 체인 — Bibliotik → Books3 → The Pile → RedPajama → 최종 모델 — 이 바로 그 $1.5B의 경로다.

### 8-6. 이 세션에서 실제로 훔쳐올 것 (보강판)

1. **라벨을 그대로 믿지 않는다** — 근거가 LG 하나가 아니다. DPI 감사: 허깅페이스 라이선스의 **66%가 오분류**, 그것도 **더 관대한 쪽으로** [28][29]
2. **벤더 계약에 학습데이터 출처·라이선스·취득 방법 고지 조항** — 표준 언어로 **SPDX 3.0 AI/Dataset Profile(36개 필드)** 을 지목하면 협상이 쉬워진다 [30][31]
3. **규제 캘린더를 데드라인으로 관리** — 한국 2026-01-22(유예 1년+), EU 집행 2026-08-02, 캘리포니아 2026-01-01. **오픈소스로 배포해도 EU 의무는 면제되지 않는다** [20][22][23]
4. **"인기 = 안전"이 아니다** — 허깅페이스의 Most Downloaded/Most Liked는 벤치마크 성능 신호이지 법적 안전 신호가 아니다. DPI가 측정한 오류율이 그 증거다
5. **추적은 자동화하되 판단은 사람이** — LG의 방식(에이전트로 재귀 추적, 사람 약 45배 대비 속도, 최종 의사결정권은 인간). 참고로 **판단까지 자동화하면 그 판단 자체가 새로운 미기록 리스크**가 된다
6. **(추가) 취득 방법을 기록 항목으로 승격** — Bartz가 증명한 것은 학습 여부가 아니라 **취득 경로가 손해배상의 크기를 정한다**는 것. 데이터 수집 파이프라인에 "어디서, 어떤 권한으로 받았는가"를 남기는 로깅이 사후 방어의 유일한 증거다

---

### 출처

[1] [LG AI연구원, 7500억개 파라미터 'K-엑사원 2.0' 공개…오픈소스로 전면 개방 — 천지일보](https://www.newscj.com/news/articleView.html?idxno=3421513)
[2] [차세대 하이브리드 AI, EXAONE 4.0 공개 — LG AI Research Blog](https://www.lgresearch.ai/blog/view?seq=575)
[3] [Unveiling EXAONE 4.0, the next generation of hybrid AI — LG AI Research Blog](https://www.lgresearch.ai/blog/view?seq=576)
[4] [대한민국 '독자 AI 파운데이션 모델' 1차 평가 결과 발표 — 인공지능신문](https://www.aitimes.kr/news/articleView.html?idxno=38163)
[5] [AI 거버넌스의 패러다임 변화와 LG AI연구원의 선도적 역할 — OSS(공개SW포털)](https://www.oss.kr/pages/11/4418)
[6] [What to Know About the $1.5 Billion Bartz v. Anthropic Settlement — Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)
[7] [Bartz v. Anthropic Settlement: What Authors Need to Know — The Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)
[8] [The Bartz v. Anthropic Settlement: Understanding America's Largest Copyright Settlement — Kluwer Copyright Blog](https://legalblogs.wolterskluwer.com/copyright-blog/the-bartz-v-anthropic-settlement-understanding-americas-largest-copyright-settlement/)
[9] [GEMA vs. OpenAI: Landmark ruling on AI language models and copyright law — Heuking](https://www.heuking.de/en/news-events/newsletter-articles/detail/gema-vs-openai-landmark-ruling-on-ai-language-models-and-copyright-law.html)
[10] [Landmark ruling of the Munich Regional Court (GEMA v OpenAI) — Bird & Bird](https://www.twobirds.com/en/insights/2025/landmark-ruling-of-the-munich-regional-court-(gema-v-openai))
[11] [German court rules in favour of music rights management organisation against OpenAI — EU IP Helpdesk](https://intellectual-property-helpdesk.ec.europa.eu/news-events/news/german-court-rules-favour-music-rights-management-organisation-against-openai-nyt-vs-openai-dispute-2025-11-14_en)
[12] [Stability AI defeats Getty Images copyright claims in first of its kind dispute — Bird & Bird](https://www.twobirds.com/en/insights/2025/uk/stability-ai-defeats-getty-images-copyright-claims-in-first-of-its-kind-dispute-before-the-high-cour)
[13] [Getty Images v. Stability AI: English High Court Rejects Secondary Copyright Claim — Latham & Watkins](https://www.lw.com/en/insights/getty-images-v-stability-ai-english-high-court-rejects-secondary-copyright-claim)
[14] [Getty Images v Stability AI: What the High Court's Decision Means — Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/11/getty-images-v-stability-ai-what-the-high-courts-decision-means-for-rights-holders-and-ai-developers)
[15] [Thomson Reuters v. ROSS Intelligence at the Third Circuit — Legal AI](https://legalai.substack.com/p/thomson-reuters-v-ross-at-the-third)
[16] [Court Decides that Use of Copyrighted Works in AI Training Is Not Fair Use — Jenner & Block](https://www.jenner.com/en/news-insights/client-alerts/court-decides-that-use-of-copyrighted-works-in-ai-training-is-not-fair-use-thomson-reuters-enterprise-centre-gmbh-v-ross-intelligence-inc)
[17] [Third Circuit Hears Oral Argument in Ross v. Reuters AI Training Copyright Case — Baker Botts](https://www.bakerbotts.com/thought-leadership/publications/2026/july/third-circuit-hears-oral-argument)
[18] [AI 기본법 시행과 그 시사점 — 법률신문 / 법무법인 세종](https://www.lawtimes.co.kr/news/articleView.html?idxno=216500)
[19] [인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 — 국가법령정보센터](https://www.law.go.kr/lsInfoP.do?lsiSeq=268543)
[20] [European Commission Releases Mandatory Template for Public Disclosure of AI Training Data — WilmerHale](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/european-commission-releases-mandatory-template-for-public-disclosure-of-ai-training-data)
[21] [EU AI Act News: Rules on General-Purpose AI Start Applying — Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/08/eu-ai-act-news-rules-on-general-purpose-ai-start-applying-guidelines-and-template-for-summary-of-training-data)
[22] [EU Commission Publishes Guidelines on General Purpose AI Obligations — Paul, Weiss](https://www.paulweiss.com/insights/client-memos/eu-commission-publishes-guidelines-on-general-purpose-ai-obligations-as-well-as-training-data-disclosure-template-further-clarity-as-the-countdown-to-enforcement-begins)
[23] [California's AB 2013 Takes Effect: Navigating AI Training Data Transparency and Trade Secret Risk — Goodwin](https://www.goodwinlaw.com/en/insights/publications/2026/01/alerts-otherindustries-californias-ab-2013-takes-effect)
[24] [Generative AI Training Data Transparency Act (AB 2013) — California Legislative Information](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240AB2013)
[25] [California's AB 2013 Requires Generative AI Data Disclosure by January 1, 2026 — Crowell & Moring](https://www.crowell.com/en/insights/client-alerts/californias-ab-2013-requires-generative-ai-data-disclosure-by-january-1-2026)
[26] [AI 학습데이터 저작권 침해와 저작권법 상의 TDM 조항 도입 논의 — NEPLA](https://www.nepla.ai/wiki/%EC%A7%80%EC%8B%9D%EC%9E%AC%EC%82%B0/%EC%A0%80%EC%9E%91%EA%B6%8C/ai-%ED%95%99%EC%8A%B5%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%A0%80%EC%9E%91%EA%B6%8C-%EC%B9%A8%ED%95%B4%EC%99%80-%EC%A0%80%EC%9E%91%EA%B6%8C%EB%B2%95-%EC%83%81%EC%9D%98-tdm-%EC%A1%B0%ED%95%AD-%EB%8F%84%EC%9E%85-%EB%85%BC%EC%9D%98-zr592w2dv96k)
[27] [저작권법상 텍스트·데이터 마이닝(TDM) 면책규정 도입 방향의 검토 — 류시원, 법무부](https://www.moj.go.kr/bbs/moj/166/450511/download.do)
[28] [The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI (arXiv:2310.16787)](https://arxiv.org/pdf/2310.16787)
[29] [A large-scale audit of dataset licensing and attribution in AI — Nature Machine Intelligence](https://www.nature.com/articles/s42256-024-00878-8)
[30] [Implementing AI Bill of Materials (AI BOM) with SPDX 3.0 — Linux Foundation Research (PDF)](https://www.linuxfoundation.org/hubfs/LF%20Research/lfr_spdx_aibom_102524a.pdf)
[31] [Implementing AI Bill of Materials (AI BOM) with SPDX 3.0 — 논문 개요 (alphaXiv 2504.16743)](https://www.alphaxiv.org/overview/2504.16743v1)
[32] [Implementing an AI BOM — SPDX](https://spdx.dev/implementing-an-ai-bom/)
[33] [From SBOMs to AI BOMs: Why SPDX 3.0 Matters — Sonatype](https://www.sonatype.com/blog/from-sboms-to-ai-boms-why-spdx-3.0-matters)

---

## 9. 📎 배포용 슬라이드(PDF) 대조 — `Closing_Keynote_2_LG_AI.pdf` (29p)

### 9-1. ✅ 발표자·소속 확정

| 항목 | 확정 정보 |
|---|---|
| 발표자 | **조정원 — Legal & Compliance Team Lead, LG AI연구원** |
| 덱 제목 | **「AI 학습데이터의 국내외 분쟁 동향과 추적가능 컴플라이언스」** |
| 부제 | **AI-BOM 기반 데이터 공급망 관리** |
| 클로징 문구 | *"We must open up not just the technology itself, but the hidden risks within it."* |

**조직 정의 (p.2)** — 노트에 없던 자기 규정:
> LG AI연구원은 **2020년 12월 설립**된 LG그룹의 AI 싱크탱크. Legal & Compliance 조직은 법률·규제 이슈에 대응하는 데 그치지 않고, **그 과정에서 축적한 기준과 노하우를 AI 기반 솔루션으로 구현해 외부로 확장하는 「Scalable Compliance」를 실행**한다.

→ 이 문장이 발표 전체의 성격을 규정한다. 법무팀이 만든 **제품** 이야기다.

### 9-2. EXAONE 5년 타임라인 (p.4) — 노트를 정정·확장

노트에는 "EXAONE 1.0을 2021년 12월 시작, EXAONE 2.0을 Apache 2.0으로 출시, 750B"로 뭉뚱그려져 있으나, 덱의 실제 타임라인은 다음과 같다.

| 모델 | 시점 | 특징 |
|---|---|---|
| EXAONE 1.0 | 2021.12 | 한국어·영어를 함께 이해하는 이중언어 모델 |
| EXAONE 2.0 | 2023.7 | 전문성·신뢰성·비용 효율성을 크게 높인 모델 |
| EXAONE 3.0 | 2024.8 | **7.8B 인스트럭션 튜닝 언어모델을 일반에 공개** |
| EXAONE 3.5 | 2024.12 | 긴 문맥 이해와 지시 수행 능력 |
| EXAONE Deep | 2025.3 | 수학·과학·코딩 추론 |
| EXAONE 4.0 | — | 언어와 추론을 통합한 **하이브리드 AI 모델** |
| **EXAONE 4.5** | 2026 | **LG 최초의 오픈 웨이트 비전-언어(VLM) 모델** |
| **K-EXAONE 2.0** | 2025.8 | **750B 프론티어급 멀티모달**, **Apache 2.0 오픈소스**, 독자 기술로 구축한 대한민국 대표 AI |

**추가 성과 표기**: Epoch AI의 *Notable AI Models* 등재, **대한민국 독자 파운데이션 모델 1차 평가 종합 1위 / 2차 평가 Top 3**

> **덱의 핵심 문장**: "모델을 만드는 법은 알지만, **그 투명성을 증명하는 법은 찾아 나가고 있습니다.**"

※ 노트 8-1의 팩트체크 표에서 "EXAONE 2.0 = 750B"로 읽힐 소지가 있었던 부분은 이 표로 정정된다. **750B는 K-EXAONE 2.0**이고, EXAONE 2.0(2023.7)은 별개다.

### 9-3. 덱에만 있고 노트에 없던 슬라이드

**① "세계는 이미 그 질문을 시작했습니다" (p.18)** — 세 주체가 같은 질문을 한다

| 주체 | 묻는 방식 |
|---|---|
| **법원** | "이 자료는 어디서 왔고, 누가 그 사용을 허락했는가?" — Bartz는 **책을 어떻게 취득했는지**를, Getty는 **복제가 어디서 일어났는지**를 물었다 |
| **규제기관** | "시스템이 무엇으로 학습되었는지 **요약을 공개하라**" — 캘리포니아 AB 2013은 **2026년 1월부터 시행 중**이고, 유사 의무가 다른 나라에도 도입되고 있다 |
| **고객** | "우리가 도입하는 모델 안에 무엇이 들어 있는지 보여 줄 수 있습니까?" — **구매 부서는 이제 SBOM을 요구하듯 데이터 출처를 요구**한다 |

→ **팀 공유 시 가장 설득력 있는 한 장.** AI-BOM이 법무 이슈가 아니라 **구매·영업 이슈**이기도 함을 보여준다.

**② 에이전트 성능 수치의 정확한 표현 (p.25)** — 노트를 정정

| 노트 표현 | 덱의 정확한 표현 |
|---|---|
| "사람 대비 약 45배 빠르고, 더 정확하다" | **수작업 대비 45배 더 빠르게**, **전문가 대비 26% 더 정확하게** |

에이전트의 3단계도 덱에서 명확해진다:
1. **읽기** — 데이터셋 카드를 열어 선언된 모든 소스를 추출
2. **추적** — 각 소스를 따라가며 **아래에 아무것도 남지 않을 때까지 재귀**
3. **평가** — 맨 위가 아니라 **공급망 전체를 평가**

> "우리는 **판단을 자동화한 것이 아닙니다. 추적하는 일을 자동화했을 뿐이고, 그것은 애초에 판단이 아니었습니다.**"

**③ FineVision 슬라이드가 별도 페이지로 존재 (p.21)**
> "「FineVision」은 **단 하나의 라이선스를 선언**합니다. 그러나 끝까지 추적하면 저마다 다른 조건을 지닌 **3,000개가 넘는 소스**가 나옵니다."

**④ 리스크 등급 분포 (p.22)** — 라벨 기준 vs 추적 이후로 A-1~C-2 7단계 분포가 막대로 제시됨. (PDF 텍스트 추출에서 두 계열의 숫자가 뒤섞여 나오므로, 인용 시 **원본 슬라이드 이미지를 직접 확인**할 것. 확실한 것은 총계 **2,852 → 605(21.2%)** 뿐이다.)

### 9-4. 노트(녹취)에만 있고 덱에는 없는 것

- 분쟁 규모 **약 130~150건 / 100건 이상 진행 중** (발표자 집계)
- **Bartz 합의금 약 2조 원**의 결정적 원인 = 오픈 데이터셋에 포함된 불법 복제본 다운로드분
- **UltraFeedback 사례** (A-3 → C-2 역전) 및 **14개 스코어링 기준**
- 데이터셋 하나에 라이선스 노드가 **최대 1만 8천 개**까지 병존
- **LG DX 그룹 배포 / 국내 로펌 협업 / NIPA 과제 / 학습데이터 추적 플랫폼 제공**
- 로봇 비유 전문 — "AI 로봇이 나를 때린다면 나는 누구에게 소송을 걸어야 합니까?"
- 허깅페이스 **Most Downloaded / Most Liked = SNS의 좋아요**라는 비유
