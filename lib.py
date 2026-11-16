"""Shared drawing helpers + page / book builder for the kids coloring books.

Every drawing is a function returning a list of SVG element strings in a
400 x 400 canvas.  Fills are given as palette names; in "line" mode every fill
becomes white (except solid black 'k'), giving clean colouring-page line art.
In "color" mode the palette is used (for the reference thumbnail + covers).
"""
import math, os, io
import cairosvg

PAL = {
    'k': '#1a1a1a', 'w': '#ffffff', 'y': '#FFD23F', 'o': '#FF9F1C', 'r': '#EF476F',
    'red': '#E63946', 'pk': '#FFAFCC', 'lpk': '#FFD6E8', 'p': '#B388EB', 'lp': '#D9C2FF',
    'b': '#4EA8DE', 'lb': '#A2D2FF', 'db': '#3A6EA5', 'g': '#80C66E', 'lg': '#B9E4A8',
    'dg': '#4E9A51', 'br': '#B5835A', 'lbr': '#E3C7A2', 'dbr': '#8A5A3B', 'gr': '#A8A8B3',
    'lgr': '#DADAE3', 'dgr': '#6B6B78', 'cr': '#FFF3D6', 'tan': '#F2D0A4', 'sky': '#CDEFFF',
    'teal': '#4CC9B0', 'gold': '#F4C430', 'none': 'none',
}

MODE = {'m': 'color'}
SW = 7      # main stroke width (in 400-unit canvas)
SW2 = 5     # detail strokes


def fc(f):
    if f == 'none':
        return 'none'
    if MODE['m'] == 'line':
        return PAL['k'] if f == 'k' else '#ffffff'
    return PAL.get(f, f)


def _st(sw):
    return f'stroke="#1a1a1a" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'


def C(cx, cy, r, f='w', sw=SW):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fc(f)}" {_st(sw)}/>'


def E(cx, cy, rx, ry, f='w', rot=0, sw=SW):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fc(f)}" {_st(sw)}{t}/>'


def R(x, y, w, h, f='w', rx=0, sw=SW, rot=0):
    t = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fc(f)}" {_st(sw)}{t}/>'


def P(d, f='w', sw=SW, extra=''):
    return f'<path d="{d}" fill="{fc(f)}" {_st(sw)} {extra}/>'


def L(d, sw=SW2):
    """open line, never filled"""
    return f'<path d="{d}" fill="none" {_st(sw)}/>'


def G(items, tf):
    return f'<g transform="{tf}">' + ''.join(items) + '</g>'


def blush(x, y, rx=14, ry=8):
    if MODE['m'] == 'line':
        return ''
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#FF8FAB" opacity="0.7"/>'


def eye(x, y, s=1.0, look=(0, 0)):
    """big cartoon eye: black pupil with white sparkle"""
    lx, ly = look
    return (f'<ellipse cx="{x}" cy="{y}" rx="{11*s}" ry="{14*s}" fill="{PAL["k"]}"/>'
            f'<circle cx="{x - 3*s + lx}" cy="{y - 5*s + ly}" r="{4.2*s}" fill="#fff"/>')


def smile(x, y, w=16, h=10, sw=SW2):
    return L(f'M{x-w},{y} Q{x},{y+h*2} {x+w},{y}', sw)


def open_smile(x, y, w=16, h=14):
    return P(f'M{x-w},{y} Q{x},{y+h*2.2} {x+w},{y} Z', 'r', SW2)


def star(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append(f'{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + ' Z'


def petals(cx, cy, n, dist, rx, ry, f, rot0=0, sw=SW):
    out = []
    for i in range(n):
        a = rot0 + i * 360 / n
        x = cx + dist * math.cos(math.radians(a))
        y = cy + dist * math.sin(math.radians(a))
        out.append(E(f'{x:.1f}', f'{y:.1f}', rx, ry, f, rot=f'{a:.1f}', sw=sw))
    return out


def wheel(cx, cy, r, f='dgr', hub='lgr'):
    return [C(cx, cy, r, f), C(cx, cy, r * 0.45, hub, SW2)]


def ground(y=372, x1=40, x2=360):
    return L(f'M{x1},{y} L{x2},{y}', SW2)


# ---------------------------------------------------------------- rendering
def svg_drawing(fn, mode):
    MODE['m'] = mode
    def flat(xs):
        for x in xs:
            if isinstance(x, (list, tuple)):
                yield from flat(x)
            elif x:
                yield x
    body = ''.join(flat(fn()))
    return body


def drawing_svg_doc(fn, mode, size=1000):
    body = svg_drawing(fn, mode)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 400 400"><rect width="400" height="400" fill="#fff"/>{body}</svg>')


# A4 page in mm
PW, PH = 210, 297
M = 15            # safe margin (KDP no-bleed: >= 9.6mm inside, 6.4mm outside)
FONT = "Fredoka"


def page_svg(title, fn):
    """Layout mirroring the reference: framed page, colour thumbnail top-left,
    outlined title on the right, big outline picture below."""
    color = svg_drawing(fn, 'color')
    line = svg_drawing(fn, 'line')
    x0, y0, w, h = M, M, PW - 2 * M, PH - 2 * M
    hh = 46                      # header height
    thumb = hh - 6
    fs = 22 if len(title) <= 9 else (18 if len(title) <= 13 else 14.5)
    tx = x0 + hh + (w - hh) / 2
    big = min(w - 10, h - hh - 10)
    bx = x0 + (w - big) / 2
    by = y0 + hh + (h - hh - big) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">
<rect width="{PW}" height="{PH}" fill="#fff"/>
<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="6" fill="none" stroke="#1a1a1a" stroke-width="1.4"/>
<line x1="{x0}" y1="{y0+hh}" x2="{x0+w}" y2="{y0+hh}" stroke="#1a1a1a" stroke-width="1.1"/>
<line x1="{x0+hh}" y1="{y0}" x2="{x0+hh}" y2="{y0+hh}" stroke="#1a1a1a" stroke-width="1.1"/>
<svg x="{x0+3}" y="{y0+3}" width="{thumb}" height="{thumb}" viewBox="0 0 400 400">{color}</svg>
<text x="{tx}" y="{y0 + hh/2}" font-family="{FONT}" font-weight="700" font-size="{fs}" text-anchor="middle"
 dominant-baseline="central" letter-spacing="1" fill="#fff" stroke="#1a1a1a" stroke-width="0.9"
 stroke-linejoin="round">{title.upper()}</text>
<svg x="{bx}" y="{by}" width="{big}" height="{big}" viewBox="0 0 400 400">{line}</svg>
</svg>'''


BLANK = f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}"><rect width="{PW}" height="{PH}" fill="#fff"/></svg>'


def build_book(name, items, outdir):
    """items: list of (title, fn); 20 items -> 40 pages (picture on every
    right-hand page, its back left blank so markers never bleed through)."""
    from pypdf import PdfWriter, PdfReader
    os.makedirs(f'{outdir}/png_pages', exist_ok=True)
    os.makedirs(f'{outdir}/line_art', exist_ok=True)
    os.makedirs(f'{outdir}/color_ref', exist_ok=True)
    writer = PdfWriter()
    blank_pdf = cairosvg.svg2pdf(bytestring=BLANK.encode())
    for i, (title, fn) in enumerate(items, 1):
        svg = page_svg(title, fn)
        writer.append(PdfReader(io.BytesIO(cairosvg.svg2pdf(bytestring=svg.encode()))))
        writer.append(PdfReader(io.BytesIO(blank_pdf)))
        slug = f'{i:02d}_{title.lower().replace(" ", "_")}'
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f'{outdir}/png_pages/{slug}.png',
                         output_width=2480, output_height=3508)   # A4 @ 300 dpi
        cairosvg.svg2png(bytestring=drawing_svg_doc(fn, 'line').encode(),
                         write_to=f'{outdir}/line_art/{slug}.png', output_width=2400, output_height=2400)
        cairosvg.svg2png(bytestring=drawing_svg_doc(fn, 'color').encode(),
                         write_to=f'{outdir}/color_ref/{slug}.png', output_width=1200, output_height=1200)
    with open(f'{outdir}/{name}_interior_A4.pdf', 'wb') as f:
        writer.write(f)
    return len(writer.pages)


def contact_sheet(items, path, mode='line'):
    cols, cell = 5, 300
    rows = math.ceil(len(items) / cols)
    parts = []
    for i, (t, fn) in enumerate(items):
        x, y = (i % cols) * cell, (i // cols) * (cell + 30)
        parts.append(f'<svg x="{x}" y="{y}" width="{cell}" height="{cell}" viewBox="0 0 400 400">{svg_drawing(fn, mode)}</svg>'
                     f'<text x="{x+cell/2}" y="{y+cell+20}" font-family="{FONT}" font-size="18" text-anchor="middle">{t}</text>')
    W, H = cols * cell, rows * (cell + 30)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/>{"".join(parts)}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path)
