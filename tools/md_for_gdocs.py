# -*- coding: utf-8 -*-
"""구글 닥스 마크다운 변환용으로 노트를 손질한다.

Drive의 마크다운 임포트는 표 셀 안의 **굵게**를 해석하지 못하고 리터럴로 남긴다.
표 행에서는 ** 를 제거하고, 셀 안의 줄바꿈 유발 요소도 정리한다.
"""
import re, sys
from pathlib import Path

def clean(text: str) -> str:
    out = []
    for line in text.split("\n"):
        if line.lstrip().startswith("|"):
            line = line.replace("**", "")
        out.append(line)
    return "\n".join(out)

for arg in sys.argv[1:]:
    src = Path(arg)
    dst = Path("/tmp/claude-0/-home-user-Aistudy/9492df34-55ab-56a5-ac1c-c34e294a01b2/scratchpad") / ("gd_" + src.name)
    dst.write_text(clean(src.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{src.name} -> {dst} ({dst.stat().st_size:,} bytes)")
