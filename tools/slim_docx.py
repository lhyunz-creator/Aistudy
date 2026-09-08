# -*- coding: utf-8 -*-
"""python-docx 기본 템플릿이 끌고 오는 불필요한 파트를 제거해 파일 크기를 줄인다.

stylesWithEffects.xml은 Word 2010 호환용 레거시 파트이고, thumbnail.jpeg는 미리보기
이미지라 둘 다 문서 내용과 무관하다. 참조(관계·콘텐츠 타입)까지 함께 지운다.
"""
import re, sys, zipfile
from pathlib import Path

DROP = ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg")

def slim(path: Path) -> tuple[int, int]:
    before = path.stat().st_size
    with zipfile.ZipFile(path) as zin:
        items = {i.filename: zin.read(i.filename) for i in zin.infolist()}
        order = [i.filename for i in zin.infolist()]

    for name in DROP:
        items.pop(name, None)

    # 관계 파일에서 삭제된 파트를 가리키는 Relationship 제거
    for rels in ("word/_rels/document.xml.rels", "_rels/.rels"):
        if rels not in items:
            continue
        xml = items[rels].decode("utf-8")
        for target in ("stylesWithEffects.xml", "thumbnail.jpeg"):
            xml = re.sub(r"<Relationship[^>]*Target=\"[^\"]*%s\"[^>]*/>" % target, "", xml)
        items[rels] = xml.encode("utf-8")

    # [Content_Types].xml에서 Override 제거
    if "[Content_Types].xml" in items:
        xml = items["[Content_Types].xml"].decode("utf-8")
        for name in DROP:
            xml = re.sub(r"<Override PartName=\"/%s\"[^>]*/>" % re.escape(name), "", xml)
        xml = re.sub(r"<Default Extension=\"jpeg\"[^>]*/>", "", xml)
        items["[Content_Types].xml"] = xml.encode("utf-8")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        for name in order:
            if name in items:
                zout.writestr(name, items[name])
    return before, path.stat().st_size

for arg in sys.argv[1:]:
    p = Path(arg)
    b, a = slim(p)
    print(f"{p.name}: {b:,} -> {a:,} bytes ({a*100//b}%)")
