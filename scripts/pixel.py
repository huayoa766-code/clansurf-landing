"""Draws the landing page's pixel-art scenes and writes them into the home page and the street use case.

Every scene is built on a small grid of colour keys, then exported as SVG with
one <path> per colour. Colours are CSS variables (--px-<key>), so the page's
theme decides them: in dark mode the street turns to night and windows light up.

Run: python3 scripts/pixel.py   (rewrites the blocks between <!--px:NAME--> markers)
"""
import math
import random
import re
from pathlib import Path


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [[None] * w for _ in range(h)]
        self.texts = []  # (x, y, text, cls, anchor)

    def px(self, x, y, k):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h and k:
            self.g[y][x] = k

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]

    def rect(self, x, y, w, h, k):
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                self.px(xx, yy, k)

    def hline(self, x0, x1, y, k):
        for x in range(int(x0), int(x1) + 1):
            self.px(x, y, k)

    def vline(self, x, y0, y1, k):
        for y in range(int(y0), int(y1) + 1):
            self.px(x, y, k)

    def sprite(self, rows, x, y, key, flip=False):
        for dy, row in enumerate(rows):
            if flip:
                row = row[::-1]
            for dx, ch in enumerate(row):
                if ch in key and key[ch]:
                    self.px(x + dx, y + dy, key[ch])

    def disc(self, cx, cy, r, fn):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                dx, dy = x - cx + 0.5, y - cy + 0.5
                if dx * dx + dy * dy <= r * r:
                    k = fn(dx, dy)
                    if k:
                        self.px(x, y, k)

    def text(self, x, y, s, cls="px-t", anchor="middle"):
        self.texts.append((x, y, s, cls, anchor))

    def svg(self, cls="", label=None, crop=None):
        x0, y0, w, h = crop or (0, 0, self.w, self.h)
        # horizontal runs per row, then stacked into rectangles when the same
        # run repeats on the next row
        open_rects = {}  # (k, x, w) -> [y_start, height]
        rects = {}
        for y in range(y0, y0 + h):
            row = self.g[y]
            seen = set()
            x = x0
            while x < x0 + w:
                k = row[x]
                if k is None:
                    x += 1
                    continue
                s = x
                while x < x0 + w and row[x] == k:
                    x += 1
                key = (k, s, x - s)
                seen.add(key)
                if key in open_rects and open_rects[key][0] + open_rects[key][1] == y:
                    open_rects[key][1] += 1
                else:
                    if key in open_rects:
                        ys, hh = open_rects[key]
                        rects.setdefault(k, []).append((s, ys, x - s, hh))
                    open_rects[key] = [y, 1]
            for key in [kk for kk in open_rects if kk not in seen]:
                ys, hh = open_rects.pop(key)
                rects.setdefault(key[0], []).append((key[1], ys, key[2], hh))
        for (k, s, rw), (ys, hh) in open_rects.items():
            rects.setdefault(k, []).append((s, ys, rw, hh))
        runs = {k: [f"M{rx - x0} {ry - y0}h{rw}v{rh}h-{rw}z" for rx, ry, rw, rh in v]
                for k, v in rects.items()}
        parts = [f'<path class="k-{k}" d="{"".join(v)}"/>' for k, v in runs.items()]
        for tx, ty, s, c, a in self.texts:
            parts.append(f'<text class="{c}" x="{tx - x0}" y="{ty - y0}" text-anchor="{a}">{s}</text>')
        aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
        return (f'<svg class="px {cls}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" '
                f'preserveAspectRatio="xMidYMax meet" {aria}>' + "".join(parts) + "</svg>")


# ---------------------------------------------------------------- people

def person(c, x, by, skin="skin1", hair="short", hairc="hair1", shirt="red",
           pants="pants", dress=False, wave=False, flip=False, scarf=None, kid=False,
           hold=None):
    """Draws a person standing on baseline `by`, 8 px wide, 16 px tall (kid: 11)."""
    if kid:
        rows = [".HHHH.", "HSSSSH", "SESSES", ".SSSS.", ".TTTT.", "STTTTS",
                ".TTTT.", ".PPPP.", ".P..P.", ".P..P.", ".K..K."]
        c.sprite(rows, x + 1, by - 11,
                 {"H": hairc, "S": skin, "E": "ink", "T": shirt, "P": pants, "K": "ink"}, flip)
        return
    rows = ["..HHHH..", ".HHHHHH.", ".HSSSSH.", ".SESSES.", ".SSSSSS.", "..SSSS..",
            "..TTTT..", ".TTTTTT.", "TTTTTTTT", "STTTTTTS", "STTTTTTS",
            ".PPPPPP.", ".PPPPPP.", ".PP..PP.", ".PP..PP.", ".KK..KK."]
    if hair == "long":
        rows[2] = "HHSSSSHH"; rows[3] = "HSESSESH"; rows[4] = "HSSSSSSH"; rows[5] = "H.SSSS.H"
    elif hair == "bun":
        rows[0] = "...HH..."; rows[1] = ".HHHHHH."
    elif hair == "cap":
        rows[0] = "..CCCC.."; rows[1] = ".CCCCCCC"; rows[2] = ".HSSSSS."
    elif hair == "bald":
        rows[0] = "........"; rows[1] = "..SSSS.."; rows[2] = ".SSSSSS."
    if scarf:
        rows[0] = "..FFFF.."; rows[1] = ".FFFFFF."; rows[2] = ".FSSSSF."
        rows[3] = ".FESSEF."; rows[4] = ".FSSSSF."; rows[5] = "..FFFF.."
    if dress:
        rows[11] = ".TTTTTT."; rows[12] = "TTTTTTTT"; rows[13] = ".SS..SS."; rows[14] = ".SS..SS."
    if wave:
        rows[9] = "STTTTTTT"; rows[10] = "STTTTTTT"
    key = {"H": hairc, "S": skin, "E": "ink", "T": shirt, "P": pants, "K": "ink",
           "C": "yellow", "F": scarf}
    c.sprite(rows, x, by - 16, key, flip)
    if wave:
        hx = x - 1 if flip else x + 8
        for yy in range(by - 12, by - 8):
            c.px(hx, yy, skin)
        c.px(hx, by - 13, skin)
    if hold == "basket":
        hx = x - 4 if flip else x + 7
        c.sprite(["w.....w", ".wwwww.", "wEeEeEw", "wwwwwww", ".wwwww."], hx, by - 9,
                 {"w": "wood", "E": "egg", "e": "egg2"})
    elif hold == "jug":
        hx = x - 3 if flip else x + 8
        c.sprite([".bb.", "bbbb", "bBbb", "bbbb", "bbbb"], hx, by - 9, {"b": "water", "B": "water2"})
    elif hold == "lantern":
        hx = x - 3 if flip else x + 8
        c.sprite([".m.", "mlm", "lll", "mlm"], hx, by - 11, {"m": "metal", "l": "lamp"})


# ---------------------------------------------------------------- goods

GOODS = {
    "milk": (["..w...w...w..", ".bwb.bwb.bwb.", ".www.www.www.", ".wBw.wBw.wBw.", ".www.www.www."],
             {"w": "milk", "b": "blue", "B": "blue"}),
    "eggs": ([".e.E.e.E.", "eEeEeEeEe", "wwwwwwwww", "wWwWwWwWw", ".wwwwwww."],
             {"e": "egg", "E": "egg2", "w": "wood", "W": "woodd"}),
    "veg": (["g.g..LL..g.", "o.o.LLLL.o.", "o.o.LLlL.o.", "rrr.LLLL.rr", "rRr..LL..rR"],
            {"g": "leaf", "o": "carrot", "L": "leaf", "l": "leaf2", "r": "tomato", "R": "tomato2"}),
    "water": ([".bb..bb..bb.", "bBbbbBbbbBbb", "bBbbbBbbbBbb", "bbbbbbbbbbbb", "bbbbbbbbbbbb"],
              {"b": "water", "B": "water2"}),
    "cloth": (["rrrr.yyyy.tt", "rRrr.yYyy.tT", "rrrr.yyyy.tt", "gggg.pppp.tt", "gGgg.pPpp.tt"],
              {"r": "red", "R": "white", "y": "yellow", "Y": "white", "t": "teal", "T": "white",
               "g": "green", "G": "white", "p": "pink", "P": "white"}),
    "wood": (["w........w..", "w.....www...", "wwwww.www...", "w...w.wmmmm.", "w...w..mmmm."],
             {"w": "wood", "m": "metal"}),
    "tools": (["...mm..rrrrrr", "..m..m.rRRRRr", "...mm..rrrrrr", "...m...r.mm.r", "...m...rrrrrr"],
              {"m": "metal", "r": "red", "R": "redd"}),
}


def signboard(c, x, by, w, sign):
    c.rect(x + 1, by - 32, w - 2, 7, "sign")
    c.hline(x + 1, x + w - 2, by - 32, "woodd"); c.hline(x + 1, x + w - 2, by - 26, "woodd")
    c.vline(x + 1, by - 32, by - 26, "woodd"); c.vline(x + w - 2, by - 32, by - 26, "woodd")
    c.text(x + w / 2, by - 27.3, sign, "px-t")


def stall(c, x, by, awn, goods, sign, w=24, seller=None):
    """Market stall on baseline `by`: sign, striped awning, seller, counter, goods."""
    if seller:
        person(c, x + w // 2 - 4, by - 2, **seller)
    for yy in range(by - 22, by):
        c.px(x + 1, yy, "woodd"); c.px(x + w - 2, yy, "woodd")
    for yy in range(by - 25, by - 20):
        for xx in range(x - 1, x + w + 1):
            c.px(xx, yy, awn if ((xx - x) // 3) % 2 == 0 else "awnw")
    for xx in range(x - 1, x + w + 1):
        if (xx - x) % 3 != 1:
            c.px(xx, by - 20, awn if ((xx - x) // 3) % 2 == 0 else "awnw")
    if sign:
        signboard(c, x, by, w, sign)
    # counter
    c.rect(x, by - 8, w, 8, "woodd")
    c.hline(x, x + w - 1, by - 8, "wood")
    for xx in range(x + 3, x + w, 5):
        c.vline(xx, by - 7, by - 1, "wood")
    rows, key = GOODS[goods]
    gw = len(rows[0])
    c.sprite(rows, x + (w - gw) // 2, by - 8 - len(rows), key)


# ---------------------------------------------------------------- scenery

def tree(c, x, by, r=8, trunk_h=7):
    c.rect(x - 1, by - trunk_h, 3, trunk_h, "trunk")
    cy = by - trunk_h - r + 2

    def shade(dx, dy):
        d = dx * dx + dy * dy
        if d > (r - 1) ** 2 and dx + dy > 0:
            return "treed"
        if dx + dy < -r * 0.7:
            return "treel"
        if dx + dy > r * 0.55:
            return "treed"
        return "tree"
    c.disc(x + 0.5, cy, r, shade)
    random.seed(x * 7 + by)
    for _ in range(r):
        a = random.random() * math.tau
        rr = random.random() * (r - 2)
        c.px(x + math.cos(a) * rr, cy + math.sin(a) * rr, "treel" if random.random() < .5 else "treed")


def palm(c, x, by, h=26):
    for i in range(h):
        xx = x + int(2 * math.sin(i / h * 1.6))
        c.px(xx, by - i, "trunk"); c.px(xx + 1, by - i, "trunkd" if i % 3 == 0 else "trunk")
    tx, ty = x + int(2 * math.sin(1.6)), by - h
    for ang, ln in [(-2.8, 11), (-2.2, 10), (-1.1, 9), (-0.4, 11), (0.2, 10), (-1.6, 7)]:
        for i in range(ln):
            fx = tx + math.cos(ang) * i
            fy = ty + math.sin(ang) * i + (i * i) / 22
            c.px(fx, fy, "tree"); c.px(fx, fy + 1, "treed" if i > 2 else "tree")
    c.px(tx, ty + 1, "trunkd"); c.px(tx + 1, ty + 2, "trunkd")


def bush(c, x, by, w=8, flowers="pink"):
    for i in range(0, w, 3):
        c.disc(x + i + 1.5, by - 2, 2.6, lambda dx, dy: "treed" if dy > 0.8 else "grass2")
    random.seed(x)
    for i in range(w // 2):
        c.px(x + random.randint(0, w), by - random.randint(2, 4), flowers)


def cloud(c, x, y, w=18):
    for i, r in enumerate([3, 4.5, 3.5, 2.5]):
        c.disc(x + i * w / 4 + 2, y - (1 if i in (1, 2) else 0), r,
               lambda dx, dy: "cloud" if dy < 1.2 else None)
    c.rect(x, y, w, 2, "cloud")


def radio(c, x, top, arcs=True, big=False):
    """Node radio on a roof: pole, antenna box, signal arcs. `top` is the roof line."""
    h = 16 if big else 10
    c.vline(x, top - h, top - 1, "metal")
    c.rect(x - 1, top - 5, 3, 3, "metald")
    c.px(x, top - h - 1, "signal"); c.px(x, top - h - 2, "signal")
    if arcs:
        cy = top - h - 1
        for r in ([4, 7, 10] if big else [3, 6]):
            for a in range(0, 360, 4):
                t = math.radians(a)
                dx, dy = math.cos(t) * r, math.sin(t) * r
                if abs(dy) < r * 0.75 and abs(dx) > r * 0.45:
                    c.px(x + dx, cy + dy, "signal")


def building(c, x, by, w, h, wall, roof, style="pitched", door=True, lit=(), seed=0):
    top = by - h
    c.rect(x, top, w, h, wall)
    c.vline(x, top, by - 1, "edge"); c.vline(x + w - 1, top, by - 1, "edge")
    # ground-floor trim
    c.hline(x, x + w - 1, by - 12, "trim")
    random.seed(seed)
    floors = max(1, (h - 12) // 13)
    cols = max(1, (w - 4) // 9)
    gap = (w - cols * 5) / (cols + 1)
    n = 0
    for f in range(floors):
        wy = by - 12 - 12 * (f + 1) + 2
        if wy < top + 2:
            break
        for i in range(cols):
            wx = int(x + gap + i * (5 + gap))
            c.rect(wx - 1, wy - 1, 7, 8, "frame")
            c.rect(wx, wy, 5, 6, "winl" if n in lit else "win")
            c.vline(wx + 2, wy, wy + 5, "frame")
            c.hline(wx - 1, wx + 5, wy + 7, "trim")
            if random.random() < 0.35:  # a flower box
                for k in range(5):
                    c.px(wx + k, wy + 6, "grass2" if k % 2 else random.choice(["pink", "red", "yellow"]))
            n += 1
    if door:
        dx = x + w // 2 - 3
        c.rect(dx, by - 10, 6, 10, "door")
        c.px(dx + 4, by - 5, "yellow")
        c.hline(dx - 1, dx + 6, by - 11, "trim")
    if style == "pitched":
        rh = w // 3 + 2
        for i in range(rh):
            inset = int((i + 1) * (w / 2 + 2) / rh)
            yy = top - rh + i
            c.hline(x - 2 + (w // 2 + 2) - inset, x + w + 1 - (w // 2 + 2) + inset, yy, roof)
        c.hline(x - 2, x + w + 1, top - 1, "roofd")
        return top - rh
    c.rect(x - 1, top - 3, w + 2, 3, roof)
    c.hline(x - 1, x + w, top - 1, "roofd")
    return top - 3


def sky(c, y_end, dither_at, stars=True, seed=1):
    for y in range(0, y_end):
        for x in range(c.w):
            if y < dither_at:
                k = "sky"
            elif y < dither_at + 4:
                k = "sky" if (x + y) % 2 == 0 and y < dither_at + 2 or (x + y) % 4 == 0 else "sky2"
            else:
                k = "sky2"
            c.px(x, y, k)
    if stars:
        random.seed(seed)
        for _ in range(c.w // 7):
            c.px(random.randrange(c.w), random.randrange(max(1, dither_at)), "star")


def hills(c, base, amp=5, k="hill"):
    for x in range(c.w):
        top = base - int(amp * (0.6 * math.sin(x / 23) + 0.4 * math.sin(x / 9 + 1)) + amp)
        c.vline(x, top, base, k)


def road(c, y, h=16):
    c.rect(0, y, c.w, h, "road")
    for x in range(0, c.w, 14):
        c.hline(x, x + 6, y + h // 2, "roadl")


def bunting(c, x0, x1, y, sag=6):
    cols = ["red", "yellow", "teal", "pink", "blue", "green"]
    n = 0
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        yy = y + int(sag * 4 * t * (1 - t))
        c.px(x, yy, "edge")
        if (x - x0) % 6 == 2:
            col = cols[n % len(cols)]; n += 1
            c.hline(x - 1, x + 1, yy + 1, col); c.px(x, yy + 2, col)


def laundry(c, x0, x1, y):
    cols = ["white", "blue", "yellow", "red", "white"]
    c.hline(x0, x1, y, "edge")
    for i, x in enumerate(range(x0 + 3, x1 - 3, 6)):
        col = cols[i % len(cols)]
        c.rect(x, y + 1, 4, 4 + (i % 2), col)


def cat(c, x, by):
    c.sprite(["o...o..", "ooooo..", "oEoEo.o", "ooooooo", ".ooooo.", ".o...o."], x, by - 6,
             {"o": "cat", "E": "ink"})


def birds(c, pts):
    for x, y in pts:
        c.px(x, y, "edge"); c.px(x + 1, y + 1, "edge"); c.px(x + 2, y, "edge")
        c.px(x - 1, y - 1, "edge"); c.px(x + 3, y - 1, "edge")


def sun(c, x, y, r=7):
    c.disc(x, y, r + 3, lambda dx, dy: "sunray" if (round(dx) == 0 or round(dy) == 0 or abs(abs(dx) - abs(dy)) < 0.8) else None)
    c.disc(x, y, r + 1.2, lambda dx, dy: "sky")
    c.disc(x, y, r, lambda dx, dy: "sunl" if dx + dy < -2 else "sun")


def planter(c, x, by):
    c.rect(x, by - 4, 6, 4, "roofa"); c.hline(x - 1, x + 6, by - 4, "roofd")
    c.disc(x + 3, by - 7, 3.4, lambda dx, dy: "treed" if dy > 1 else "grass2")
    random.seed(x)
    for _ in range(3):
        c.px(x + random.randint(1, 5), by - random.randint(6, 9), random.choice(["pink", "yellow", "red", "white"]))


def balloon(c, x, y):
    c.sprite([".rr.", "rRrr", "rrrr", ".rr.", "..e.", ".e..", "..e.", "..e."], x, y - 6,
             {"r": "red", "R": "white", "e": "edge"})


def dog(c, x, by):
    c.sprite(["......oo", "o....ooE", ".ooooooo", ".oooooo.", ".o.o.o.o"], x, by - 5,
             {"o": "cat", "E": "ink"})


# ---------------------------------------------------------------- scenes

SELLERS = [
    dict(skin="skin2", hair="cap", hairc="hair1", shirt="blue"),
    dict(skin="skin3", scarf="pink", shirt="teal"),
    dict(skin="skin1", hair="bald", shirt="green"),
    dict(skin="skin4", hair="short", hairc="hair1", shirt="yellow"),
    dict(skin="skin2", hair="bun", hairc="hair3", shirt="red", dress=True),
    dict(skin="skin3", hair="short", hairc="hair2", shirt="white"),
    dict(skin="skin4", hair="long", hairc="hair1", shirt="indigo"),
]


def hero_scene():
    W, H = 360, 170
    c = Canvas(W, H)
    base = 128
    sky(c, base, 58)
    sun(c, 318, 22)
    cloud(c, 20, 20, 22); cloud(c, 150, 12, 26); cloud(c, 290, 26, 18)
    birds(c, [(96, 18), (104, 22), (232, 14)])
    hills(c, base, 6, "hill")
    for x in range(-4, W, 11):
        c.disc(x + 3, base - 22 - (x * 7 % 5), 6, lambda dx, dy: "hill2")
    c.rect(0, base - 20, W, 20, "hill2")

    plan = [  # x, w, h, wall, roof, style, lit
        (2, 32, 48, "walla", "roofa", "pitched", (1,)),
        (48, 38, 64, "wallc", "roofb", "flat", (0, 5)),
        (98, 30, 44, "walld", "roofc", "pitched", ()),
        (140, 44, 78, "walle", "roofb", "flat", (2, 6)),
        (196, 32, 52, "wallb", "roofa", "pitched", (0,)),
        (242, 36, 60, "walla", "roofd", "flat", (3,)),
        (290, 30, 46, "wallc", "roofc", "pitched", (1,)),
        (330, 32, 56, "walld", "roofa", "flat", ()),
    ]
    tops = []
    for i, (x, w, h, wall, roof, style, lit) in enumerate(plan):
        tops.append(building(c, x, base, w, h, wall, roof, style, lit=lit, seed=i))
    tree(c, 40, base, 7, 9)
    palm(c, 132, base, 30)
    tree(c, 234, base, 8, 10)
    tree(c, 284, base - 1, 6, 8)
    laundry(c, 250, 300, base - 44)
    bunting(c, 50, 138, base - 52, 7)
    cat(c, 74, base - 67)
    # the node radio on the tallest roof, and two neighbours relaying
    radio(c, 162, tops[3], big=True)
    radio(c, 16, tops[0] + 1)
    radio(c, 262, tops[5])

    # the street curves: every row below the far pavement follows yo(x)
    def yo(x):
        return round(4 * math.sin((x - 30) / 52))

    for x in range(W):
        o = yo(x)
        c.vline(x, base, base + 7 + o, "pave")
        c.px(x, base + 7 + o, "paved")
        c.vline(x, base + 8 + o, base + 23 + o, "road")
        if (x // 7) % 2 == 0:
            c.px(x, base + 15 + o, "roadl")
        c.px(x, base + 24 + o, "paved")
        c.vline(x, base + 25 + o, base + 29 + o, "pave")
        c.vline(x, base + 30 + o, H - 1, "grass")
        c.px(x, base + 30 + o, "grass2")
        if x % 8 == 0:
            c.px(x, base + 3, "paved")
    random.seed(5)
    for _ in range(90):  # meadow flowers and tufts on the verge
        x = random.randrange(W)
        y = random.randint(base + 33 + yo(x), H - 2)
        c.px(x, y, random.choice(["pink", "yellow", "white", "grass2", "grass2", "red"]))

    stalls = [(6, "blue", "milk", "MILK"), (52, "green", "eggs", "EGGS"),
              (100, "red", "veg", "VEGETABLES"), (200, "teal", "water", "WATER"),
              (246, "yellow", "cloth", "TAILOR"), (294, "green", "wood", "CARPENTER"),
              (334, "red", "tools", "REPAIRS")]
    for i, (x, awn, goods, sign) in enumerate(stalls):
        stall(c, x, base + 5, awn, goods, sign, w=26 if len(sign) > 7 else 24, seller=SELLERS[i])
    for x in (44, 92, 190, 238, 286):  # planters between stalls
        planter(c, x, base + 6)

    def on_road(x, dy):
        return base + dy + yo(x + 4)

    # neighbours out on the street
    person(c, 32, base + 6, skin="skin1", hair="long", hairc="hair2", shirt="yellow", dress=True, hold="basket")
    person(c, 84, base + 6, skin="skin4", hair="short", shirt="green", flip=True)
    person(c, 150, base + 6, skin="skin3", hair="short", hairc="hair3", shirt="white", wave=True)
    person(c, 176, base + 6, skin="skin1", scarf="blue", shirt="indigo", dress=True, hold="jug", flip=True)
    person(c, 226, base + 6, skin="skin2", hair="bun", shirt="teal", dress=True)
    person(c, 120, on_road(120, 19), skin="skin3", hair="cap", shirt="red")  # crossing the road
    person(c, 58, on_road(58, 29), skin="skin2", hair="short", shirt="blue")
    person(c, 68, on_road(68, 29), skin="skin4", hair="long", shirt="pink", dress=True, flip=True)
    person(c, 200, on_road(200, 29), skin="skin1", kid=True, shirt="yellow")
    balloon(c, 207, on_road(200, 29) - 11)
    person(c, 212, on_road(212, 29), skin="skin1", hair="short", hairc="hair2", shirt="green")
    dog(c, 224, on_road(224, 29))
    person(c, 300, on_road(300, 29), skin="skin3", hair="bald", shirt="yellow", wave=True, flip=True)
    person(c, 312, on_road(312, 29), skin="skin4", kid=True, shirt="teal", flip=True)
    # foreground greenery along the curve
    for x, r in ((16, 6), (140, 7), (262, 6), (348, 5)):
        tree(c, x, H - 1, r, 5)
    for x in (34, 96, 170, 232, 322):
        bush(c, x, H - 1, 12, random.choice(["pink", "yellow", "red", "white"]))
    return c


def icon(kind):
    c = Canvas(16, 16)
    if kind == "you":
        person(c, 4, 16, skin="skin2", hair="short", shirt="indigo")
    elif kind == "neighbour":
        c.sprite(["rrwwrrwwrrwwrr", "rrwwrrwwrrwwrr", "r.r.r.r.r.r.r."], 1, 1, {"r": "red", "w": "awnw"})
        person(c, 4, 13, skin="skin3", scarf="pink", shirt="teal")
        c.rect(1, 11, 14, 5, "woodd"); c.hline(1, 14, 11, "wood")
        c.sprite([".e.E.e.", "eEeEeEe", "wwwwwww"], 4, 8, {"e": "egg", "E": "egg2", "w": "wood"})
    elif kind == "data":
        c.rect(4, 1, 8, 14, "ink"); c.rect(5, 3, 6, 9, "sky")
        for i, hh in enumerate([2, 4, 6]):
            c.rect(6 + i * 2, 11 - hh, 1, hh, "indigo")
        c.px(8, 13, "metal")
    elif kind == "account":
        c.rect(1, 3, 14, 10, "white"); c.rect(1, 3, 14, 1, "metald"); c.rect(1, 12, 14, 1, "metald")
        c.vline(1, 3, 12, "metald"); c.vline(14, 3, 12, "metald")
        c.disc(5, 7, 2, lambda dx, dy: "metal"); c.rect(3, 9, 5, 2, "metal")
        c.hline(9, 12, 6, "metald"); c.hline(9, 12, 8, "metal"); c.hline(9, 11, 10, "metal")
    elif kind == "server":
        for i in range(3):
            y = 2 + i * 4
            c.rect(3, y, 10, 3, "metald"); c.hline(3, 12, y, "metal")
            c.px(5, y + 1, "green" if i != 1 else "red"); c.hline(8, 11, y + 1, "ink")
        c.rect(4, 14, 8, 1, "ink")
    elif kind == "platform":
        c.rect(3, 5, 10, 10, "metal"); c.hline(2, 13, 4, "metald"); c.hline(3, 12, 3, "metald")
        c.hline(5, 10, 2, "metald"); c.rect(6, 10, 4, 5, "ink")
        for x in (4, 7, 10):
            c.rect(x, 6, 2, 2, "win")
        c.sprite([".yy.", "yYyy", "yyyy", ".yy."], 11, 10, {"y": "yellow", "Y": "white"})
    elif kind == "radio":
        c.rect(3, 13, 10, 3, "roofb")
        radio(c, 8, 13)
    return c


def vignette(kind):
    c = Canvas(40, 34)
    c.rect(0, 30, 40, 4, "pave"); c.hline(0, 39, 30, "paved")
    if kind == "visible":
        stall(c, 4, 30, "yellow", "veg", "", w=20, seller=dict(skin="skin4", hair="short", shirt="green"))
        person(c, 29, 31, skin="skin1", hair="long", hairc="hair2", shirt="red", dress=True, flip=True)
        for i, (dx, dy) in enumerate([(-3, -4), (-5, -1), (-3, 2)]):
            c.px(28 + dx, 20 + dy, "signal")
    elif kind == "reachable":
        person(c, 3, 31, skin="skin3", hair="cap", shirt="blue")
        person(c, 29, 31, skin="skin2", scarf="teal", shirt="yellow", flip=True)
        c.sprite(["m", "m", "k"], 12, 18, {"m": "metal", "k": "ink"})
        c.sprite(["m", "m", "k"], 27, 18, {"m": "metal", "k": "ink"})
        for x in range(15, 26, 2):
            c.px(x, 13 + int(abs(x - 20) / 2.5), "signal")
    elif kind == "shared":
        person(c, 5, 31, skin="skin4", hair="bun", shirt="teal", dress=True)
        person(c, 27, 31, skin="skin1", hair="short", hairc="hair2", shirt="red", flip=True)
        c.sprite(["w.....w", ".wwwww.", "wEeEeEw", "wwwwwww"], 16, 19,
                 {"w": "wood", "E": "egg", "e": "egg2"})
    return c


def stack_scene():
    W, H = 110, 170
    c = Canvas(W, H)
    base = 150
    sky(c, base, 40, stars=True, seed=4)
    # the public chain, up where the internet is
    for i, bx in enumerate((14, 47, 80)):
        c.rect(bx, 8, 14, 12, "chain"); c.rect(bx + 2, 6, 14, 2, "chainl"); c.vline(bx + 14, 7, 18, "chaind")
        c.rect(bx + 3, 11, 8, 2, "chainl"); c.rect(bx + 3, 15, 5, 2, "chainl")
        if i < 2:
            c.hline(bx + 15, bx + 32, 14, "chaind"); c.px(bx + 22, 13, "chaind"); c.px(bx + 25, 15, "chaind")
    # the connection line
    for x in range(0, W, 5):
        c.hline(x, x + 2, 34, "dash")
    # three houses
    t1 = building(c, 4, base, 30, 52, "walla", "roofa", "pitched", lit=(1,), seed=11)
    t2 = building(c, 40, base, 32, 74, "walle", "roofb", "flat", lit=(0, 3), seed=12)
    t3 = building(c, 78, base, 28, 48, "wallc", "roofc", "pitched", lit=(), seed=13)
    radio(c, 18, t1 + 1)
    radio(c, 92, t3 + 1)
    # hop arcs between the neighbours' radios and the middle roof
    for x in range(20, 90):
        y = t2 - 18 + int(((x - 55) / 35) ** 2 * 12)
        if x % 3 == 0:
            c.px(x, y, "signal")
    # the governance node: a lit box on the middle roof, reaching up to the chain
    c.rect(49, t2 - 8, 12, 8, "gov"); c.rect(51, t2 - 6, 3, 2, "winl"); c.rect(56, t2 - 6, 3, 2, "green")
    for y in range(22, t2 - 9):
        if y % 4 < 2:
            c.px(55, y, "signal")
    c.rect(0, base, W, 6, "pave"); c.hline(0, W, base + 5, "paved")
    c.rect(0, base + 6, W, H - base - 6, "grass")
    person(c, 8, base + 5, skin="skin2", hair="long", shirt="red", dress=True)
    person(c, 30, base + 5, skin="skin4", hair="cap", shirt="yellow", flip=True)
    person(c, 64, base + 5, skin="skin1", scarf="teal", shirt="blue", dress=True, hold="basket")
    person(c, 88, base + 5, skin="skin3", kid=True, shirt="green")
    tree(c, 101, base + 5, 5, 6)
    bush(c, 40, base + 14, 12, "yellow")
    return c


def night_scene():
    W, H = 360, 112
    c = Canvas(W, H)
    base = 96
    sky(c, base, 56, stars=True, seed=9)
    c.disc(300, 20, 6, lambda dx, dy: "moon" if dx < 2.5 else None)
    hills(c, base, 4, "hill")
    plan = [(4, 34, 44, "walla", "roofa", "pitched"), (50, 40, 58, "wallc", "roofb", "flat"),
            (104, 30, 40, "walld", "roofc", "pitched"), (148, 42, 64, "walle", "roofb", "flat"),
            (204, 32, 46, "wallb", "roofa", "pitched"), (250, 40, 54, "walla", "roofd", "flat"),
            (306, 34, 42, "wallc", "roofc", "pitched")]
    tops = [building(c, p[0], base, *p[1:], lit=(), seed=20 + i) for i, p in enumerate(plan)]
    radio(c, 169, tops[3], big=True)
    radio(c, 20, tops[0] + 1)
    radio(c, 270, tops[5])
    tree(c, 96, base, 6, 8); tree(c, 240, base, 7, 9)
    c.rect(0, base, W, H - base, "pave"); c.hline(0, W, base + 5, "paved")
    stall(c, 150, base + 6, "teal", "water", "WATER", seller=SELLERS[3])
    person(c, 128, base + 7, skin="skin2", hair="long", shirt="red", dress=True, hold="lantern")
    person(c, 180, base + 7, skin="skin4", hair="cap", shirt="yellow", hold="jug", flip=True)
    person(c, 192, base + 7, skin="skin1", kid=True, shirt="green")
    person(c, 60, base + 7, skin="skin3", scarf="blue", shirt="teal", hold="lantern")
    person(c, 232, base + 7, skin="skin1", hair="short", hairc="hair3", shirt="white", hold="lantern", flip=True)
    return c


def mini_node(seed):
    random.seed(seed)
    c = Canvas(16, 16)
    c.rect(0, 14, 16, 2, "grass")
    walls = ["walla", "wallb", "wallc", "walld", "walle"]
    roofs = ["roofa", "roofb", "roofc", "roofd"]
    t = building(c, 1, 14, 8, 8, random.choice(walls), random.choice(roofs), "pitched", door=False, seed=seed)
    radio(c, 5, t + 1, arcs=False)
    tree(c, 12, 14, 3, 3)
    return c


def agent_sprite():
    c = Canvas(12, 16)
    c.px(6, 0, "signal"); c.vline(6, 1, 2, "metal")
    c.rect(2, 3, 9, 6, "metal"); c.rect(3, 4, 7, 4, "ink"); c.px(4, 5, "signal"); c.px(8, 5, "signal")
    c.hline(5, 7, 7, "signal")
    c.rect(3, 9, 7, 5, "metald"); c.rect(1, 10, 2, 3, "metal"); c.rect(10, 10, 2, 3, "metal")
    c.rect(8, 10, 4, 5, "white"); c.hline(9, 10, 11, "metal"); c.hline(9, 10, 13, "metal")
    c.rect(4, 14, 2, 2, "ink"); c.rect(7, 14, 2, 2, "ink")
    return c


def decider_sprite():
    c = Canvas(12, 16)
    person(c, 2, 16, skin="skin3", hair="bun", shirt="green", dress=True, wave=True)
    return c


def welcome_scene():
    W, H = 360, 96
    c = Canvas(W, H)
    base = 70
    sky(c, base, 36, stars=True, seed=3)
    cloud(c, 60, 14, 20); cloud(c, 250, 10, 24)
    hills(c, base, 3, "hill")
    t = building(c, 10, base, 34, 36, "walla", "roofa", "pitched", lit=(1,), seed=31)
    building(c, 56, base, 28, 30, "walld", "roofc", "pitched", seed=32)
    tree(c, 96, base, 7, 8)
    # an empty plot with a sign, waiting for the next node
    c.rect(134, base - 16, 16, 8, "sign"); c.vline(141, base - 8, base - 1, "woodd")
    c.hline(134, 149, base - 16, "woodd"); c.hline(134, 149, base - 9, "woodd")
    c.text(142, base - 10.6, "NEXT?", "px-t")
    bush(c, 114, base, 12, "yellow"); bush(c, 158, base, 12, "pink")
    t2 = building(c, 184, base, 36, 34, "wallc", "roofb", "flat", seed=33)
    # someone up a ladder fitting a radio
    radio(c, 196, t2 + 1)
    for y in range(t2 + 2, base):
        c.px(210, y, "wood"); c.px(214, y, "wood")
        if y % 3 == 0:
            c.hline(210, 214, y, "wood")
    person(c, 208, t2 + 14, skin="skin4", hair="cap", shirt="yellow")
    tree(c, 234, base, 6, 7)
    building(c, 250, base, 30, 32, "wallb", "roofa", "pitched", lit=(0,), seed=34)
    palm(c, 286, base, 24)
    building(c, 298, base, 36, 38, "walle", "roofd", "flat", seed=35)
    radio(c, 26, t + 1)

    def yo(x):
        return round(3 * math.sin((x + 20) / 45))
    for x in range(W):
        o = yo(x)
        c.vline(x, base, base + 6 + o, "pave")
        c.px(x, base + 6 + o, "paved")
        c.vline(x, base + 7 + o, H - 1, "grass")
        c.px(x, base + 7 + o, "grass2")
    random.seed(8)
    for _ in range(60):
        x = random.randrange(W)
        c.px(x, random.randint(base + 10 + yo(x), H - 2), random.choice(["pink", "yellow", "white", "red", "grass2"]))
    for x in (20, 120, 230, 330):
        bush(c, x, H - 1, 12, random.choice(["pink", "yellow", "red"]))
    for x, kw in [(60, dict(skin="skin2", hair="long", shirt="red", dress=True, wave=True)),
                  (72, dict(skin="skin1", kid=True, shirt="yellow")),
                  (120, dict(skin="skin3", hair="short", shirt="blue", wave=True, flip=True)),
                  (160, dict(skin="skin4", scarf="pink", shirt="teal", dress=True)),
                  (270, dict(skin="skin1", hair="bun", hairc="hair3", shirt="green", dress=True, wave=True)),
                  (330, dict(skin="skin3", hair="cap", shirt="indigo", flip=True))]:
        person(c, x, base + 6 + yo(x + 4), **kw)
    dog(c, 84, base + 6 + yo(88))
    return c


# ---------------------------------------------------------------- write

def inject(html, name, svg):
    pat = re.compile(rf"(<!--px:{name}-->).*?(<!--/px:{name}-->)", re.S)
    if not pat.search(html):
        raise SystemExit(f"marker px:{name} not found")
    return pat.sub(lambda m: m.group(1) + svg + m.group(2), html)


def main():
    root = Path(__file__).resolve().parent.parent
    blocks = {
        "hero": hero_scene().svg("px-hero", "A street inside one node: seven stalls selling milk, eggs, vegetables, water, tailoring, carpentry and repairs, neighbours on the pavement, and a node radio on the tallest roof relaying to radios on two other roofs"),
        "stack": stack_scene().svg("px-stack"),
        "night": night_scene().svg("px-night", "The same street during a blackout: windows dark, neighbours with lanterns at the water stall, and the node radios still signalling"),
        "welcome": welcome_scene().svg("px-welcome"),
        "agent": agent_sprite().svg("px-sprite"),
        "decider": decider_sprite().svg("px-sprite"),
    }
    for k in ("you", "data", "account", "server", "platform", "neighbour", "radio"):
        blocks[f"i-{k}"] = icon(k).svg("px-ico")
    for k in ("visible", "reachable", "shared"):
        blocks[f"v-{k}"] = vignette(k).svg("px-vig")
    blocks["minis"] = "".join(mini_node(i * 13 + 5).svg("px-mini") for i in range(25))
    # palette + one fill rule per colour key actually used
    keys = sorted(set(re.findall(r'class="k-([a-z0-9]+)"', "".join(blocks.values()))))
    css = (root / "scripts" / "px-palette.css").read_text()
    css += "\n" + "\n".join(f".px .k-{k} {{ fill: var(--px-{k}); }}" for k in keys)
    blocks["css"] = "<style>\n" + css + "\n</style>"
    for page in (root / "public" / "index.html", root / "public" / "use-cases" / "street" / "index.html"):
        html = page.read_text()
        for name, svg in blocks.items():
            if f"<!--px:{name}-->" in html:
                html = inject(html, name, svg)
        page.write_text(html)

    # the social card uses a crop of the hero street around the node radio
    og = root / "scripts" / "og-image.html"
    if og.exists():
        card = og.read_text()
        card = inject(card, "og", hero_scene().svg("px-og", crop=(120, 0, 156, 170)).replace(
            'preserveAspectRatio="xMidYMax meet"', 'preserveAspectRatio="xMidYMax slice"'))
        card = inject(card, "css", blocks["css"])
        og.write_text(card)
    # the home page's card shows many small nodes
    ogh = root / "scripts" / "og-home.html"
    if ogh.exists():
        card = ogh.read_text()
        minis = "".join(mini_node(i * 7 + 3).svg("px-mini") for i in range(16))
        card = inject(card, "minis", minis)
        card = inject(card, "css", blocks["css"])
        ogh.write_text(card)
    print({k: len(v) for k, v in blocks.items()})


if __name__ == "__main__":
    main()
