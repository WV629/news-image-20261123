#!/usr/bin/env python3
"""Render 'The World in One Image' for Monday 23 November 2026.

Deterministic Pillow pipeline: no network, no timestamps, no randomness.
Running it twice must produce byte-identical PNG output.
Writes entry.png (1024x1024, PNG) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- palette ---------------------------------------------------------------
PAPER = (247, 243, 234)   # warm off-white page
INK = (18, 30, 54)        # deep navy ink
INK_SOFT = (52, 68, 96)
RED = (178, 34, 34)       # headline accent
TEAL = (14, 92, 96)
GOLD = (184, 134, 11)
GREY_LINE = (203, 196, 182)
CARD = (255, 255, 255)
DARK_PANEL = (24, 38, 64)
MUTED = (110, 116, 128)

# ---- fonts -----------------------------------------------------------------
def font(name, size):
    paths = {
        "sans": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "sans_b": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "serif_b": "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if name.endswith("_b") else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)

F_TITLE = font("serif_b", 46)
F_STRAP = font("sans_b", 15)
F_KICK = font("sans_b", 12)
F_HEAD = font("sans_b", 21)
F_DECK = font("sans", 14)
F_SMALL_HEAD = font("sans_b", 15)
F_SMALL_DECK = font("sans", 11)
F_STAT_N = font("sans_b", 30)
F_STAT_L = font("sans_b", 11)
F_BRIEF = font("sans", 12)
F_BRIEF_B = font("sans_b", 12)
F_FOOT = font("sans", 11)
F_MAP_LBL = font("sans_b", 11)
F_NUM = font("sans_b", 16)
F_BIG_NUM = font("serif_b", 40)

# ---- verified news content: Monday 23 November 2026 ------------------------
# Every fact below was checked against live reporting (Reuters, AP, CNN,
# Al Jazeera, Arab News, Kyiv Independent, Xinhua, Dawn) on 23 Nov 2026.
MASTHEAD_STRAP = "MONDAY 23 NOVEMBER 2026  ·  27 STORIES  ·  5 REGIONS  ·  ONE DAY"

STATS = [
    ("NO DEAL", "COP31 ends with no pact"),
    ("258", "Democrats' House seats"),
    ("11", "killed in Kyiv region"),
    ("5", "tankers hit in 3 days"),
    ("24", "bodies from factory fire"),
    ("1,000+", "Delta flights delayed"),
]

FEATURES = [
    {
        "num": "01", "place": "ANTALYA", "cat": "CLIMATE",
        "head": "COP31 collapses with no deal",
        "deck": ("The EU, Panama and island states reject a draft that never "
                 "mentions fossil fuels. The longest COP ever ends with no pact."),
        "src": "Reuters · CNN",
        "art": "cop",
    },
    {
        "num": "02", "place": "WASHINGTON", "cat": "POLITICS",
        "head": "Democrats clinch 258 House seats",
        "deck": ("A North Carolina recount gives Hubbard the 258th seat — the "
                 "biggest majority since 1992. Democrats also take the Senate."),
        "src": "AP · Reuters",
        "art": "house",
    },
    {
        "num": "03", "place": "DYMER, UKRAINE", "cat": "WAR",
        "head": "Russian strikes kill 11 across Kyiv region",
        "deck": ("A drone collapses a five-storey block in Dymer, killing nine; "
                 "a supermarket and a home are also hit."),
        "src": "Arab News · Kyiv Independent",
        "art": "dymer",
    },
]

SMALLS = [
    ("04", "STRAIT OF HORMUZ", "CONFLICT",
     "Tanker attacks hit highest level since war began",
     "Three tankers struck Fri–Sat; Iran's navy says two more hit mines on Sunday.",
     "AP · UKMTO"),
    ("05", "BENGHAZI", "WAR",
     "Sea drones hit Russian warship in Libya",
     "Corvette Merkury badly damaged and later capsized; 10 hurt, Libyan officials say.",
     "AP · Reuters"),
    ("06", "RAMALLAH", "CONFLICT",
     "Settlers torch 12 vehicles in West Bank",
     "Overnight fires in four villages; Israel opens an inquiry.",
     "Reuters"),
    ("07", "NEW YORK", "MARKETS",
     "Washington demands answers on Nvidia",
     "SEC probe reported Fri; shares -14%. Bessent demands answers.",
     "Reuters · NYT"),
    ("08", "JOHANNESBURG", "DIPLOMACY",
     "G20 opens on African soil for first time",
     "South Africa hosts the first G20 summit ever held in Africa.",
     ""),
    ("09", "ATLANTA", "TRAVEL",
     "Delta glitch delays 1,000+ flights",
     "Automation fault snarls Sunday travel at the Atlanta hub days before Thanksgiving.",
     "AP"),
    ("10", "SEOUL", "POLITICS",
     "South Korea minister quits over exam chaos",
     "Education chief Choi Kyo-jin resigns after AI cheating confusion.",
     "Xinhua"),
    ("11", "KHARTOUM", "WAR",
     "Drones hit UN building in Khartoum",
     "Strikes damage a UN facility; three killed in a house in Omdurman.",
     "Arab News"),
    ("12", "CIKANDE", "DISASTER",
     "24 bodies pulled from factory fire",
     "Search resumes Monday after the candy-factory blaze in Banten, Indonesia.",
     "Xinhua"),
    ("13", "WASHINGTON", "DEFENCE",
     "Hegseth curbs US–Canada defence ties",
     "Classified memo imposes new restrictions, the Washington Post reports.",
     "Washington Post"),
]

BRIEFS = [
    ("Ohio", "Three killed at a baby shower shooting in Parma. (AP)"),
    ("South Sudan", "SPLA-IO attack leaves 24 civilians dead. (AFP)"),
    ("Congo", "Fighting near the Ebola outbreak disrupts the WHO response. (Reuters)"),
    ("Naha", "Shuri Castle's main hall reopens, seven years after fire."),
    ("Lahore", "World's most polluted major city again, AQI 538. (Dawn)"),
    ("Virginia", "Trump hosts a third meme-coin gala at his country club. (Reuters)"),
    ("Iowa", "Army plans to detonate five tons of bomb chemicals Mon–Tue. (AP)"),
    ("Paris", "Sixth weekend of marches draws tens of thousands. (AFP)"),
    ("Washington", "Trump vows a 10% cap on credit-card rates. (AP)"),
    ("Gulf", "US denies Iran downed an F-16 over the Gulf. (CENTCOM)"),
    ("Washington", "Trump threatens a tax on firms building AI data centres abroad."),
    ("Riyadh", "Coalition intercepts a Houthi drone aimed at the Riyadh region."),
    ("Gaza", "Strikes go on despite the truce; displaced people protest."),
    ("Baghdad", "Basra power-station fire kills 4 and hurts 35. (Reuters)"),
]

DATE_CHECK = ("NOT MONDAY — reported before today: Shenzhen summit (Thu) · "
              "Chapo Isidro captured (Fri) · Nvidia -14% (Fri) · "
              "BepiColombo at Mercury (Sat) · Alcaraz wins ATP Finals (Sun)")

FOOTER = "Sources: Reuters · AP · CNN · Al Jazeera · Arab News · Kyiv Independent · Xinhua · Dawn · NYT · Washington Post."

REGION_CHIPS = ["NORTH AMERICA 4", "MIDDLE EAST 3", "AFRICA 3", "ASIA 2", "EUROPE 1"]

# ---- text helpers ------------------------------------------------------------
def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)

# ---- banner art (simple flat shapes, drawn, not photos) ----------------------
def banner_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 74, 78))
    d.ellipse([x + w // 2 - 52, y + 8, x + w // 2 + 52, y + 112], fill=(247, 243, 234))
    # cracked globe: red diagonal crack + small flame
    d.line([x + w // 2 - 30, y + 18, x + w // 2 + 5, y + 55,
            x + w // 2 - 12, y + 78, x + w // 2 + 28, y + 104],
           fill=RED, width=5)
    d.ellipse([x + w - 46, y + h - 40, x + w - 18, y + h - 12], fill=(232, 122, 42))
    d.text((x + 12, y + h - 30), "NO DEAL", font=F_NUM, fill=(255, 255, 255))

def banner_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 38, 64))
    cx = x + w // 2
    # capitol dome silhouette
    d.rectangle([cx - 52, y + 74, cx + 52, y + 112], fill=(247, 243, 234))
    d.pieslice([cx - 42, y + 30, cx + 42, y + 82], 180, 360, fill=(247, 243, 234))
    d.rectangle([cx - 4, y + 18, cx + 4, y + 34], fill=(247, 243, 234))
    for i in range(-2, 3):
        d.rectangle([cx + i * 20 - 3, y + 84, cx + i * 20 + 3, y + 110],
                    fill=(24, 38, 64))
    d.text((x + w - 78, y + 10), "258", font=F_BIG_NUM, fill=(255, 255, 255))

def banner_dymer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 58, 62))
    # standing block left, collapsed jagged block right
    d.rectangle([x + 16, y + 34, x + 96, y + 112], fill=(210, 205, 192))
    for r in range(3):
        for c in range(3):
            d.rectangle([x + 28 + c * 22, y + 46 + r * 22,
                         x + 44 + c * 22, y + 60 + r * 22], fill=(58, 58, 62))
    d.polygon([(x + 120, y + 112), (x + 140, y + 66), (x + 168, y + 88),
               (x + 196, y + 60), (x + 228, y + 92), (x + 252, y + 112)],
              fill=(150, 143, 128))
    d.line([x + 30, y + 8, x + 150, y + 40], fill=(232, 196, 90), width=3)
    d.text((x + w - 52, y + h - 30), "11", font=F_BIG_NUM, fill=(255, 255, 255))

BANNERS = {"cop": banner_cop, "house": banner_house, "dymer": banner_dymer}

# ---- stylised world map ------------------------------------------------------
# Rough continent outlines as (lon, lat) polygons; equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-80, 32), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-165, 60)],
    [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-77, -12)],
    [(-10, 36), (-2, 37), (5, 38), (12, 42), (18, 40), (23, 36), (28, 41),
     (30, 46), (20, 50), (12, 55), (8, 58), (5, 60), (-5, 58), (-10, 50),
     (-10, 43)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (28, -28), (20, -35),
     (15, -30), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(30, 70), (50, 70), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 45), (140, 40),
     (130, 35), (122, 30), (115, 22), (108, 12), (103, 8), (100, 8), (95, 15),
     (90, 22), (85, 20), (80, 13), (75, 8), (70, 20), (65, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (45, 35), (40, 38), (35, 36), (30, 36),
     (28, 42), (30, 45), (30, 50), (35, 55), (40, 60), (35, 65)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -14),
     (114, -22)],
]
# numbered pins: (lon, lat, label, label dx, label dy) — 2 and 13 share
# one Washington dot, labelled "2·13", so the two stories stay visible.
# Dots are nudged a few degrees where the map scale would merge them;
# the map is stylised, not a survey chart.
PINS = [
    (30.7, 36.9, "1", -4, -16), (-77.0, 38.9, "2·13", -12, -16),
    (33.0, 56.0, "3", 6, -14), (56.5, 26.6, "4", 8, -6),
    (20.1, 32.1, "5", -16, 8), (35.2, 31.9, "6", 6, 10),
    (-70.0, 44.0, "7", 6, -8), (28.0, -26.2, "8", 8, -6),
    (-88.0, 30.0, "9", -16, -6), (127.0, 37.5, "10", 8, -6),
    (32.5, 15.6, "11", 8, -6), (106.1, -6.2, "12", 8, -6),
]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 242))
    d.rectangle([x, y, x + w, y + h], outline=GREY_LINE, width=1)
    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (90.0 - lat) / 180.0 * h
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(148, 168, 178))
    for lon, lat, lbl, dx, dy in PINS:
        px, py = proj(lon, lat)
        r = 5
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px + dx, py + dy), lbl, font=F_MAP_LBL, fill=RED)

# ---- page assembly -----------------------------------------------------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 92], fill=INK)
    d.text((24, 12), "THE WORLD IN ONE IMAGE", font=F_TITLE, fill=(255, 255, 255))
    d.text((24, 66), MASTHEAD_STRAP, font=F_STRAP, fill=(232, 196, 90))
    d.rectangle([0, 92, W, 96], fill=RED)

    # stat strip
    y0 = 96
    cw = W // 6
    for i, (num, lbl) in enumerate(STATS):
        cx = i * cw + cw // 2
        d.text((cx, y0 + 8), num, font=F_STAT_N, fill=RED, anchor="ma")
        d.text((cx, y0 + 46), lbl, font=F_STAT_L, fill=INK_SOFT, anchor="ma")
        if i:
            d.line([i * cw, y0 + 10, i * cw, y0 + 62], fill=GREY_LINE, width=1)
    d.line([0, 168, W, 168], fill=GREY_LINE, width=1)

    # features: three columns
    fx, fy, fw, fh = 24, 180, 312, 272
    gap = 16
    for i, f in enumerate(FEATURES):
        x = fx + i * (fw + gap)
        d.rectangle([x, fy, x + fw, fy + fh], fill=CARD, outline=GREY_LINE, width=1)
        BANNERS[f["art"]](d, x + 1, fy + 1, fw - 2, 118)
        ty = fy + 130
        d.text((x + 12, ty), f["num"] + "  " + f["place"] + " — " + f["cat"],
               font=F_KICK, fill=RED)
        ty += 20
        for ln in wrap(d, f["head"], F_HEAD, fw - 24):
            d.text((x + 12, ty), ln, font=F_HEAD, fill=INK)
            ty += 24
        ty += 4
        for ln in wrap(d, f["deck"], F_DECK, fw - 24):
            d.text((x + 12, ty), ln, font=F_DECK, fill=INK_SOFT)
            ty += 18
        d.text((x + 12, fy + fh - 20), f["src"], font=F_FOOT, fill=MUTED)

    # smalls: two columns x five rows
    sy = 464
    col_w = (W - 48 - 16) // 2
    row_h = 50
    for i, (num, place, cat, head, deck, src) in enumerate(SMALLS):
        col, row = i % 2, i // 2
        x = 24 + col * (col_w + 16)
        y = sy + row * row_h
        d.text((x, y), num, font=F_NUM, fill=RED)
        d.text((x + 34, y), place + " — " + cat, font=F_KICK, fill=INK_SOFT)
        d.text((x + 34, y + 14), head, font=F_SMALL_HEAD, fill=INK)
        for j, ln in enumerate(wrap(d, deck, F_SMALL_DECK, col_w - 34)):
            if j >= 1:
                break
            d.text((x + 34, y + 31), ln, font=F_SMALL_DECK, fill=MUTED)
        if row < 4:
            d.line([x, y + row_h - 1, x + col_w, y + row_h - 1],
                   fill=GREY_LINE, width=1)
    d.line([0, 720, W, 720], fill=GREY_LINE, width=1)

    # map + region chips
    my = 728
    draw_map(d, 24, my, 660, 110)
    d.text((24, my + 114), "WHERE IT HAPPENED — pins 01–13 match the stories above",
           font=F_KICK, fill=INK_SOFT)
    chip_x, chip_y = 708, my + 2
    d.text((chip_x, chip_y), "STORIES BY REGION", font=F_KICK, fill=RED)
    chip_y += 22
    for chip in REGION_CHIPS:
        tw = d.textlength(chip, font=F_STAT_L) + 18
        d.rounded_rectangle([chip_x, chip_y, chip_x + tw, chip_y + 22],
                            radius=11, fill=INK)
        d.text((chip_x + 9, chip_y + 4), chip, font=F_STAT_L,
               fill=(255, 255, 255))
        chip_y += 24

    # briefs: two columns
    by = 856
    d.text((24, by), "ALSO TODAY", font=F_KICK, fill=RED)
    by += 18
    bcol_w = (W - 48 - 16) // 2
    for i, (place, txt) in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x = 24 + col * (bcol_w + 16)
        y = by + row * 15
        line = place + ": " + txt
        d.text((x, y), "•  ", font=F_BRIEF, fill=RED)
        d.text((x + 12, y), line, font=F_BRIEF, fill=INK_SOFT)

    # date check + footer
    d.rectangle([0, 984, W, 1006], fill=(253, 238, 214))
    d.text((24, 988), "DATE CHECK", font=F_KICK, fill=RED)
    d.text((118, 988), DATE_CHECK, font=F_FOOT, fill=INK_SOFT)
    d.text((24, 1010), FOOTER, font=F_FOOT, fill=MUTED)
    return img

def main():
    img = render()
    img.save(OUT, format="PNG", optimize=True)

if __name__ == "__main__":
    main()
