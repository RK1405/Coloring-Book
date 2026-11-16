"""Amazon KDP paperback wraparound cover: back + spine + front, A4 trim.

KDP paperback, black & white interior on white paper:
  spine width = pages x 0.002252 in, bleed = 0.125 in on every outside edge.
For 40 pages at 8.27 x 11.69 in (A4):
  full cover = 0.125 + 8.27 + 0.0901 + 8.27 + 0.125 = 16.88 in wide, 11.94 in tall.
Output: PNG + JPG at 360 DPI and a PDF at the exact size (KDP uploads covers as PDF).
"""
import os, math, textwrap, cairosvg, img2pdf
from PIL import Image
import lib, vehicles

DPI = 360
TRIM_W, TRIM_H = 8.27, 11.69
BLEED = 0.125
PAPER = 0.002252            # in per page, white paper, B&W
SAFE = 0.375                # keep text this far inside the trim
FONT, BODY = 'Fredoka', 'Inter'

BOOKS = {
    'cars_motors': dict(
        pages=40, items=vehicles.BOOK, bg='#8ECAE6', accent='#219EBC', dark='#1b4965',
        author='Zara Krishnann',
        title=['Cars, Trucks', '&amp; MOTORS', 'Coloring Book'],
        tagline="Vroom! Let's Color!",
        blurb=[
            "Start your engines! This fun coloring book is packed with 20 friendly "
            "vehicles for kids aged 3 to 8.",
            "Race cars, fire trucks, police cars, school buses, tractors, monster trucks, "
            "an ice cream truck and many more are waiting for your colors.",
        ],
        bullets=[
            "20 big, simple pictures with thick, bold outlines",
            "One picture per page with a blank back, so markers won't bleed through",
            "A small color guide on every page to inspire young artists",
            "Large 8.27 x 11.69 in (A4) pages, easy for small hands",
        ],
        closing="A great gift for birthdays, holidays and road trips!",
        peek=['Monster Truck', 'Fire Truck', 'Tractor'],
        hero='Race Car', cards=['Police Car', 'School Bus', 'Taxi'],
    ),
}


def px(inches):
    return inches * DPI


def art(items, name, mode, x, y, s):
    fn = dict(items)[name]
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" viewBox="0 0 400 400">{lib.svg_drawing(fn, mode)}</svg>'


def text(x, y, s, size, fill='#fff', stroke='#1a1a1a', sw=0, family=FONT, weight=700, anchor='middle', extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" stroke-linejoin="round"' if sw else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}"{st} {extra}>{s}</text>')


def dots(x0, w, h, seed):
    return ''.join(f'<circle cx="{x0 + (i*397 + seed) % w:.0f}" cy="{(i*613 + seed*3) % h:.0f}" '
                   f'r="{40 + (i % 3)*25}" fill="#fff" opacity="0.22"/>' for i in range(46))


def front(b, W, H):
    """front panel, coordinates relative to its trim box (W x H px)"""
    it = b['items']
    o = [text(W/2, 470, b['title'][0], 250, sw=26),
         text(W/2, 860, b['title'][1], 420, fill=b['accent'], sw=34, extra='letter-spacing="10"'),
         text(W/2, 1150, b['title'][2], 250, sw=26)]
    cx, cy, cw, ch = 330, 1300, W - 660, 1520
    o += [f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="140" fill="#fff" stroke="#1a1a1a" stroke-width="22"/>',
          art(it, b['hero'], 'color', W/2 - 720, cy + 40, 1440)]
    o += [f'<circle cx="{W-380}" cy="{cy+60}" r="230" fill="#EF476F" stroke="#1a1a1a" stroke-width="18"/>',
          text(W-380, cy+10, 'AGES', 100), text(W-380, cy+170, '3-8', 175)]
    s, gap = 640, 150
    x0 = (W - (3*s + 2*gap)) / 2
    for i, n in enumerate(b['cards']):
        x = x0 + i*(s + gap)
        o += [f'<rect x="{x:.0f}" y="2960" width="{s}" height="{s}" rx="90" fill="#fff" stroke="#1a1a1a" stroke-width="18"/>',
              art(it, n, 'color', x + 30, 2990, s - 60)]
    o += ['<rect x="420" y="3650" width="%d" height="230" rx="115" fill="#fff" stroke="#1a1a1a" stroke-width="18"/>' % (W - 840),
          text(W/2, 3800, '20 Big &amp; Easy Pictures', 125, fill='#1a1a1a'),
          text(W/2, 4010, b['author'], 105, fill=b['dark'], family=FONT)]
    return ''.join(o)


def back(b, W, H):
    it = b['items']
    m = px(SAFE) + 40
    o = [text(W/2, 430, b['tagline'], 260, sw=26)]
    # description card
    lines = []
    for p in b['blurb']:
        lines += textwrap.wrap(p, 54) + ['']
    bl = []
    for t in b['bullets']:
        w = textwrap.wrap(t, 50)
        bl.append(w)
    lh, fs = 118, 88
    n_lines = len(lines) + sum(len(w) for w in bl) + 2
    cy, ch = 580, n_lines * lh + 60
    o.append(f'<rect x="{m}" y="{cy}" width="{W - 2*m:.0f}" height="{ch}" rx="110" fill="#fff" stroke="#1a1a1a" stroke-width="18"/>')
    y = cy + 170
    tx = m + 110
    for ln in lines:
        if ln:
            o.append(text(tx, y, ln, fs, fill='#1a1a1a', family=BODY, weight=500, anchor='start'))
        y += lh if ln else lh * 0.5
    o.append(text(tx, y, 'Inside you will find:', fs + 6, fill=b['dark'], family=FONT, anchor='start'))
    y += lh
    for w in bl:
        o.append(f'<path d="{lib.star(tx + 34, y - 30, 34, 15)}" fill="#FFD23F" stroke="#1a1a1a" stroke-width="6" stroke-linejoin="round"/>')
        for k, ln in enumerate(w):
            o.append(text(tx + 110, y, ln, fs, fill='#1a1a1a', family=BODY, weight=500, anchor='start'))
            y += lh
    y += lh * 0.4
    o.append(text(tx, y, b['closing'], fs + 6, fill=b['dark'], family=FONT, anchor='start'))
    # peek inside (line art, as the child will see it)
    py = cy + ch + 170
    o.append(text(W/2, py, 'A peek inside', 140, sw=18))
    s, gap = 600, 120
    x0 = (W - (3*s + 2*gap)) / 2
    for i, n in enumerate(b['peek']):
        x = x0 + i*(s + gap)
        o += [f'<rect x="{x:.0f}" y="{py + 80}" width="{s}" height="{s}" rx="80" fill="#fff" stroke="#1a1a1a" stroke-width="16"/>',
              art(it, n, 'line', x + 40, py + 120, s - 80)]
    # bottom left: age badge + author. Bottom right is left clear for the KDP barcode (2 x 1.2 in).
    o += [f'<circle cx="{m + 170}" cy="{H - m - 170}" r="170" fill="#EF476F" stroke="#1a1a1a" stroke-width="16"/>',
          text(m + 170, H - m - 205, 'AGES', 74), text(m + 170, H - m - 85, '3-8', 130),
          text(m + 400, H - m - 175, b['author'], 105, fill=b['dark'], anchor='start'),
          text(m + 400, H - m - 60, 'Kids Coloring Books', 80, fill='#1a1a1a', family=BODY, weight=500, anchor='start')]
    return ''.join(o)


def build(key, outdir):
    b = BOOKS[key]
    spine = b['pages'] * PAPER
    Wi = 2*BLEED + 2*TRIM_W + spine
    Hi = 2*BLEED + TRIM_H
    W, H = round(px(Wi)), round(px(Hi))
    tw, th = px(TRIM_W), px(TRIM_H)
    bx = px(BLEED)                       # back trim starts here
    sx = bx + tw                         # spine
    fx = sx + px(spine)                  # front trim
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{b["bg"]}"/>{dots(0, W, H, 7)}'
           f'<rect x="{sx:.1f}" y="0" width="{px(spine):.1f}" height="{H}" fill="{b["accent"]}"/>'
           f'<g transform="translate({bx:.1f},{px(BLEED):.1f})">{back(b, tw, th)}</g>'
           f'<g transform="translate({fx:.1f},{px(BLEED):.1f})">{front(b, tw, th)}</g></svg>')
    os.makedirs(outdir, exist_ok=True)
    base = f'{outdir}/{key}_paperback_cover_A4_{b["pages"]}p_{DPI}dpi'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + '.png', output_width=W, output_height=H)
    im = Image.open(base + '.png').convert('RGB')
    im.save(base + '.png', dpi=(DPI, DPI))
    im.save(base + '.jpg', quality=95, dpi=(DPI, DPI))
    with open(base + '.pdf', 'wb') as f:
        f.write(img2pdf.convert(base + '.jpg', layout_fun=img2pdf.get_fixed_dpi_layout_fun((DPI, DPI))))
    print(f'{key}: {Wi:.3f} x {Hi:.3f} in, spine {spine:.4f} in -> {W} x {H} px @ {DPI} dpi')
    return base


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    for k in BOOKS:
        build(k, f'{out}/{k}')
