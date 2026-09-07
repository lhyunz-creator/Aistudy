# -*- coding: utf-8 -*-
"""팀 공유용 세션 정리 Word 문서 빌더 공통 헬퍼."""
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_FONT = "맑은 고딕"
ACCENT = RGBColor(0x1F, 0x3B, 0x73)     # 짙은 남색
MUTED = RGBColor(0x5A, 0x60, 0x6A)      # 회색
WARN = RGBColor(0xB0, 0x30, 0x2E)       # 경고 적색
HDR_FILL = "1F3B73"
ALT_FILL = "EEF1F7"
QUOTE_FILL = "F5F6F8"
NOTE_FILL = "FDF3E7"


def _set_cjk(run):
    """한글이 Times New Roman으로 깨지지 않도록 eastAsia 폰트를 명시한다."""
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), BODY_FONT)


def _shade(element, fill):
    """CT_TcPr 스키마상 w:shd는 w:tcBorders 다음에 와야 한다."""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    borders = element.find(qn("w:tcBorders"))
    if borders is not None:
        borders.addnext(shd)
    else:
        element.append(shd)


def new_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)   # A4
    sec.top_margin = sec.bottom_margin = Cm(2.0)
    sec.left_margin = sec.right_margin = Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(10)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    pf = normal.paragraph_format
    pf.space_after = Pt(6)
    pf.line_spacing = 1.35

    for name, size, color, before in (
        ("Heading 1", 16, ACCENT, 20),
        ("Heading 2", 13, ACCENT, 16),
        ("Heading 3", 11, RGBColor(0x2C, 0x2C, 0x2C), 12),
    ):
        st = doc.styles[name]
        st.font.name = BODY_FONT
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = color
        st.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True
    return doc


def add_page_number_footer(doc, left_text):
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(left_text + "  |  ")
    run.font.size = Pt(8)
    run.font.color.rgb = MUTED
    _set_cjk(run)
    for instr in ("PAGE",):
        fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
        instr_el = OxmlElement("w:instrText"); instr_el.set(qn("xml:space"), "preserve")
        instr_el.text = f" {instr} "
        fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
        r = p.add_run(); r.font.size = Pt(8); r.font.color.rgb = MUTED
        r._element.append(fld_begin); r._element.append(instr_el); r._element.append(fld_end)


def para(doc, text="", size=10, bold=False, italic=False, color=None,
         align=None, space_before=0, space_after=6, indent=0, style=None):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if text:
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        if color is not None:
            run.font.color.rgb = color
        _set_cjk(run)
    return p


def rich(doc, segments, size=10, align=None, space_before=0, space_after=6, indent=0):
    """segments: [(text, {'b':True,'i':True,'color':RGBColor,'size':9}), ...]"""
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    for text, opts in segments:
        run = p.add_run(text)
        run.font.size = Pt(opts.get("size", size))
        run.bold = opts.get("b", False)
        run.italic = opts.get("i", False)
        if "color" in opts:
            run.font.color.rgb = opts["color"]
        _set_cjk(run)
    return p


def bullet(doc, text, level=0, size=10, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.6 + 0.5 * level)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True; r.font.size = Pt(size); _set_cjk(r)
    r = p.add_run(text); r.font.size = Pt(size); _set_cjk(r)
    return p


def numbered(doc, text, size=10, bold_prefix=None, n=None):
    """List Number 스타일은 문서 전체가 하나의 번호 인스턴스를 공유해 번호가 이어져 버린다.
    번호를 직접 찍고 내어쓰기만 준다."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    if n is not None:
        r = p.add_run(f"{n}. "); r.bold = True; r.font.size = Pt(size); _set_cjk(r)
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True; r.font.size = Pt(size); _set_cjk(r)
    r = p.add_run(text); r.font.size = Pt(size); _set_cjk(r)
    return p


def callout(doc, text, fill=QUOTE_FILL, bar=HDR_FILL, size=10, bold=False, italic=False):
    """좌측 컬러 바 + 배경색 인용 블록."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)
    _shade(cell._tc.get_or_add_tcPr(), fill)
    _cell_borders(cell, left=(bar, 24), top=(fill, 4), bottom=(fill, 4), right=(fill, 4))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(0.25)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    _set_cjk(run)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl


def _cell_borders(cell, **edges):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge, spec in edges.items():
        if spec is None:
            continue
        color, sz = spec
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    shd = tcPr.find(qn("w:shd"))
    if shd is not None:
        shd.addprevious(borders)
    else:
        tcPr.append(borders)


def table(doc, headers, rows, widths=None, size=9, header_size=9, zebra=True,
          first_col_bold=False):
    ncols = len(headers)
    tbl = doc.add_table(rows=1, cols=ncols)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    if widths is None:
        widths = [17.0 / ncols] * ncols
    total = sum(widths)
    widths = [w * 17.0 / total for w in widths]

    hdr = tbl.rows[0]
    _repeat_header(hdr)
    for i, text in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths[i])
        _shade(cell._tc.get_or_add_tcPr(), HDR_FILL)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(str(text))
        run.bold = True
        run.font.size = Pt(header_size)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        _set_cjk(run)

    for r, row in enumerate(rows):
        cells = tbl.add_row().cells
        for i, text in enumerate(row):
            cell = cells[i]
            cell.width = Cm(widths[i])
            if zebra and r % 2 == 1:
                _shade(cell._tc.get_or_add_tcPr(), ALT_FILL)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.2
            _write_marked(p, str(text), size, force_bold=(first_col_bold and i == 0))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl


def _write_marked(p, text, size, force_bold=False):
    """**굵게** 마크업만 해석한다."""
    parts = text.split("**")
    for idx, part in enumerate(parts):
        if not part:
            continue
        run = p.add_run(part)
        run.font.size = Pt(size)
        run.bold = force_bold or (idx % 2 == 1)
        _set_cjk(run)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def hr(doc, color="C6CCD8"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), color)
    borders.append(bottom)
    pPr.append(borders)
    return p


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def cover(doc, kicker, title, subtitle, meta_rows):
    """subtitle은 문자열 또는 줄 단위 리스트. \n은 Word에서 렌더링되지 않으므로 단락을 나눈다."""
    rich(doc, [(kicker, {"b": True, "size": 9, "color": MUTED})], space_after=2)
    rich(doc, [(title, {"b": True, "size": 22, "color": ACCENT})], space_after=4)
    lines = [subtitle] if isinstance(subtitle, str) else list(subtitle or [])
    for i, line in enumerate(lines):
        rich(doc, [(line, {"size": 11.5, "color": MUTED})],
             space_after=10 if i == len(lines) - 1 else 1)
    hr(doc)
    table(doc, ["항목", "내용"], meta_rows, widths=[3.2, 13.8], size=9.5,
          zebra=True, first_col_bold=True)
