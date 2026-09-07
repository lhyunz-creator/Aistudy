# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/home/user/Aistudy/tools")
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx_helpers import (ACCENT, MUTED, WARN, add_page_number_footer, bullet,
                          callout, cover, hr, new_document, numbered, page_break,
                          para, rich, table)

doc = new_document()
add_page_number_footer(doc, "AI Infrastructure & Data 2026 · LG AI연구원 세션 정리")

# ────────────────────────────── 표지
cover(
    doc,
    "AI Infrastructure & Data 2026 · Closing Keynote 2 · 세션 정리",
    "AI 학습데이터의 국내외 분쟁 동향과 추적가능 컴플라이언스",
    ["AI-BOM 기반 데이터 공급망 관리",
     "We must open up not just the technology itself, but the hidden risks within it."],
    [
        ["행사", "AI Infrastructure & Data 2026 (CIO Korea / ITWORLD)"],
        ["일시·장소", "2026년 9월 2일(수) · 서울 드래곤시티 그랜드볼룸 한라(3F)"],
        ["발표", "조정원 — Legal & Compliance Team Lead, LG AI연구원"],
        ["첨부 자료", "Closing_Keynote_2_LG_AI.pdf (29페이지)"],
        ["정리 범위", "배포 슬라이드 + 발표 현장 녹취 + 외부 웹 리서치(2026-09-07 기준)"],
    ],
)

para(doc, "한 줄 요약", size=11, bold=True, color=ACCENT, space_before=10, space_after=4)
callout(doc, "신뢰는 한 번도 맹목적인 믿음이었던 적이 없습니다. 언제나 「보이는가」의 문제였습니다.",
        size=12.5, bold=True)
para(doc, "SBOM이 코드의 투명성을 풀었듯, AI-BOM은 학습 데이터의 계보를 풀어야 한다. "
          "그런데 AI 구성요소 세 가지(베이스 모델 아키텍처 / 파라미터·가중치 / 학습 데이터셋) 중 "
          "두 가지는 코드에 아무 흔적도 남기지 않는다.")

hr(doc)
rich(doc, [("이 문서를 읽는 법  ", {"b": True, "size": 10, "color": ACCENT}),
           ("1~5장은 발표 내용, 6장은 외부 근거로 붙인 맥락과 팩트체크, 7장은 우리 팀 체크리스트와 "
            "규제 데드라인, 8장은 인용 시 주의사항입니다. ", {"size": 9.5}),
           ("판례·규제 일정은 모두 1차 자료로 교차 검증했고, 검증하지 못한 항목은 8장에 따로 적었습니다.",
            {"size": 9.5, "b": True, "color": WARN})],
     space_after=4)

page_break(doc)

# ────────────────────────────── 0. 발표사
doc.add_heading("0. 발표 조직 — 법무팀이 만든 제품 이야기", level=1)
callout(doc, "LG AI연구원은 2020년 12월 설립된 LG그룹의 AI 싱크탱크. Legal & Compliance 조직은 "
             "법률·규제 이슈에 대응하는 데 그치지 않고, 그 과정에서 축적한 기준과 노하우를 "
             "AI 기반 솔루션으로 구현해 외부로 확장하는 「Scalable Compliance」를 실행한다.")
para(doc, "→ 이 한 문단이 발표 전체의 성격을 규정한다. 법무 리스크 브리핑이 아니라, "
          "법무팀이 만든 제품에 대한 발표다.", size=9.5, color=MUTED)

doc.add_heading("0-1. 지난 5년의 모델, 그리고 아직 못 푼 것", level=2)
table(doc, ["모델", "시점", "특징"], [
    ["EXAONE 1.0", "2021.12", "한국어와 영어를 함께 이해하는 이중언어 모델"],
    ["EXAONE 2.0", "2023.7", "전문성·신뢰성·비용 효율성을 크게 높인 모델"],
    ["EXAONE 3.0", "2024.8", "**7.8B 인스트럭션 튜닝 언어모델을 일반에 공개**"],
    ["EXAONE 3.5", "2024.12", "긴 문맥 이해와 지시 수행 능력이 뛰어난 모델"],
    ["EXAONE Deep", "2025.3", "수학·과학·코딩에서 강력한 추론 능력"],
    ["EXAONE 4.0", "—", "언어와 추론을 통합한 하이브리드 AI 모델"],
    ["EXAONE 4.5", "2026", "**LG 최초의 오픈 웨이트 비전-언어(VLM) 모델**"],
    ["**K-EXAONE 2.0**", "2025.8", "**750B 프론티어급 멀티모달 · Apache 2.0 오픈소스 · "
                                  "독자 기술로 구축한 대한민국 대표 AI**"],
], widths=[3.5, 2.5, 11.0], first_col_bold=True)
para(doc, "추가 성과 — Epoch AI의 Notable AI Models 등재, 대한민국 독자 파운데이션 모델 "
          "1차 평가 종합 1위 / 2차 평가 Top 3.", size=9.5, color=MUTED)
callout(doc, "모델을 만드는 법은 알지만, 그 투명성을 증명하는 법은 찾아 나가고 있습니다.",
        bold=True, size=11)

# ────────────────────────────── 1. 왜 AI-BOM인가
doc.add_heading("1. 왜 AI-BOM인가 — 공급망이 단절되지 않게 어떻게 지킬 것인가", level=1)
table(doc, ["시대", "명세서", "무엇을 보장하나"], [
    ["하드웨어의 시대", "부품 명세서 (BOM)", "제조 공급망 투명성 + 제품 구성요소 추적성"],
    ["소프트웨어의 시대", "소프트웨어 명세서 (SBOM)", "소프트웨어 공급망 투명성 + 의존성·라이선스 추적성"],
    ["**인공지능의 시대**", "**AI 명세서 (AI-BOM)**", "**AI의 투명성은 어떻게 추적할 것인가?**"],
], widths=[3.5, 5.0, 8.5])
callout(doc, "블랙박스인 AI의 투명성은 어떻게 보장할 수 있을까요? "
             "지금의 SBOM 도구로 그 상자를 열 수 있을까요?")
para(doc, "EU AI Act, 한국 AI 기본법 등은 공통적으로 「AI를 어떻게 만들고 무슨 데이터를 썼는지 기록하라」고 "
          "요구한다. 왜 기록하라고 했는가를 끝까지 따라가면 이 질문에 닿는다:")
callout(doc, "AI가 로봇에 탑재되어 사람에게 위해를 가했을 때, 대체 무엇 때문에 이 문제가 발생했는가?",
        bold=True, fill="FDF3E7", bar="B0302E")
para(doc, "한국은 2026년 1월 AI 기본법 발효. 발효 이후 각 기업에서 — LG 그룹 내부에서도 — 상당한 혼란이 "
          "있었고, 그 해결책으로 AI-BOM을 만들고 있다.")

# ────────────────────────────── 2. 왜 SBOM으로는 안 되는가
doc.add_heading("2. 왜 SBOM 도구로는 안 되는가", level=1)
table(doc, ["구분", "소프트웨어", "AI"], [
    ["동작 방식", "개발자가 정의한 로직 그대로 동작 (입력 → 출력)",
     "학습한 패턴을 바탕으로 **확률적으로** 결과 생성 (입력 → 출력 1/2/3)"],
    ["스캔 결과", "`source_code.py`의 `import flask` → 스캐너 탐지: flask 3.1.0, BSD-3-Clause",
     "`train.py`의 `load_model('weights.h5')`, `load_dataset(\"./corpus/\")` → "
     "**스캐너에는 파일 이름만 보인다**"],
    ["결론", "위험이 특정 코드 라인에 분명히 드러남 → **소스코드로 추적 가능**",
     "어떤 코드 한 줄로도 위험을 알아낼 수 없음 → **소스코드로는 추적 불가**"],
], widths=[2.5, 7.0, 7.5], first_col_bold=True)

doc.add_heading("2-1. AI-BOM이 반드시 해결해야 할 세 가지", level=2)
table(doc, ["구성요소", "SBOM 스캐너로 잡히나"], [
    ["베이스 모델 아키텍처", "**가능** — SBOM 스캐너가 찾아낼 수 있는 유일한 항목"],
    ["모델 파라미터 및 가중치", "**불가능**"],
    ["학습 데이터셋", "**불가능**"],
], widths=[6.0, 11.0], first_col_bold=True)
callout(doc, "세 가지 중 두 가지는 코드에 아무 흔적도 남기지 않습니다. "
             "그럼에도 AI BOM은 이를 기록해야 합니다.", bold=True)

doc.add_heading("2-2. 이미 한 번 풀어낸 문제, 구성요소만 바뀌었다", level=2)
table(doc, ["질문", "소프트웨어 (SBOM)", "AI (AI-BOM)"], [
    ["구성요소는 무엇인가", "패키지, 라이브러리, 버전", "데이터셋, 모델, 가중치"],
    ["누가 선언하는가", "빌드 시스템이 자동으로 선언", "**아무도 하지 않는다**"],
    ["얼마나 깊은가", "해석 가능하고, 대체로 깊지 않다", "**끝없이 깊고, 해석이 어렵다**"],
    ["무슨 질문에 답하는가", "이 바이너리 안에 무엇이 있는가?", "이 모델 안에 무엇이 있는가?"],
    ["표준", "SPDX — 리눅스재단 · ISO/IEC 5962", "**SPDX 3.0 & OpenChain AI System BOM** — 리눅스재단"],
], widths=[4.0, 6.5, 6.5], first_col_bold=True)
callout(doc, "명세서에는 이미 그 자리가 마련되어 있습니다. 그 자리를 채울 방법이 없을 뿐입니다.",
        bold=True)

page_break(doc)

# ────────────────────────────── 3. 투명성은 연결 속에
doc.add_heading("3. 투명성은 「연결」 속에 있다", level=1)
table(doc, ["#", "항목", "질문"], [
    ["1", "모델 출처", "이 모델을 처음부터 직접 만들었는가? 사전학습된 파운데이션 모델을 "
                      "파인튜닝하거나 파생된 것인가?"],
    ["2", "학습 데이터 계보", "학습에 정확히 어떤 데이터셋을 사용했는가?"],
    ["3", "데이터셋 출처", "이 데이터는 어디서 비롯되었고, **적법하게 확보되었는가?**"],
], widths=[1.2, 3.8, 12.0])
para(doc, "베이스 모델 알고리즘 → 모델 파라미터·가중치 → 학습 데이터셋 → 데이터 출처(복수)",
     bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_heading("3-1. 모델은 형태를 남기지만, 데이터는 남기지 않는다", level=2)
table(doc, ["계보", "상태"], [
    ["**모델 계보** — 「이 모델은 저 모델에서 파생되었다」", "표현 가능하고, 구조화되며, **기록으로 남는다**"],
    ["**데이터셋 계보** — 「이 데이터셋은… 어디서 왔는가?」",
     "**선택 항목.** 그래서 요구되지 않고, 채워지지 않고, 존재하지 않는다"],
], widths=[7.5, 9.5])
callout(doc, "모델도 중요합니다. 하지만 우리가 여전히 볼 수 없는 쪽은 데이터입니다.", bold=True)

# ────────────────────────────── 4. 법적 리스크
doc.add_heading("4. 법적 리스크는 이미 현실이다", level=1)
para(doc, "현재 시점 기준 전 세계 약 130~150건의 AI 학습데이터 관련 분쟁이 존재하고 100건 이상이 진행 중이라는 것이 "
          "발표자의 집계다. 쟁점은 ① 저작권 침해가 있었는가 ② 개인정보보호법 침해가 있었는가로 모인다. "
          "미국은 연방 차원의 통일된 개인정보보호법이 없어, 대부분 원저작물의 권리자가 AI 회사를 상대로 "
          "손해배상 청구 + 금지명령을 구하는 구조로 간다.")

doc.add_heading("4-1. 학습데이터 관련 주요 판례 (2024~)", level=2)
table(doc, ["사건", "국가", "년도", "승소", "법적 배경"], [
    ["Li v. Liu", "중국", "2024", "원고", "저작권법"],
    ["Sin Changhwa Cultural Development LLC v. AI Company", "중국", "2024", "원고", "저작권법"],
    ["Thomson Reuters v. ROSS Intelligence", "미국", "2025", "원고", "저작권법 (공정이용)"],
    ["Andrea Bartz v. Anthropic", "미국", "2025", "원고", "저작권법 (공정이용)"],
    ["Kadrey v. Meta", "미국", "2025", "**피고(AI사)**", "저작권법 (공정이용)"],
    ["Getty Images v. Stability AI", "영국", "2025", "**피고(AI사)**", "저작권법"],
    ["GEMA v. OpenAI", "독일", "2025", "원고", "저작권법"],
    ["GEMA v. Suno", "독일", "2026", "원고", "저작권법 (미·독)"],
], widths=[7.0, 2.0, 1.6, 2.4, 4.0])

doc.add_heading("4-2. 오픈소스 컴플라이언스와의 성숙도 격차", level=2)
table(doc, ["영역", "축적된 역사"], [
    ["**Open Source**", "AFPA v. Edu4 → SCO v. IBM($1B, 2003) → BusyBox(2007) → Jacobsen v. Katzer(2008) "
                        "→ Google v. Oracle(2018) → 현재. **20년 넘게 다듬어져 준비되어 있음**"],
    ["**Open Data**", "Getty Image v. Stable Diffusion(2023) → 중국 2건(2024) → Thomson Reuters v. ROSS / "
                      "Bartz v. Anthropic / GEMA v. OpenAI(2025) → 현재. **아직 준비되지 않음**"],
], widths=[3.0, 14.0])
table(doc, ["Source Code", "AI Training Data"], [
    ["형태: 코드", "형태: 코드, 텍스트, 이미지, 영상, 오디오 등"],
    ["이용 목적: 소프트웨어 개발", "이용 목적: **본래 저작물의 목적과 다른 목적**"],
    ["컴플라이언스: 표준화되어 준수됨", "컴플라이언스: **표준화되지 않음**"],
    ["고지의 의무: 표준화되어 준수됨", "고지의 의무: **표준화되지 않음**"],
    ["Source Code → compile → Software", "**Data + Source Code → train → AI Model** "
                                         "(데이터가 결과물의 일부가 된다)"],
], widths=[8.5, 8.5])

doc.add_heading("4-3. 국가별 면책 규정 — 파편화", level=2)
table(doc, ["국가", "항변 근거", "핵심 조항"], [
    ["미국", "Fair Use", "17 U.S.C. § 107 (4요소 형량)"],
    ["한국", "공정이용", "저작권법 제35조의5"],
    ["EU", "TDM 예외", "DSM Directive Arts. 3 & 4"],
    ["일본", "정보분석 예외", "저작권법 제30조의4"],
    ["싱가포르", "전산데이터분석(CDA) 예외", "Copyright Act 2021 §§ 243–244"],
    ["영국", "Fair Dealing", "CDPA 1988 §§ 29–30"],
], widths=[2.5, 5.5, 9.0], first_col_bold=True)
callout(doc, "국가별로 저작권법상의 면책은 파편화되고 있고, 예측 가능성은 줄어들고 있습니다.", bold=True)
bullet(doc, "한국의 공정이용 조항은 2012년 한미 FTA 당시 미국 저작권법의 공정이용 범위를 거의 그대로 차용한 것.")
bullet(doc, "문제는 글로벌 배포. 모델을 허깅페이스에 올리면 지구 반대편까지 도달하는데, "
            "그 국가의 저작권법은 어떤지, 항변 근거는 무엇인지를 매번 리서치해야 한다. "
            "파편화가 심해질수록 기업 내부 컴플라이언스 체계에 소모되는 에너지가 급증한다.")
bullet(doc, "고객 요구도 실재한다 — AI 모델을 제3자·고객사에 제공할 때 "
            "「학습데이터를 뭘로 썼는지 공개해 달라」는 요청이 그룹사 포함해 꽤 들어온다.")

doc.add_heading("4-4. Andrea Bartz v. Anthropic — 같은 학습, 다른 결론", level=2)
para(doc, "같은 AI 학습이라도 데이터를 어떻게 취득했는가에 따라 공정이용 판단이 갈렸다.")
table(doc, ["공정이용 4요소", "① LLM 학습을 위한 복제", "② 구매한 책의 디지털화", "③ 불법 다운로드 도서 저장"], [
    ["제1요소: 이용의 목적과 성격", "피고 유리", "피고 유리", "원고 유리"],
    ["제2요소: 원저작물의 성격", "원고 유리", "원고 유리", "원고 유리"],
    ["제3요소: 이용된 부분의 양과 중요성", "피고 유리", "피고 유리", "원고 유리"],
    ["제4요소: 잠재적 시장·가치에 미치는 영향", "피고 유리", "중립", "원고 유리"],
    ["**공정이용?**", "**인정 O**", "**인정 O**", "**부정 X**"],
], widths=[6.0, 3.7, 3.7, 3.6], first_col_bold=True)
callout(doc, "문제는, 우리가 사용하는 데이터셋이 어디서 온 데이터인지 모른다는 데 있습니다.", bold=True)

doc.add_heading("4-5. 세계는 이미 같은 질문을 시작했다", level=2)
table(doc, ["주체", "묻는 방식"], [
    ["**법원**", "「이 자료는 어디서 왔고, 누가 그 사용을 허락했는가?」 — Bartz는 **책을 어떻게 취득했는지**를, "
               "Getty는 **복제가 어디서 일어났는지**를 물었다"],
    ["**규제기관**", "「시스템이 무엇으로 학습되었는지 요약을 공개하라」 — 캘리포니아 AB 2013은 "
                  "**2026년 1월부터 시행 중**이고, 유사 의무가 다른 나라에도 도입되고 있다"],
    ["**고객**", "「우리가 도입하는 모델 안에 무엇이 들어 있는지 보여 줄 수 있습니까?」 — "
               "**구매 부서는 이제 SBOM을 요구하듯 데이터 출처를 요구한다**"],
], widths=[3.0, 14.0])
para(doc, "→ 팀 공유 시 가장 설득력 있는 한 장. AI-BOM이 법무 이슈만이 아니라 구매·영업 이슈이기도 함을 보여준다.",
     size=9.5, color=MUTED)

page_break(doc)

# ────────────────────────────── 5. LG가 만들고 있는 것
doc.add_heading("5. LG AI연구원이 만들고 있는 것", level=1)

doc.add_heading("5-1. 빠진 고리를 정의한다 — 데이터셋 계보", level=2)
para(doc, "대한민국 정부의 국가 AI-BOM 프로파일 과제로 수행 중이며, SPDX 3.0을 수정 없이 확장한다.")
table(doc, ["법적 의무", "문제", "우리가 정의하는 필드"], [
    ["**인공지능 기본법** — 학습에 사용된 데이터의 개요",
     "**문장은 기록이 아니다** — 「공개 웹데이터로 학습함」 식으로는 검증할 수 있는 것이 없다",
     "**데이터셋 계보** — 문장이 아닌 **그래프**. 기계 판독 가능하고 검증 가능"],
], widths=[5.0, 6.0, 6.0])
para(doc, "구조: 모델 ← 데이터셋 ← 데이터 소스 1~4 ← 소스 1-1, 1-2… ← 소스 1-2-1… "
          "(더 이상 새로운 소스가 나오지 않을 때까지)", bold=True)
para(doc, "각 엣지에 담기는 정보: 출처 · 라이선스 · 취득 방법 · 용도", bold=True)
callout(doc, "한 나라의 법적 의무를 국제 표준의 언어로 옮겼습니다. "
             "대한민국은 신뢰가 국경을 넘는 첫걸음입니다.")

doc.add_heading("5-2. 왜 공급망의 「끝」까지 추적해야 하는가", level=2)
table(doc, ["단계", "무엇", "무슨 일이 일어났나"], [
    ["시작점", "**Bibliotik**", "비공개 트래커 — **불법 저작물 도서 유통 사이트**"],
    ["복제", "**Books3**", "여기서 스크래핑해 만들어진 도서 컬렉션"],
    ["재포장", "**The Pile**", "이를 포함한 오픈 데이터셋"],
    ["재라벨링", "**RedPajama**", "다운스트림 코퍼스, **Permissive 라이선스**"],
    ["전부 상속", "**어떤 모델**", "「오픈」 데이터로 학습"],
], widths=[2.5, 3.5, 11.0], first_col_bold=True)
bullet(doc, "중복 제거와 필터링은 데이터를 더 깨끗하게 만들 뿐, 그 출처를 알려주지는 않는다.")
bullet(doc, "모든 단계가 기술적으로는 정당했지만, 최종 모델에 이르렀을 때 진짜 출처는 "
            "네 단계 위 데이터셋에 묻혀 상위 라벨에서는 전혀 보이지 않는다.")
callout(doc, "결함은 최종 데이터셋에 있지 않습니다. 아무도 더 이상 들여다보지 않는 그 출발점에 있습니다.",
        bold=True, fill="FDF3E7", bar="B0302E")
para(doc, "왜 이런 체인이 생기는가 — A 개발자가 미국에서 학습데이터를 배포하면, 지구 반대편 인도의 개발자가 "
          "그걸 받아 「이 데이터셋 좋네, 여기에 뉴욕타임스 에디션을 좀 포함시켜 재배포해볼까」 한다. "
          "이런 식으로 데이터셋이 합쳐지고, 분할되고, 증류되고, 재배포되는 현상이 무한히 반복된다. "
          "그리고 이것이 Anthropic이 거액을 배상하게 된 바로 그 데이터셋 계보다.")

doc.add_heading("5-3. 21%만 살아남았다", level=2)
para(doc, "스스로 「상업적 이용 가능」이라 밝힌 2,852개 데이터셋을 모든 하위 소스까지 추적한 결과:")
table(doc, ["기준", "결과"], [
    ["라벨 기준 (최상단이 말한 그대로)", "**2,852개**"],
    ["추적 이후 (공급망을 실제로 따라간 결과)", "**605개 (21.2%)**"],
], widths=[9.0, 8.0], first_col_bold=True)
para(doc, "리스크 등급: A-1 > A-2 > A-3 (상업적 이용 가능) > B-1 > B-2 (연구 목적 한정) > C-1 > C-2 (이용 불가)",
     size=9.5, color=MUTED)
callout(doc, "이 숫자는 누구도 탓하지 않습니다. 우리가 얼마나 몰랐는지를 보여 줍니다. "
             "우리가 「오픈」이라 부르는 것의 78.8%는 단 한 번도 그 사슬이 추적된 적이 없습니다. "
             "배포자도, 사용자도 하지 않았습니다. 그것을 해낼 도구를 만들기 전까지는 우리도 하지 않았습니다.",
        bold=True)

rich(doc, [("FineVision 추적 사례 — ", {"b": True, "color": ACCENT})], space_before=6, space_after=2)
para(doc, "개발자들은 「이 데이터셋은 Apache / MIT / CC-BY 4.0으로 배포되어 있으니 써도 문제없겠죠?」라고 "
          "법무팀에 묻는다. 그래서 FineVision이라는 단일 데이터셋 하나를 에이전트로 끝까지 추적해봤다.")
bullet(doc, "그 아래에 약 **3,000개**의 서로 다른 라이선스 텀이 존재")
bullet(doc, "그중에는 **「이 데이터를 절대 AI 학습에 사용하지 마세요」**, 「non-commercial 용도로만 사용 가능」 "
            "같은 조건이 다수")
bullet(doc, "이미 소송에 걸려 있거나 판결을 앞둔 **위험 데이터셋**도 포함")

rich(doc, [("개발자들은 출처를 알고 쓰는가? — 아니다", {"b": True, "color": ACCENT})],
     space_before=6, space_after=2)
callout(doc, "이게 SNS의 「좋아요」와 같습니다.", bold=True)
para(doc, "허깅페이스의 Most Downloaded / Most Liked 목록이 그 역할을 한다. 「이 데이터를 썼더니 성능이 많이 "
          "올라간다」는 좋아요가 쌓인 데이터셋이 널리 쓰이고, 출처는 추적되지 않는다. 그래서 위험한 데이터셋인지 "
          "— 심지어 악용 데이터가 섞여 있는지 — 전혀 모르는 상태로, 벤치마크 성능에 도움 되는 데이터셋 위주로 "
          "사용·배포되고 있다.")

doc.add_heading("5-4. 노력의 문제가 아니라 규모의 문제", level=2)
para(doc, "데이터셋 하나를 정직하게 검토하려면:")
for i, step in enumerate([
    "검토 대상 데이터셋 확인",
    "루트 데이터셋의 라이선스 조건 분석",
    "루트 데이터셋 내 모든 하위 소스 발견 (메타데이터 파싱 → 중첩 하위 소스 추출)",
    "개별 하위 소스별 조건 분석",
    "하위의 하위 소스까지 재귀적으로 추적",
    "최하위 소스의 조건까지 평가 → 라이선스를 종합해 총체적 리스크 평가 → AI 데이터 리스크 등급",
], 1):
    numbered(doc, step, n=i)
callout(doc, "사람의 속도로는 끝에 닿을 수 없습니다. 게을러서가 아니라, 숫자가 허락하지 않기 때문입니다.",
        bold=True)
para(doc, "규모의 실체 — 데이터셋 하나 안에 서로 다른 라이선스 노드가 많은 경우 1만 8천 개까지 병존한다. "
          "이걸 전부 수집하고 노드별로 평가해야만 최종 AI 데이터 리스크 등급을 낼 수 있다.")

doc.add_heading("5-5. 그래서 에이전트로 풀었다", level=2)
table(doc, ["단계", "하는 일"], [
    ["**1. 읽기**", "데이터셋 카드를 연다. 선언된 모든 소스를 추출한다"],
    ["**2. 추적**", "각 소스를 따라간다. **아래에 아무것도 남지 않을 때까지 재귀**한다. "
                  "개발자가 논문·개인 블로그·허깅페이스 페이지에 남긴 단서까지 웹을 돌아다니며 뒤진다"],
    ["**3. 평가**", "맨 위가 아니라 **공급망 전체를 평가**한다. 각 소스 노드의 라이선스 텀을 수집해 "
                  "「사용 가능」인지 「AI 학습 금지 조항이 있는지」를 판단한다"],
], widths=[2.5, 14.5])
table(doc, ["측정", "결과"], [
    ["수작업 대비", "**45배 더 빠르게**"],
    ["전문가 대비", "**26% 더 정확하게**"],
], widths=[4.0, 13.0], first_col_bold=True)
callout(doc, "우리는 판단을 자동화한 것이 아닙니다. 추적하는 일을 자동화했을 뿐이고, "
             "그것은 애초에 판단이 아니었습니다.", bold=True, size=11)
para(doc, "이 체계는 LG AI연구원 내부를 넘어 LG DX 그룹에도 배포되었고, 국내 로펌들과 협업해 "
          "복잡하게 트리화된 학습데이터의 평가 기준을 만들고 있다.")

doc.add_heading("5-6. 추적의 끝에서 드러나는 것 — UltraFeedback 사례", level=2)
para(doc, "INPUT: openbmb/UltraFeedback (Dataset, Text, License: MIT). "
          "14개 기준(데이터 라이선스의 존재, 산출물에 대한 권리, 알려진 분쟁 등)으로 스코어링.")
table(doc, ["평가", "결과"], [
    ["**Individual Assessment (A-3)**", "상업적 이용 가능 (Low Risk) — **최상단 노드만 보면 MIT 오픈소스**"],
    ["**Aggregate Assessment (C-2)**", "**Common Crawl과 GPT-4를 사용했기 때문에 "
                                       "상업적·내부 이용 모두 불가 (High Risk)**"],
], widths=[6.0, 11.0])
para(doc, "의존 체인: UltraFeedback ← GPT-4 / UltraChat / ShareGPT / Evol-Instruct ← "
          "ChatGPT Turbo API / C4 Dataset / dolly-15k / Falcon 40B ← Common Crawl / Wikipedia / "
          "Databricks employees…", size=9.5)
para(doc, "※ 의존 대상의 등급이 파생물보다 낮은 역전(inversion)이 발생하는 지점에서 오류가 드러난다. "
          "등급 체계는 A = 안전(상업적 이용 가능) ↔ C = 위험(이용 불가).", size=9.5, color=MUTED)
callout(doc, "법적 리스크는 데이터 라이프사이클 추적을 통해서만 탐지 가능합니다.", bold=True)

doc.add_heading("5-7. K-AI BOM은 공급망 전체를 따라 이동한다", level=2)
table(doc, ["주체", "역할"], [
    ["데이터셋", "자신의 출처와 계보를 선언한다"],
    ["AI 모델", "이를 상속하고 자신의 기록을 더한다"],
    ["서비스", "모델과 그 기록을 함께 제공한다"],
    ["사용자", "무엇을 실행하고 있는지 검증할 수 있다"],
], widths=[3.0, 14.0], first_col_bold=True)
bullet(doc, "네 주체가 원하는 바는 서로 다르지만, 이제는 같은 기록 위에서 각자 스스로 판단하고 결정할 수 있다.",
       bold_prefix="이해관계는 달라도, 근거는 하나 — ")
bullet(doc, "누구도 다른 사람의 판단을 받아들일 필요는 없다. 같은 것을 볼 수 있고, "
            "그다음 스스로 결정할 수 있으면 충분하다.", bold_prefix="하나의 기록, 여러 개의 결정 — ")
callout(doc, "몇 년 후에는 우리 집에도 가사 로봇이 있고 길거리에도 로봇이 걸어 다닐 것 같습니다. "
             "AI 로봇이 나를 때린다면, 나는 누구에게 소송을 걸어야 합니까? AI 배포자인가, 로봇을 만든 "
             "사람인가, 아니면 데이터셋을 무단으로 여러 번 재배포한 사람인가? 공급망에서 학습데이터와 "
             "AI 모델이 다음 이해관계자에게 전달될 때 증빙 가능한 정보가 함께 들어간다면, "
             "그 판단의 근거가 됩니다.", italic=True)
para(doc, "K-AI BOM 현황 — SPDX를 차용한 한국형 AI-BOM으로 개발 중이며 NIPA 과제를 통해 수행. "
          "별도로 학습데이터를 직접 추적해볼 수 있는 플랫폼도 제공 중이다. "
          "목적은 사후 수습이 아니라 사전 대처 — 다 만들어놓고 나서 거액짜리 데이터셋을 썼다는 걸 "
          "알게 되는 상황을 막는 것.")

page_break(doc)

# ────────────────────────────── 6. 외부 검증
doc.add_heading("6. 외부 검증 — 웹 리서치 팩트체크", level=1)
para(doc, "발표 내용을 1차 자료와 대조한 결과다 (2026-09-07 검색 기준).", size=9.5, color=MUTED)
table(doc, ["발표 내용", "공개 자료로 확인한 것", "판정"], [
    ["「Bartz v. Anthropic 합의금 약 2조 원」",
     "**$1.5B(15억 달러)** 합의. 약 50만 건의 저작물 대상, **작품당 약 $3,000**, "
     "해적판 데이터셋 폐기 의무, 120일 옵트아웃. 미국 사상 최대 규모 저작권 합의 [1][2][3]", "맞음"],
    ["Bartz 4요소 표 (①O ②O ③X)",
     "Alsup 판사는 **적법 취득 도서로 학습한 것은 공정이용**이라 했으나, 해적 사이트에서 내려받아 "
     "중앙 라이브러리에 보관한 부분은 공정이용을 인정하지 않았다. Anthropic은 Books3·LibGen·PiLiMi 등에서 "
     "**700만 권 이상**을 내려받았다 [1][2][3]", "맞음"],
    ["「GEMA v. OpenAI 독일에서 OpenAI 완패」",
     "2025-11-11 **뮌헨 지방법원 I**, OpenAI가 독일 저명 아티스트의 저작권을 침해했다고 판결. "
     "부작위·손해배상·정보제공 명령 [4][5][6]", "맞음"],
    ["「Getty Images v. Stability AI — 피고 승」",
     "2025-11-04 영국 고등법원. **2차적 침해 주장 기각** — 모델 가중치가 원저작물을 저장하지 않으므로 "
     "「침해 복제물」이 아님. 단, **Getty가 재판 중 학습 과정 침해·산출물 침해 주장을 스스로 철회** [7][8]",
     "결론은 맞음 (표현 주의)"],
    ["「Thomson Reuters v. ROSS — 원고 승」",
     "2025-02 델라웨어 연방법원, 헤드노트 2,243건 직접침해 인정 + 공정이용 항변 배척. "
     "**단, 제3연방항소법원 항소 진행 중** (2025-06 상고 허가, 2026-07 구두변론) [9][10]",
     "**확정된 법리 아님**"],
    ["「K-EXAONE 2.0 = 750B, 오픈소스」",
     "LG AI연구원이 **7,500억(750B) 파라미터 K-EXAONE 2.0**을 공개, 상업적 활용 가능하도록 "
     "오픈소스로 전면 개방 [11]", "맞음"],
    ["「GEMA v. Suno 독일 연쇄 패소(2026)」", "이번 검색으로는 확인하지 못함", "**미검증**"],
], widths=[4.5, 10.0, 2.5])

doc.add_heading("6-1. 「라벨을 믿지 마라」에 대한 독립적 근거", level=2)
para(doc, "LG의 2,852 → 605(21.2%)는 자체 산출이라 외부 검증이 안 된다. 그런데 같은 현상을 "
          "다른 팀이 독립적으로 측정한 연구가 있다 — Data Provenance Initiative (MIT 등, "
          "Nature Machine Intelligence 게재) [12][13].")
table(doc, ["측정 항목", "결과"], [
    ["감사 대상", "44개 instruction/alignment 컬렉션, **1,858개 개별 데이터셋**의 계보 추적"],
    ["라이선스 누락률", "GitHub·허깅페이스 인기 데이터셋의 **70% 이상이 「unspecified」**"],
    ["라이선스 오류율", "**50% 이상.** 허깅페이스 라이선스의 **66%가 실제와 다른 이용 카테고리**"],
    ["오류의 방향", "대부분 **원저자의 실제 라이선스보다 더 관대(permissive)하게** 표기됨"],
    ["개선 결과", "미지정 라이선스를 72% → **30%**로 낮추고 라이선스 URL 부착"],
], widths=[4.0, 13.0], first_col_bold=True)
callout(doc, "「허깅페이스 라벨이 실제보다 더 관대한 쪽으로 틀린다」는 것은, UltraFeedback 사례"
             "(MIT라 적혀 있으나 실제는 C-2)가 예외가 아니라 구조적 패턴임을 뜻한다. "
             "LG의 21.2%와 DPI의 66% 오분류는 서로 다른 방법론으로 같은 방향을 가리킨다.", bold=True)

doc.add_heading("6-2. AI-BOM 표준의 현재 위치", level=2)
bullet(doc, "**SPDX 3.0**은 **2024-04-16 정식 릴리스**되었고, **AI Profile**과 **Dataset Profile**을 "
            "분리해 담았다 [14][15]")
bullet(doc, "산업계·학계 워킹그룹이 모델 카드·데이터시트·팩트시트를 분석해 두 프로파일에 걸쳐 "
            "**36개 필드**를 선정 [14][15]")
bullet(doc, "이 프레임워크는 **EU AI Act, FDA 의료기기 규제 등 규제 요건에 매핑**되도록 설계되었고, "
            "기존 SPDX 툴체인과 호환된다 [14][15]")
bullet(doc, "Linux Foundation Research가 실무 가이드를 공개 [14][16]")
para(doc, "→ 발표의 표현은 정확하다. 스펙에는 데이터셋 계보를 담을 필드가 이미 있다. 없는 것은 그 필드를 "
          "채울 데이터이고, LG가 만든 것은 표준이 아니라 그 필드를 채우는 에이전트다. "
          "다만 SPDX 3.0의 Dataset Profile은 「이 데이터셋이 무엇인가」를 기술하는 데는 충분하지만 "
          "「어디서 왔는가」를 재귀적으로 강제하지는 않는다 — 발표가 지목한 빈칸이 정확히 여기다.")

page_break(doc)

# ────────────────────────────── 7. 체크리스트 + 규제 캘린더
doc.add_heading("7. 우리 팀에서 바로 쓸 것", level=1)

doc.add_heading("7-1. 규제 데드라인", level=2)
table(doc, ["관할", "근거", "시점", "요구 사항"], [
    ["**한국**", "AI 기본법 + 시행령", "**2026-01-22 시행**",
     "고영향 AI·생성형 AI 기반이라는 사실의 사전 고지 등. **규제 적용은 최소 1년 이상 유예**되며 "
     "유예 기간에는 계도 중심 운영 [17][18]"],
    ["**EU**", "AI Act 제53조(1)(d)", "의무 **2025-08-02**, 집행 **2026-08-02**, 기존 모델 **2027-08-02**",
     "AI Office 공식 템플릿(2025-07-24 공개)으로 학습 콘텐츠 요약 공개. **오픈소스·무료 라이선스 모델도 대상.** "
     "위반 시 **최대 1,500만 유로 또는 전 세계 매출 3%** 중 큰 금액 [19][20][21]"],
    ["**미국(캘리포니아)**", "AB 2013", "**2026-01-01 시행**",
     "**2022-01-01 이후** 공개된 생성형 AI에 대해 학습 데이터셋 요약을 웹사이트에 사전 게시, "
     "중대 변경 시 갱신. **12개 항목**(출처·소유자, 데이터 포인트 수, 저작물·개인정보 포함 여부 등). "
     "**영업비밀 예외 없음** → xAI가 위헌 소송 제기 [22][23][24]"],
    ["**한국(저작권법)**", "TDM 면책 조항", "**미입법**",
     "AI 학습 목적 복제를 조건부 허용하는 개정안이 발의됐으나 국회 미통과. 한편 문체부는 "
     "**학습데이터 목록 공개 의무**를 포함한 개정을 예고 [25][26]"],
], widths=[3.0, 3.0, 3.5, 7.5])
callout(doc, "여기서 발표의 논지가 강화된다 — EU는 「요약을 공개하라」, 캘리포니아는 「출처·소유자·저작물 "
             "포함 여부를 12개 항목으로 공개하라」고 한다. 그런데 UltraFeedback을 끝까지 추적해야 "
             "그 답이 A-3이 아니라 C-2라는 걸 알 수 있다. 즉 추적 없이는 공시 자체가 부정확한 진술이 된다.",
        bold=True, fill="FDF3E7", bar="B0302E")

doc.add_heading("7-2. 실행 체크리스트", level=2)
items = [
    ("라벨을 그대로 믿지 않는다",
     "MIT·Apache·CC-BY 같은 최상단 라벨과 실제 상속 리스크는 다를 수 있다. "
     "근거는 LG 하나가 아니다 — DPI 감사에서 허깅페이스 라이선스의 66%가 오분류, 그것도 더 관대한 쪽으로."),
    ("벤더 계약서에 학습데이터 고지 조항을 넣는다",
     "출처 · 라이선스 · 취득 방법 · 용도. 표준 언어로 SPDX 3.0 AI/Dataset Profile(36개 필드)을 지목하면 "
     "협상이 쉬워진다."),
    ("규제 캘린더를 데드라인으로 관리한다",
     "한국 2026-01-22(유예 1년+), EU 집행 2026-08-02, 캘리포니아 2026-01-01. "
     "오픈소스로 배포해도 EU 의무는 면제되지 않는다."),
    ("「인기 = 안전」이 아님을 팀 규칙으로 못 박는다",
     "허깅페이스의 Most Downloaded / Most Liked는 벤치마크 성능 신호이지 법적 안전 신호가 아니다."),
    ("취득 방법을 기록 항목으로 승격한다",
     "Bartz가 증명한 것은 「학습했는가」가 아니라 「어떻게 취득했는가가 배상액의 크기를 정한다」는 것. "
     "데이터 수집 파이프라인에 「어디서, 어떤 권한으로 받았는가」를 남기는 로깅이 사후 방어의 유일한 증거다."),
    ("추적은 자동화하되, 판단은 사람이 한다",
     "LG의 방식이 그대로 참고 모델이다 — 에이전트로 재귀 추적(수작업 대비 45배, 전문가 대비 26% 더 정확), "
     "최종 의사결정권은 인간. 판단까지 자동화하면 그 판단 자체가 새로운 미기록 리스크가 된다."),
]
for i, (title, body) in enumerate(items, 1):
    rich(doc, [(f"{i}. {title}", {"b": True, "size": 10.5, "color": ACCENT})],
         space_before=6, space_after=2)
    para(doc, body, size=9.5, indent=0.5, space_after=2)

doc.add_heading("7-3. 무신사 세션(같은 날)과 이어 읽기", level=2)
cmp_tbl = table(doc, ["", "무신사 (길기용)", "LG AI연구원 (조정원)"], [
    ["관점", "도입 판단 — 살까 / 만들까 / 안 할까", "공급망 신뢰 — 무엇으로 만들어졌는지 증명 가능한가"],
    ["언제 기록하나", "시작 전에 「멈출 기준」을 **계약서보다 먼저**", "학습 전에 데이터 계보를 **문장이 아닌 그래프로**"],
    ["자동화한 것", "판단이 아니라 **검증 절차**(가드레일 지표)", "판단이 아니라 **추적**(에이전트)"],
    ["자동화하지 않은 것", "환불·보상 판정, 분쟁 소지 확인 → 100% 사람", "**최종 법적 판단** → 100% 사람"],
    ["공통점", "둘 다 **「기록되지 않은 것은 판단할 수 없다」** — 사후 논쟁을 없애기 위해 사전에 기준·기록을 문서로 확정", ""],
], widths=[3.0, 7.0, 7.0], first_col_bold=True)
# 「공통점」 행은 두 열에 걸치는 하나의 문장이므로 병합한다
cmp_tbl.rows[-1].cells[1].merge(cmp_tbl.rows[-1].cells[2])
para(doc, "→ 무신사가 외부 업체 계약에 건 조건 ③ 「어떤 LLM으로 바꾸더라도 돌아가는 구조」는 벤더 종속 "
          "방지책이지만, LG의 관점에서 읽으면 모델 계보를 우리가 통제하겠다는 선언이기도 하다. "
          "반대로 LG가 말한 「구매 부서는 이제 SBOM을 요구하듯 데이터 출처를 요구한다」는, "
          "무신사식 TCO 계산서에 새 비용 항목이 하나 추가된다는 뜻이다 — "
          "벤더의 학습데이터 계보를 검증하는 비용.", size=9.5, color=MUTED)

page_break(doc)

# ────────────────────────────── 8. 주의 + 출처
doc.add_heading("8. 인용할 때 주의할 점", level=1)
table(doc, ["항목", "주의"], [
    ["GEMA v. Suno 독일 판결(2026)", "**웹 검색으로 확인하지 못했다.** 인용 시 「발표자 언급」 단서를 달 것"],
    ["Thomson Reuters v. ROSS", "1심은 원고 승이지만 **제3연방항소법원 항소 진행 중**(2026-07 구두변론). "
                                "「확정된 법리」로 인용하면 안 된다"],
    ["Getty Images v. Stability AI", "「AI사가 이겼다」보다 **「Getty가 두 개의 핵심 주장을 스스로 철회했고 "
                                     "남은 2차적 침해 주장도 기각됐다」**가 정확하다"],
    ["2,852 → 605 (21.2%)", "LG **자체 추적 결과**이며 방법론이 공개되지 않았다. "
                            "다만 Data Provenance Initiative의 독립 감사가 같은 방향을 가리킨다"],
    ["분쟁 130~150건 / 100건 이상 진행 중", "**발표자 집계**. 공개 통계로 교차 확인하지 못했다"],
    ["리스크 등급 분포 (A-1~C-2)", "PDF 텍스트 추출 시 두 계열의 숫자가 뒤섞여 나온다. "
                                   "인용하려면 **원본 슬라이드 p.22 이미지를 직접 확인**할 것"],
    ["평가 기준 개수", "발표 슬라이드는 UltraFeedback 스코어링에 **14개 기준**, 공개 자료는 "
                     "데이터 컴플라이언스 **18개 기준**을 말한다. 서로 다른 시점/층위로 보이므로 "
                     "인용 시 출처를 명시할 것"],
], widths=[4.5, 12.5], first_col_bold=True)

hr(doc)
doc.add_heading("출처", level=2)
sources = [
    "[1] What to Know About the $1.5 Billion Bartz v. Anthropic Settlement — Copyright Alliance  https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/",
    "[2] Bartz v. Anthropic Settlement: What Authors Need to Know — The Authors Guild  https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/",
    "[3] The Bartz v. Anthropic Settlement — Kluwer Copyright Blog  https://legalblogs.wolterskluwer.com/copyright-blog/the-bartz-v-anthropic-settlement-understanding-americas-largest-copyright-settlement/",
    "[4] GEMA vs. OpenAI: Landmark ruling — Heuking  https://www.heuking.de/en/news-events/newsletter-articles/detail/gema-vs-openai-landmark-ruling-on-ai-language-models-and-copyright-law.html",
    "[5] Landmark ruling of the Munich Regional Court (GEMA v OpenAI) — Bird & Bird  https://www.twobirds.com/en/insights/2025/landmark-ruling-of-the-munich-regional-court-(gema-v-openai)",
    "[6] German court rules in favour of GEMA against OpenAI — EU IP Helpdesk  https://intellectual-property-helpdesk.ec.europa.eu/news-events/news/german-court-rules-favour-music-rights-management-organisation-against-openai-nyt-vs-openai-dispute-2025-11-14_en",
    "[7] Stability AI defeats Getty Images copyright claims — Bird & Bird  https://www.twobirds.com/en/insights/2025/uk/stability-ai-defeats-getty-images-copyright-claims-in-first-of-its-kind-dispute-before-the-high-cour",
    "[8] Getty Images v. Stability AI: English High Court Rejects Secondary Copyright Claim — Latham & Watkins  https://www.lw.com/en/insights/getty-images-v-stability-ai-english-high-court-rejects-secondary-copyright-claim",
    "[9] Court Decides that Use of Copyrighted Works in AI Training Is Not Fair Use — Jenner & Block  https://www.jenner.com/en/news-insights/client-alerts/court-decides-that-use-of-copyrighted-works-in-ai-training-is-not-fair-use-thomson-reuters-enterprise-centre-gmbh-v-ross-intelligence-inc",
    "[10] Third Circuit Hears Oral Argument in Ross v. Reuters — Baker Botts  https://www.bakerbotts.com/thought-leadership/publications/2026/july/third-circuit-hears-oral-argument",
    "[11] LG AI연구원, 7500억개 파라미터 'K-엑사원 2.0' 공개 — 천지일보  https://www.newscj.com/news/articleView.html?idxno=3421513",
    "[12] The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI (arXiv:2310.16787)  https://arxiv.org/pdf/2310.16787",
    "[13] A large-scale audit of dataset licensing and attribution in AI — Nature Machine Intelligence  https://www.nature.com/articles/s42256-024-00878-8",
    "[14] Implementing AI Bill of Materials (AI BOM) with SPDX 3.0 — Linux Foundation Research  https://www.linuxfoundation.org/hubfs/LF%20Research/lfr_spdx_aibom_102524a.pdf",
    "[15] Implementing AI BOM with SPDX 3.0 — 논문 개요 (alphaXiv 2504.16743)  https://www.alphaxiv.org/overview/2504.16743v1",
    "[16] Implementing an AI BOM — SPDX  https://spdx.dev/implementing-an-ai-bom/",
    "[17] AI 기본법 시행과 그 시사점 — 법률신문 / 법무법인 세종  https://www.lawtimes.co.kr/news/articleView.html?idxno=216500",
    "[18] 인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 — 국가법령정보센터  https://www.law.go.kr/lsInfoP.do?lsiSeq=268543",
    "[19] European Commission Releases Mandatory Template for Public Disclosure of AI Training Data — WilmerHale  https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/european-commission-releases-mandatory-template-for-public-disclosure-of-ai-training-data",
    "[20] EU AI Act News: Rules on General-Purpose AI Start Applying — Mayer Brown  https://www.mayerbrown.com/en/insights/publications/2025/08/eu-ai-act-news-rules-on-general-purpose-ai-start-applying-guidelines-and-template-for-summary-of-training-data",
    "[21] EU Commission Publishes Guidelines on General Purpose AI Obligations — Paul, Weiss  https://www.paulweiss.com/insights/client-memos/eu-commission-publishes-guidelines-on-general-purpose-ai-obligations-as-well-as-training-data-disclosure-template-further-clarity-as-the-countdown-to-enforcement-begins",
    "[22] California's AB 2013 Takes Effect — Goodwin  https://www.goodwinlaw.com/en/insights/publications/2026/01/alerts-otherindustries-californias-ab-2013-takes-effect",
    "[23] Generative AI Training Data Transparency Act (AB 2013) — California Legislative Information  https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240AB2013",
    "[24] California's AB 2013 Requires Generative AI Data Disclosure by January 1, 2026 — Crowell & Moring  https://www.crowell.com/en/insights/client-alerts/californias-ab-2013-requires-generative-ai-data-disclosure-by-january-1-2026",
    "[25] AI 학습데이터 저작권 침해와 저작권법 상의 TDM 조항 도입 논의 — NEPLA  https://www.nepla.ai/",
    "[26] 저작권법상 텍스트·데이터 마이닝(TDM) 면책규정 도입 방향의 검토 — 류시원, 법무부  https://www.moj.go.kr/bbs/moj/166/450511/download.do",
    "[27] AI 거버넌스의 패러다임 변화와 LG AI연구원의 선도적 역할 — 공개SW포털  https://www.oss.kr/pages/11/4418",
]
for s in sources:
    para(doc, s, size=8.5, color=MUTED, space_after=2, indent=0.3)

out = "/home/user/Aistudy/share/02_LG-AI연구원_AI-BOM_세션정리.docx"
doc.save(out)
print("saved:", out)
