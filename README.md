# Aistudy

AI 관련 컨퍼런스·세션 학습 노트 저장소.

## 구성

| 경로 | 내용 |
|---|---|
| [`notes/`](notes/) | 세션별 정리 노트 (마크다운) — 원문 정리 + 웹 리서치 보강 + 배포 슬라이드 대조 |
| [`share/`](share/) | 팀 공유용 Word 문서(.docx)와 원본 발표 자료(PDF) |
| [`tools/`](tools/) | 마크다운 노트를 Word 문서로 빌드하는 스크립트 |

## 세션 노트

### AI Infrastructure & Data 2026 (2026-09-02, CIO Korea / ITWORLD)

- [세션 3건 교차 정리 · 종합 체크리스트](notes/2026-09-02-ai-infra-data/README.md)
- [01. 유행이 아니라 데이터로 — 무신사의 AI 기술 도입 전략](notes/2026-09-02-ai-infra-data/01-musinsa-ai-adoption.md) · 길기용 (무신사)
- [02. AI 학습데이터의 국내외 분쟁 동향과 추적가능 컴플라이언스](notes/2026-09-02-ai-infra-data/02-lg-ai-bom.md) · 조정원 (LG AI연구원)
- [03. Securing AI starts with Identity — AI 에이전트·NHI 거버넌스](notes/2026-09-02-ai-infra-data/03-sailpoint-agentic-identity.md) · Dean Clarke (SailPoint)

## 공유용 문서 다시 만들기

```bash
pip install python-docx
python3 tools/build_musinsa_docx.py
python3 tools/build_lgai_docx.py
```

`tools/render_check.py`는 생성된 .docx를 PDF로 변환해 페이지 이미지를 뽑는 검증용 스크립트다
(LibreOffice와 PyMuPDF 필요, 한글 폰트가 없는 환경에서는 NanumGothic으로 치환해 렌더링한다).
