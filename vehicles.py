"""Cars & motors: friendly original vehicles. Faces sit in the headlight +
bumper (not windscreen eyes) so the style stays clearly original."""
from lib import *


def tube(d, w, f):
    return [P(d, 'none', w + 2 * SW), P(d, 'none', w).replace('#1a1a1a', fc(f))]


def T(x, y, txt, size=28, f='w', sw=4):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-weight="700" font-size="{size}" text-anchor="middle" '
            f'dominant-baseline="central" fill="{fc(f)}" stroke="#1a1a1a" stroke-width="{sw}" paint-order="stroke" '
            f'stroke-linejoin="round">{txt}</text>')


def lamp_eye(x, y, r=17):
    return [C(x, y, r, 'cr', SW2), eye(x, y + 1, 0.8)]


def bumper_smile(x, y, w=14):
    return smile(x, y, w, 6)


def wheels(*xs, y=310, r=36):
    out = []
    for x in xs:
        out += wheel(x, y, r)
    return out


def sky():
    out = [C(56, 56, 22, 'y', SW2)]
    for a in range(0, 360, 45):
        out.append(L(f'M{56 + 30*math.cos(math.radians(a)):.0f},{56 + 30*math.sin(math.radians(a)):.0f} L{56 + 42*math.cos(math.radians(a)):.0f},{56 + 42*math.sin(math.radians(a)):.0f}', 4))
    out.append(P('M250,76 C236,76 236,56 252,56 C254,38 282,34 290,50 C300,38 324,44 322,60 C340,60 340,76 324,76 Z', 'w', SW2))
    return out


def road(y=348):
    return L(f'M20,{y} L380,{y}', SW2)


SEDAN = ('M36,300 L36,252 Q36,232 66,228 L118,222 L158,172 Q166,162 186,162 L268,162 Q288,162 298,176 '
         'L332,222 L350,226 Q370,232 370,262 L370,300 Z')


def sedan(f, extra=()):
    return [road(), P(SEDAN, f),
            P('M134,222 L170,180 L222,180 L222,222 Z', 'sky', SW2), P('M238,180 L284,180 L312,222 L238,222 Z', 'sky', SW2),
            L('M230,170 L230,298', SW2), R(244, 236, 22, 8, 'gr', 4, 4), R(176, 236, 22, 8, 'gr', 4, 4),
            R(26, 276, 26, 16, 'gr', 6, SW2), R(352, 276, 26, 16, 'gr', 6, SW2)] + list(extra) + \
        wheels(110, 300) + lamp_eye(350, 250) + [bumper_smile(340, 270, 10), blush(318, 266, 8, 5)]


def race_car():
    return [road(), L('M8,250 l40,0 M14,272 l30,0 M20,228 l24,0', 4),
            R(52, 182, 14, 60, 'dgr', 4, SW2), R(40, 172, 58, 18, 'red', 6, SW2),
            P('M50,290 L54,236 L150,224 L190,190 L250,190 L272,226 L350,246 Q376,254 374,290 Z', 'red'),
            C(222, 186, 26, 'y', SW), P('M200,186 L246,186 L246,196 L200,196 Z', 'k', 3),
            C(140, 256, 24, 'w', SW2), T(140, 258, '7', 30, 'w', 0).replace('stroke-width="0"', 'stroke-width="0"').replace('fill="#ffffff"', 'fill="#1a1a1a"'),
            L('M190,262 L320,262', SW2)] + wheels(100, 300, y=296, r=38) + lamp_eye(352, 262, 14) + [bumper_smile(352, 282, 9)]


def police_car():
    return sedan('w', [R(180, 144, 90, 18, 'w', 6, SW2), R(182, 146, 40, 14, 'b', 5, 0), R(228, 146, 40, 14, 'red', 5, 0),
                       R(180, 144, 90, 18, 'none', 6, SW2),
                       P('M36,262 L370,262 L370,284 L36,284 Z', 'db', SW2), P(star(170, 250, 14, 6), 'gold', 4)])


def fire_truck():
    out = [road(), R(30, 180, 230, 116, 'red', 10), P('M260,296 L260,150 L320,150 Q338,150 346,170 L370,226 L370,296 Z', 'red'),
           P('M272,164 L318,164 L340,222 L272,222 Z', 'sky', SW2),
           R(40, 150, 210, 18, 'lgr', 4, SW2)]
    for x in range(56, 250, 26):
        out.append(L(f'M{x},150 L{x},168', 4))
    out += [R(46, 200, 60, 50, 'gr', 6, SW2), C(76, 225, 14, 'lgr', 4), R(120, 200, 120, 50, 'gr', 6, SW2),
            L('M140,200 L140,250 M160,200 L160,250 M180,200 L180,250 M200,200 L200,250 M220,200 L220,250', 3),
            R(286, 132, 26, 18, 'b', 6, SW2), L('M30,262 L370,262', SW2)]
    out += wheels(90, 200, 316) + lamp_eye(352, 246) + [bumper_smile(346, 278, 10)]
    return out


def taxi():
    return sedan('y', [R(200, 136, 60, 26, 'y', 6, SW2), T(230, 150, 'TAXI', 15, 'w', 3)] +
                 [R(36 + i * 22, 262, 11, 11, 'k' if i % 2 == 0 else 'w', 0, 2) for i in range(15)])


def school_bus():
    out = [road(), P('M24,300 L24,120 Q24,100 44,100 L320,100 Q346,100 352,124 L372,210 L374,300 Z', 'y')]
    for x in (40, 102, 164, 226):
        out.append(R(x, 120, 50, 54, 'sky', 6, SW2))
    out += [P('M290,120 L330,120 Q340,120 344,134 L358,190 L290,190 Z', 'sky', SW2),
            R(290, 196, 50, 100, 'none', 4, SW2), L('M315,196 L315,296', 4),
            L('M24,194 L290,194 M24,230 L290,230', SW2), T(150, 212, 'SCHOOL BUS', 22, 'w', 3),
            R(10, 270, 24, 18, 'gr', 6, SW2), R(358, 270, 26, 18, 'gr', 6, SW2), R(-6, 0, 0, 0, 'none', 0, 0)]
    out += wheels(90, 286, y=306) + lamp_eye(356, 240, 14) + [bumper_smile(352, 262, 9)]
    return out


def monster_truck():
    out = [road(354), R(120, 220, 180, 40, 'dgr', 8, SW2),
           L('M150,260 L150,280 M270,260 L270,280', 10)]
    for x in (100, 300):
        out += [C(x, 290, 62, 'dgr'), C(x, 290, 30, 'lgr', SW2), C(x, 290, 10, 'gr', 4)]
        for a in range(0, 360, 30):
            out.append(L(f'M{x + 56*math.cos(math.radians(a)):.0f},{290 + 56*math.sin(math.radians(a)):.0f} '
                         f'L{x + 64*math.cos(math.radians(a)):.0f},{290 + 64*math.sin(math.radians(a)):.0f}', 6))
    out += [P('M40,220 L40,170 L150,160 L180,110 L270,110 L300,160 L360,170 Q376,174 376,200 L376,220 Z', 'g'),
            P('M190,124 L262,124 L282,160 L170,160 Z', 'sky', SW2), L('M226,124 L226,160', SW2),
            P(star(110, 190, 18, 8), 'y', 4), R(140, 96, 120, 14, 'gr', 6, SW2), C(160, 96, 6, 'y', 3), C(240, 96, 6, 'y', 3)]
    out += lamp_eye(354, 190, 14) + [bumper_smile(352, 210, 8)]
    return out


def tractor():
    return [road(356), R(300, 80, 14, 70, 'dgr', 4, SW2), P('M296,80 L318,80 L314,70 L300,70 Z', 'dgr', 4),
            P('M60,250 L60,150 L190,150 L190,250 Z', 'r'), P('M70,80 L180,80 L190,150 L60,150 Z', 'sky'),
            R(54, 70, 146, 18, 'r', 6), L('M125,88 L125,150', SW2),
            P('M190,170 L330,170 Q360,172 360,200 L360,260 L190,260 Z', 'r'),
            L('M210,186 L340,186 M210,200 L340,200 M210,214 L340,214', 4)] + \
        [C(120, 280, 74, 'dgr'), C(120, 280, 34, 'y', SW2), C(120, 280, 10, 'dgr', 4)] + \
        [L(f'M{120 + 66*math.cos(math.radians(a)):.0f},{280 + 66*math.sin(math.radians(a)):.0f} L{120 + 78*math.cos(math.radians(a)):.0f},{280 + 78*math.sin(math.radians(a)):.0f}', 8) for a in range(0, 360, 30)] + \
        [C(310, 310, 42, 'dgr'), C(310, 310, 20, 'y', SW2)] + lamp_eye(350, 228, 13) + [bumper_smile(346, 248, 8)]


def dump_truck():
    return [road(), R(30, 240, 330, 40, 'gr', 6),
            P('M30,240 L10,130 L230,120 L230,240 Z', 'o'),
            L('M60,140 L72,232 M110,136 L118,232 M160,132 L164,232 M200,128 L200,232', SW2),
            P('M8,120 L50,96 L80,110 L120,92 L160,104 L200,88 L234,112 L230,124 L10,132 Z', 'br', SW2),
            P('M240,280 L240,150 L310,150 Q330,150 340,170 L366,226 L366,280 Z', 'y'),
            P('M254,164 L306,164 L332,222 L254,222 Z', 'sky', SW2)] + \
        wheels(80, 160, 310, y=310, r=34) + lamp_eye(348, 246, 13) + [bumper_smile(344, 266, 8)]


def ambulance():
    return [road(), P('M24,300 L24,130 Q24,116 40,116 L270,116 L270,300 Z', 'w'),
            P('M270,300 L270,150 L314,150 Q334,150 344,170 L372,230 L372,300 Z', 'w'),
            P('M282,162 L312,162 L340,222 L282,222 Z', 'sky', SW2),
            R(118, 140, 80, 80, 'w', 0, 0), P('M140,150 h36 v26 h26 v36 h-26 v26 h-36 v-26 h-26 v-36 h26 Z', 'red', SW2),
            R(220, 96, 40, 20, 'b', 6, SW2), R(40, 140, 50, 40, 'sky', 6, SW2),
            L('M24,240 L372,240', SW2), L('M24,256 L372,256', SW2).replace('fill="none"', 'fill="none"'),
            R(10, 276, 24, 16, 'gr', 6, SW2), R(360, 276, 24, 16, 'gr', 6, SW2)] + \
        wheels(90, 300) + lamp_eye(352, 266 - 18, 13) + [bumper_smile(346, 270, 8)]


def motorbike():
    return [road(), C(90, 290, 54, 'dgr'), C(90, 290, 26, 'lgr', SW2), C(310, 290, 54, 'dgr'), C(310, 290, 26, 'lgr', SW2),
            tube('M310,290 L270,170', 12, 'gr'), tube('M90,290 L160,240', 10, 'gr'),
            P('M130,230 C150,200 200,196 250,210 L270,250 C230,270 170,270 130,250 Z', 'red'),
            P('M150,214 C150,186 200,186 210,206 Z', 'b', SW2),
            P('M92,226 C100,200 160,200 160,220 L140,232 Z', 'k', SW2),
            R(160, 254, 70, 30, 'lgr', 8, SW2), L('M236,262 L290,254', 6),
            tube('M60,250 C80,230 120,232 140,240', 10, 'dgr'),
            L('M262,166 L250,140 M262,166 L288,150', 8)] + lamp_eye(282, 192, 15) + [bumper_smile(270, 228, 8)]


def scooter():
    return [road(), C(100, 300, 40, 'dgr'), C(100, 300, 18, 'lgr', SW2), C(300, 300, 40, 'dgr'), C(300, 300, 18, 'lgr', SW2),
            P('M60,290 C60,220 120,200 180,220 L240,270 L290,270 C290,240 280,200 270,140 L290,138 C310,200 330,260 330,290 Z', 'teal'),
            P('M70,210 C80,180 170,180 176,204 C150,214 90,216 70,210 Z', 'br'),
            P('M60,290 C60,250 90,240 140,250 C140,270 120,290 100,290 Z', 'teal', SW2),
            L('M262,130 L250,110 M262,130 L300,118', 8), C(250, 108, 8, 'k', 0)] + lamp_eye(290, 170, 15) + [bumper_smile(304, 240, 8)]


def jeep():
    return [road(), C(42, 236, 34, 'dgr'), C(42, 236, 16, 'lgr', SW2),
            P('M50,300 L50,200 L110,200 L120,140 L260,140 L270,200 L350,206 Q370,208 370,230 L370,300 Z', 'g'),
            R(130, 152, 60, 46, 'sky', 4, SW2), R(200, 152, 58, 46, 'sky', 4, SW2),
            L('M120,140 L114,120 M262,140 L268,120 M114,120 L268,120', SW2),
            L('M196,200 L196,296', SW2), R(210, 214, 22, 8, 'gr', 4, 4),
            P('M36,296 L380,296 L380,312 L36,312 Z', 'dgr', SW2)] + wheels(110, 300, y=312, r=38) + lamp_eye(350, 238, 13) + [bumper_smile(346, 262, 8)]


def tow_truck():
    return [road(), R(30, 254, 210, 36, 'gr', 6),
            tube('M70,250 L130,130', 14, 'y'), L('M130,130 L40,150 L40,210', 4), P('M40,210 q0,24 -16,18', 'none', 6),
            R(110, 230, 50, 26, 'y', 4, SW2),
            P('M230,300 L230,140 L310,140 Q330,140 340,160 L370,226 L370,300 Z', 'o'),
            P('M244,154 L306,154 L332,220 L244,220 Z', 'sky', SW2), R(260, 120, 40, 20, 'y', 6, SW2)] + \
        wheels(90, 300) + lamp_eye(352, 248, 13) + [bumper_smile(346, 270, 8)]


def cement_mixer():
    return [road(), R(30, 250, 330, 40, 'gr', 6),
            P('M40,230 C30,170 80,120 160,120 L230,140 L230,240 L60,250 Z', 'o'),
            L('M80,130 C110,170 120,220 110,246 M140,120 C170,160 180,210 172,246 M196,128 C214,160 220,200 214,240', SW2),
            P('M230,140 L250,150 L250,230 L230,240 Z', 'dgr', SW2), P('M250,170 L270,190 L250,210 Z', 'gr', 4),
            P('M250,300 L250,150 L310,150 Q330,150 340,170 L366,226 L366,300 Z', 'b'),
            P('M262,164 L306,164 L332,222 L262,222 Z', 'sky', SW2)] + \
        wheels(80, 170, 310) + lamp_eye(350, 248, 13) + [bumper_smile(346, 270, 8)]


def pickup():
    return [road(), P('M30,300 L30,210 L170,210 L170,140 L270,140 Q290,140 300,160 L320,208 L352,214 Q372,218 372,244 L372,300 Z', 'b'),
            P('M184,154 L264,154 Q276,154 282,166 L298,208 L184,208 Z', 'sky', SW2), L('M234,154 L234,296', SW2),
            L('M30,230 L170,230', SW2), R(40, 196, 40, 20, 'br', 4, SW2), R(90, 186, 40, 30, 'o', 4, SW2),
            R(248, 222, 22, 8, 'gr', 4, 4), R(20, 280, 24, 16, 'gr', 6, SW2)] + \
        wheels(100, 300) + lamp_eye(352, 244, 14) + [bumper_smile(346, 268, 9)]


def vintage_car():
    return [road(), P('M30,280 C30,240 70,236 110,240 L110,170 Q110,140 140,140 L240,140 Q262,140 264,170 L268,230 L330,236 C370,240 372,260 372,280 Z', 'p'),
            R(130, 158, 50, 56, 'sky', 6, SW2), R(196, 158, 52, 56, 'sky', 6, SW2),
            P('M40,300 C40,250 140,250 150,300 Z', 'p'), P('M250,300 C250,250 350,250 360,300 Z', 'p'),
            L('M150,286 L250,286', SW), R(330, 220, 14, 30, 'gold', 6, 4), R(100, 120, 170, 22, 'lp', 10, SW2)] + \
        wheels(95, 305, y=306, r=34) + lamp_eye(356, 252, 13) + [bumper_smile(352, 272, 7)]


def sports_car():
    return [road(), P('M30,296 L34,244 Q36,228 60,224 L130,212 L190,170 Q200,164 220,164 L262,166 Q280,168 300,190 L356,224 Q378,236 374,296 Z', 'o'),
            P('M150,214 L196,182 L236,180 L236,214 Z', 'sky', SW2), P('M248,180 L268,182 Q280,186 290,200 L298,214 L248,214 Z', 'sky', SW2),
            P('M34,236 L20,214 L60,214 L60,226 Z', 'o', SW2), L('M60,258 L330,250', SW2), L('M150,276 l60,0', 4)] + \
        wheels(98, 300, y=300, r=36) + lamp_eye(352, 246, 13) + [bumper_smile(352, 270, 8)]


def camper_van():
    return [road(), P('M24,300 L24,130 Q24,100 54,100 L290,100 Q320,100 330,130 L356,200 Q374,206 374,230 L374,300 Z', 'lb'),
            P('M24,200 L374,200 L374,224 L24,224 Z', 'w', SW2),
            R(50, 122, 60, 50, 'sky', 8, SW2), R(130, 122, 60, 50, 'sky', 8, SW2), L('M60,128 L60,166 M80,128 L80,166', 3),
            P('M240,122 L300,122 Q312,122 318,134 L338,190 L240,190 Z', 'sky', SW2), R(200, 122, 30, 170, 'none', 6, SW2),
            P('M44,90 L210,90 L200,100 L54,100 Z', 'o', SW2), R(70, 70, 120, 20, 'br', 4, SW2)] + \
        wheels(90, 300) + lamp_eye(354, 248, 13) + [bumper_smile(350, 270, 8)]


def ice_cream_truck():
    return [road(), P('M24,300 L24,130 L260,130 L260,300 Z', 'lpk'),
            P('M260,300 L260,160 L310,160 Q330,160 340,178 L370,232 L370,300 Z', 'pk'),
            P('M274,174 L308,174 L332,222 L274,222 Z', 'sky', SW2),
            P('M24,130 L44,110 L240,110 L260,130 Z', 'w', SW2),
            R(50, 150, 130, 70, 'sky', 6, SW2), P('M44,150 L190,150 L180,166 L168,150 L156,166 L144,150 L132,166 L120,150 L108,166 L96,150 L84,166 L72,150 L60,166 L48,150 Z', 'y', 4),
            P('M120,100 L106,60 L134,60 Z', 'tan', SW2), C(120, 52, 18, 'pk', SW2), C(120, 34, 8, 'red', 4),
            L('M110,74 L128,64 M114,86 L126,80', 3), T(140, 250, 'ICE CREAM', 22, 'w', 3)] + \
        wheels(80, 300) + lamp_eye(354, 252, 13) + [bumper_smile(350, 274, 8)]


def garbage_truck():
    return [road(), P('M24,290 L24,130 Q24,110 46,110 L240,110 L240,290 Z', 'g'),
            L('M24,160 L240,160 M24,210 L240,210', SW2), P('M24,130 L8,130 L8,280 L24,280', 'gr', SW2),
            P('M110,250 a30,30 0 1,1 30,0', 'none', SW2), P('M136,246 l6,10 l-10,0 Z', 'k', 3),
            R(26, 224, 50, 50, 'gr', 6, SW2), L('M40,224 L40,274 M60,224 L60,274', 3),
            P('M240,300 L240,150 L310,150 Q330,150 340,170 L366,226 L366,300 Z', 'lg'),
            P('M254,164 L306,164 L332,222 L254,222 Z', 'sky', SW2)] + \
        wheels(80, 180, 310) + lamp_eye(348, 248, 13) + [bumper_smile(344, 270, 8)]


BOOK = [('Race Car', race_car), ('Police Car', police_car), ('Fire Truck', fire_truck), ('Taxi', taxi),
        ('School Bus', school_bus), ('Monster Truck', monster_truck), ('Tractor', tractor), ('Dump Truck', dump_truck),
        ('Ambulance', ambulance), ('Motorbike', motorbike), ('Scooter', scooter), ('Jeep', jeep), ('Tow Truck', tow_truck),
        ('Cement Mixer', cement_mixer), ('Pickup Truck', pickup), ('Vintage Car', vintage_car), ('Sports Car', sports_car),
        ('Camper Van', camper_van), ('Ice Cream Truck', ice_cream_truck), ('Garbage Truck', garbage_truck)]


_NOSKY = {'School Bus', 'Tractor', 'Dump Truck', 'Camper Van', 'Ice Cream Truck'}


def _with_sky(fn):
    return lambda: sky() + fn()


BOOK = [(t, fn if t in _NOSKY else _with_sky(fn)) for t, fn in BOOK]
