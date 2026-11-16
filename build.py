import os, cairosvg, lib
import animals, flowers, vehicles, household
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
BOOKS = [
    ('animals', 'Animals', ['My First', 'ANIMALS', 'Coloring Book'], '#FFB703', '#FB8500', animals.BOOK, 0),
    ('flowers', 'Flowers', ['My First', 'FLOWERS', 'Coloring Book'], '#FFAFCC', '#E05780', flowers.BOOK, 0),
    ('cars_motors', 'Cars & Motors', ['Cars, Trucks', '&amp; MOTORS', 'Coloring Book'], '#8ECAE6', '#219EBC', vehicles.BOOK, 0),
    ('household', 'Household Items', ['Around the', 'HOUSE', 'Coloring Book'], '#B9E4A8', '#4E9A51', household.BOOK, 0),
]


def cover_svg(lines, bg, accent, items):
    W, H = 1600, 2560
    hero_t, hero = items[0]
    small = items[1:7]
    def img(fn, x, y, s):
        return f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 400 400">{lib.svg_drawing(fn, "color")}</svg>'
    dots = ''.join(f'<circle cx="{(i*137)%W}" cy="{(i*251)%H}" r="{18 + (i%3)*10}" fill="#fff" opacity="0.25"/>' for i in range(40))
    cards = ''
    pos = [(110, 1720), (590, 1720), (1070, 1720)]
    for (t, fn), (x, y) in zip(small[:3], pos):
        cards += f'<rect x="{x}" y="{y}" width="420" height="420" rx="60" fill="#fff" stroke="#1a1a1a" stroke-width="10"/>' + img(fn, x + 30, y + 30, 360)
    big = (f'<rect x="250" y="700" width="1100" height="960" rx="90" fill="#fff" stroke="#1a1a1a" stroke-width="12"/>'
           + img(hero[1] if isinstance(hero, tuple) else hero, 340, 700, 920))
    title = (
        f'<text x="800" y="200" font-family="Fredoka" font-weight="700" font-size="130" text-anchor="middle" fill="#fff" stroke="#1a1a1a" stroke-width="14" paint-order="stroke" stroke-linejoin="round">{lines[0]}</text>'
        f'<text x="800" y="420" font-family="Fredoka" font-weight="700" font-size="{230 if len(lines[1].replace('&amp;', '&')) <= 8 else 190}" text-anchor="middle" fill="{accent}" stroke="#1a1a1a" stroke-width="18" paint-order="stroke" stroke-linejoin="round" letter-spacing="6">{lines[1]}</text>'
        f'<text x="800" y="590" font-family="Fredoka" font-weight="700" font-size="130" text-anchor="middle" fill="#fff" stroke="#1a1a1a" stroke-width="14" paint-order="stroke" stroke-linejoin="round">{lines[2]}</text>')
    badge = ('<circle cx="1360" cy="760" r="150" fill="#EF476F" stroke="#1a1a1a" stroke-width="10"/>'
             '<text x="1360" y="725" font-family="Fredoka" font-weight="700" font-size="56" text-anchor="middle" fill="#fff">AGES</text>'
             '<text x="1360" y="810" font-family="Fredoka" font-weight="700" font-size="96" text-anchor="middle" fill="#fff">3-8</text>')
    foot = ('<rect x="200" y="2240" width="1200" height="180" rx="90" fill="#fff" stroke="#1a1a1a" stroke-width="10"/>'
            '<text x="800" y="2352" font-family="Fredoka" font-weight="700" font-size="76" text-anchor="middle" fill="#1a1a1a">20 Big &amp; Easy Pictures</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{dots}{title}{big}{badge}{cards}{foot}</svg>')


def main():
    for key, name, lines, bg, accent, items, _ in BOOKS:
        d = f'{OUT}/{key}'
        n = lib.build_book(key, items, d)
        svg = cover_svg(lines, bg, accent, [(t, f) for t, f in items])
        png = f'{d}/{key}_kindle_cover.png'
        cairosvg.svg2png(bytestring=svg.encode(), write_to=png)
        Image.open(png).convert('RGB').save(f'{d}/{key}_kindle_cover_1600x2560.jpg', quality=95, dpi=(300, 300))
        os.remove(png)
        lib.contact_sheet(items, f'{d}/{key}_preview_contact_sheet.png', 'line')
        print(key, n, 'pages')


if __name__ == '__main__':
    main()
