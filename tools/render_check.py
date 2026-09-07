# -*- coding: utf-8 -*-
"""검증용: 폰트를 컨테이너에 설치된 NanumGothic으로 바꿔 PDF 렌더링 결과를 확인한다."""
import shutil, subprocess, sys, zipfile
from pathlib import Path

src, tag = Path(sys.argv[1]), sys.argv[2]
sp = Path("/tmp/claude-0/-home-user-Aistudy/9492df34-55ab-56a5-ac1c-c34e294a01b2/scratchpad")
work = sp / f"{tag}_check.docx"
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(work, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith(".xml"):
            data = data.replace("맑은 고딕".encode(), b"NanumGothic")
        zout.writestr(item, data)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", str(work),
                "--outdir", str(sp)], check=True, capture_output=True, timeout=300)
import pymupdf
d = pymupdf.open(str(work.with_suffix(".pdf")))
for i in range(len(d)):
    d[i].get_pixmap(dpi=95).save(str(sp / f"{tag}_{i+1:02d}.png"))
print(f"pages={len(d)} -> {sp}/{tag}_NN.png")
