"""临时：M03 语料形态勘察 4——图片独立性/交叉引用/代码块/定义区/目录段。"""

import collections
import pathlib
import re

root = pathlib.Path("/home/lxx/wrk/AgenticDocer/spec/standards")

IMG_MD = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
XREF = re.compile(
    r"^(?:See|Refer to|refer to|see)\b[^.]{0,120}\b(Section|Chapter|Clause|Table|Figure|Annex|Appendix|Part)\b",
    re.I,
)
EXAMPLE = re.compile(r"^(?:Example|EXAMPLE)\s*\d*\s*[:.\-—]?\s")
GLOSSARY = re.compile(
    r"(?i)^(glossary|terms and acronyms|terms and definitions|terms|definitions|abbreviations|acronyms|"
    r"definitions and abbreviations|list of abbreviations|terminology)\b"
)
NONGLOSS = re.compile(
    r"(?i)^(contents|table of contents|list of tables|list of figures|figures|tables|preface|index|"
    r"revision history|change history|introduction|notice|disclaimer|about this|using this|intended audience)"
)
TOCLINE = re.compile(r"^\s*(?:[A-Z0-9]|Appendix|Chapter|Part|Annex)?[\w.()\-/ ]*\s*\.{3,}\s*\.*\s*\d*\s*$")

tot = collections.Counter()
for f in sorted(root.glob("*/*.md")):
    lines = f.read_text(encoding="utf-8").split("\n")
    c = collections.Counter()
    # 图片行是否独占一行
    for i, l in enumerate(lines, 1):
        for m in IMG_MD.finditer(l):
            rest = IMG_MD.sub("", l).strip()
            if rest:
                c["img_inline"] += 1
                if c["img_inline"] < 4:
                    print("  inline img", f.name, i, repr(l[:110]))
            else:
                c["img_standalone"] += 1
    # 交叉引用段落（独立行且整行匹配）
    for l in lines:
        s = l.strip()
        if s and XREF.match(s):
            c["xref_line"] += 1
    # example 行
    for l in lines:
        s = l.strip()
        if s and EXAMPLE.match(s):
            c["example_line"] += 1
    # 目录行
    for l in lines:
        if TOCLINE.match(l) and "." in l:
            c["toc_line"] += 1
    # glossary 区
    for i, l in enumerate(lines, 1):
        m = re.match(r"^#+ (.*)$", l)
        if m:
            t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if GLOSSARY.match(t):
                c["glossary_head"] += 1
                if c["glossary_head"] < 4:
                    print("  glossary", f.name, i, repr(t[:80]))
    tot.update(c)
    print(f.name, dict(c))
print("TOTAL", dict(tot))
