"""Convierte un PDF de ordenamiento jurídico poblano a Markdown con formato Lex MX.

Uso: python3 -I convert.py ENTRADA.pdf SALIDA.md
"""
import re
import sys
import collections
import warnings

warnings.filterwarnings("ignore")
import pymupdf as fitz

SRC, DST = sys.argv[1], sys.argv[2]
COLS = len(sys.argv) > 3 and sys.argv[3] == "--columnas"
doc = fitz.open(SRC)

# 1. Tamaño de letra del cuerpo (moda ponderada por caracteres)
sizes = collections.Counter()
for page in doc:
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                sizes[round(s["size"], 1)] += len(s["text"].strip())
BODY = sizes.most_common(1)[0][0]

# 2. Recolectar líneas por página
pages = []
for pno, page in enumerate(doc):
    h = page.rect.height
    lines = []
    blocks = page.get_text("dict")["blocks"]
    if COLS:
        xs = sorted({round(b["bbox"][0]) for b in blocks})
        starts = [xs[0]] if xs else []
        for x in xs[1:]:
            if x - starts[-1] > 120:
                starts.append(x)
        def col(b):
            return max(i for i, s0 in enumerate(starts) if b["bbox"][0] >= s0 - 1)
        blocks.sort(key=lambda b: (col(b), b["bbox"][1]))
    for bi, b in enumerate(blocks):
        for l in b.get("lines", []):
            for s in l["spans"]:
                s["text"] = re.sub(r"[\ue000-\uf8ff]", "", s["text"])
            spans = [s for s in l["spans"] if s["text"].strip()]
            if not spans:
                continue
            lines.append({"block": bi, "y": l["bbox"][1], "x": l["bbox"][0],
                          "spans": spans, "h": h})
    # fusionar fragmentos de la misma línea dentro del mismo bloque
    merged = []
    for ln in lines:
        if merged and merged[-1]["block"] == ln["block"] and abs(merged[-1]["y"] - ln["y"]) < 2:
            merged[-1]["spans"] += ln["spans"]
        else:
            merged.append(ln)
    pages.append(merged)


def norm(t):
    return re.sub(r"\d+", "#", re.sub(r"\s+", " ", t)).strip().lower()


def line_text(ln):
    return " ".join(s["text"].strip() for s in ln["spans"]).strip()


# 3. Encabezados y pies repetidos
zone_counts = collections.Counter()
for pg in pages:
    seen = set()
    for ln in pg:
        if ln["y"] < 0.11 * ln["h"] or ln["y"] > 0.89 * ln["h"]:
            seen.add(norm(line_text(ln)))
    zone_counts.update(seen)
npages = len(pages)
repeated = {t for t, c in zone_counts.items() if c >= max(3, 0.2 * npages)}

# 4. Separar notas al pie, marcas de nota y texto
footnotes = {}
body_lines = []  # (texto, y, nueva_pagina)
for pno, pg in enumerate(pages):
    last_fn = None
    first = True
    for ln in pg:
        txt = line_text(ln)
        in_zone = ln["y"] < 0.11 * ln["h"] or ln["y"] > 0.89 * ln["h"]
        if in_zone and (norm(txt) in repeated or re.fullmatch(r"[\d\s\-–]+", txt)):
            continue
        small = all(s["size"] < BODY * 0.85 for s in ln["spans"])
        if small:
            m = re.match(r"^(\d+)\s*(.*)$", txt)
            if m and ln["spans"][0]["size"] < BODY * 0.75:
                last_fn = m.group(1)
                footnotes[last_fn] = m.group(2).strip()
                continue
            if last_fn is not None:
                footnotes[last_fn] += " " + txt
                continue
        parts = []
        for s in ln["spans"]:
            t = s["text"]
            if s["size"] < BODY * 0.8 and re.fullmatch(r"\s*\d+\s*", t) and (s["flags"] & 1 or s["size"] < BODY * 0.7):
                parts.append(f"⟦{t.strip()}⟧")
            else:
                parts.append(t)
        txt = re.sub(r"\s+", " ", " ".join(p.strip() for p in parts)).strip()
        if txt:
            body_lines.append((txt, ln["y"], first))
            first = False

# 5. Armar párrafos
START = re.compile(
    r"^(ART[ÍI]CULO|Art[íi]culo|LIBRO|T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N|TRANSITORIOS?|"
    r"[IVXLC]+\s*[\.\-–]|[a-zñ]\)|\d+\s*\.-)"
)
paras = []
prev_y = None
for txt, y, newpage in body_lines:
    if re.search(r"\.{5,}", txt):  # renglones de índice
        prev_y = y
        continue
    start = bool(START.match(txt))
    if start and paras and re.search(
            r"\b(el|la|los|las|del|al|de|en|y|o|e|que|por|a|con|conforme|según|segun|"
            r"y/o|término|términos|previsto|prevista|dispuesto|establecido|señalado|presente)\s*$",
            paras[-1], re.I) and (prev_y is None or newpage or (y - prev_y) < 17):
        start = False
    gap = (y - prev_y) if (prev_y is not None and not newpage) else None
    if not paras:
        paras.append(txt)
    elif start or (gap is not None and gap > 17) or (gap is not None and gap < -5):
        paras.append(txt)
    elif newpage and re.search(r"[\.:;]$", paras[-1]):
        paras.append(txt)
    elif paras[-1].endswith("-") and txt[:1].islower():
        paras[-1] = paras[-1][:-1] + txt
    else:
        paras[-1] += " " + txt
    prev_y = y


# 7. Clasificar y dar formato
ART = re.compile(
    r"^\s*(?:ART[ÍI]CULO|Art[íi]culo)(?:\s*[\.\-–]*\s*(?=\d)|\s+)((?:\d+[oº°]?|[A-ZÁÉÍÓÚ]{4,}[OA]?)(?:[\s\-]*(?:Bis|BIS|Ter|TER|Qu[aá]ter|QU[AÁ]TER|Quinquies|QUINQUIES|[A-Z](?![a-záéíóú])))*)"
    r"\s*(⟦\d+⟧)?\s*[\.\-–:]*\s*(⟦\d+⟧)?\s*(.*)$"
)
HEAD = [
    (re.compile(r"^(LIBRO|PARTE)\b"), "##"),
    (re.compile(r"^(T[ÍI]TULO)\b"), "##"),
    (re.compile(r"^(TRANSITORIOS?|ART[ÍI]CULOS TRANSITORIOS)\b"), "##"),
    (re.compile(r"^(CAP[ÍI]TULO)\b"), "###"),
    (re.compile(r"^(SECCI[ÓO]N)\b"), "####"),
]

out = []
last_heading = False
for p in paras:
    p = p.strip()
    up = p.upper() == p and any(c.isalpha() for c in p)
    lvl = None
    for rx, mark in HEAD:
        if rx.match(p) and up and len(p) < 200:
            lvl = mark
            break
    if lvl:
        out.append(f"{lvl} {p}")
        last_heading = True
        continue
    if last_heading and up and len(p) < 160 and not ART.match(p):
        out[-1] += " " + p
        continue
    last_heading = False
    m = ART.match(p)
    if m and len(m.group(1)) < 40:
        num = m.group(1).strip()
        marker = (m.group(2) or "") + (m.group(3) or "")
        rest = m.group(4).strip()
        head = f"**Artículo {num}.**{marker}"
        out.append(head + ((" " + rest) if rest else ""))
    else:
        out.append(p)

# recorta tabla de reformas, índice y considerandos previos al artículo 1
a1 = next((i for i, p in enumerate(out) if re.match(r"^\*\*Artículo 1(o|º)?\.\*\*", p)), None)
if a1:
    k = a1
    while k > 0 and a1 - k < 4 and len(out[k - 1]) < 120 and out[k - 1].lstrip("# ").upper() == out[k - 1].lstrip("# ") and "..." not in out[k - 1]:
        k -= 1
    out = out[k:]
text = "\n\n".join(out)
text = re.sub(r"(\*\*Artículo [^*]+\.\*\*(?:⟦\d+⟧)?)\n\n(?!\*\*|#)", r"\1 ", text)

# 8. Sustituir marcas por notas en línea
def fn(m):
    n = m.group(1)
    t = footnotes.get(n)
    return f" *[Nota: {t.strip()}]*" if t else ""

text = re.sub(r"⟦(\d+)⟧", fn, text)
text = re.sub(r"[ \t]+", " ", text)
open(DST, "w").write(text.strip() + "\n")
print(f"{SRC}: cuerpo {BODY}pt, {len(out)} párrafos, {len(footnotes)} notas, "
      f"{len(re.findall(r'^\*\*Artículo', text, re.M))} artículos")
