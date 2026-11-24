#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026.

Pure Pillow drawing, no network, no randomness, no timestamps.
Deterministic: two runs write byte-identical PNGs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 30)
BLUE = (31, 68, 110)
TEAL = (18, 96, 92)
GOLD = (184, 134, 11)
GREY = (90, 86, 78)
RULE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
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


def draw_globe(d, cx, cy, r, sea, land, ink):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=sea, outline=ink, width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.7, cx + r * 0.15, cy - r * 0.1],
              fill=land)
    d.ellipse([cx - r * 0.1, cy + r * 0.05, cx + r * 0.6, cy + r * 0.65],
              fill=land)
    d.ellipse([cx - r * 0.75, cy + r * 0.35, cx - r * 0.2, cy + r * 0.7],
              fill=land)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=ink, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=ink, width=1)


def draw_tanker_scene(d, x0, y0, x1, y1):
    """Flat vector: tanker, mines and sun over the Strait of Hormuz."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 238))
    # sun
    d.ellipse([x1 - 78, y0 + 14, x1 - 30, y0 + 62], fill=(232, 164, 32))
    # gulls
    for gx, gy in ((x0 + 30, y0 + 26), (x0 + 62, y0 + 40), (x0 + 96, y0 + 22)):
        d.arc([gx, gy, gx + 16, gy + 10], 200, 340, fill=INK, width=2)
        d.arc([gx + 14, gy, gx + 30, gy + 10], 200, 340, fill=INK, width=2)
    sea_y = y0 + 118
    d.rectangle([x0, sea_y, x1, y1], fill=(46, 110, 138))
    d.rectangle([x0, sea_y, x1, sea_y + 5], fill=(120, 180, 200))
    # waves
    for wy in (sea_y + 22, sea_y + 42):
        for wx in range(x0 + 8, x1 - 30, 46):
            d.arc([wx, wy, wx + 34, wy + 12], 180, 360, fill=(150, 200, 215),
                  width=2)
    # tanker hull
    hx0, hx1 = x0 + 26, x1 - 26
    hy0, hy1 = sea_y - 34, sea_y + 30
    d.polygon([(hx0, hy0), (hx1, hy0), (hx1 - 14, hy1), (hx0 + 14, hy1)],
              fill=(52, 52, 58))
    d.rectangle([hx0 + 6, hy0 - 26, hx0 + 118, hy0], fill=(176, 42, 30))
    d.rectangle([hx0 + 122, hy0 - 40, hx0 + 196, hy0], fill=(232, 228, 216))
    d.rectangle([hx0 + 130, hy0 - 52, hx0 + 150, hy0 - 40],
                fill=(232, 228, 216))
    d.rectangle([hx0 + 200, hy0 - 18, hx0 + 252, hy0], fill=(184, 134, 11))
    # containers
    for i, col in enumerate(((232, 164, 32), (46, 110, 138), (18, 96, 92),
                             (176, 42, 30))):
        cx = hx0 + 210 + i * 0  # placeholder kept deterministic
        _ = cx
    # deck containers row
    cx = hx0 + 206
    for col in ((232, 164, 32), (18, 96, 92), (176, 42, 30)):
        d.rectangle([cx, hy0 - 16, cx + 26, hy0], fill=col)
        cx += 28
    # funnel smoke
    for i, r in enumerate((6, 9, 12)):
        d.ellipse([hx0 + 128 + i * 10, hy0 - 66 - i * 8,
                   hx0 + 128 + i * 10 + r * 2, hy0 - 66 - i * 8 + r * 2],
                  fill=(200, 196, 186))
    # naval mines
    for mx, my in ((x1 - 66, sea_y + 40), (x0 + 44, sea_y + 52)):
        d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(26, 26, 26))
        for ang in range(0, 360, 45):
            import math
            a = math.radians(ang)
            d.line([mx + 10 * math.cos(a), my + 10 * math.sin(a),
                    mx + 16 * math.cos(a), my + 16 * math.sin(a)],
                   fill=(26, 26, 26), width=2)


def icon_skyline(d, x, y, s, col):
    d.rectangle([x, y + s * 0.35, x + s * 0.22, y + s], fill=col)
    d.rectangle([x + s * 0.26, y, x + s * 0.5, y + s], fill=col)
    d.rectangle([x + s * 0.54, y + s * 0.5, x + s * 0.78, y + s], fill=col)
    d.rectangle([x + s * 0.82, y + s * 0.25, x + s, y + s], fill=col)
    d.rectangle([x + s * 0.34, y + s * 0.12, x + s * 0.42, y + s * 0.2],
                fill=col)


def icon_mountains(d, x, y, s, col):
    d.polygon([(x, y + s), (x + s * 0.35, y + s * 0.1), (x + s * 0.65, y + s)],
              fill=col)
    d.polygon([(x + s * 0.4, y + s), (x + s * 0.75, y),
               (x + s, y + s)], fill=(120, 120, 110))
    d.ellipse([x + s * 0.72, y, x + s * 0.95, y + s * 0.23],
              fill=(232, 164, 32))


def icon_stars(d, x, y, s, col):
    import math
    for i in range(12):
        a = math.radians(i * 30 - 90)
        px = x + s / 2 + (s * 0.38) * math.cos(a)
        py = y + s / 2 + (s * 0.38) * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
    d.ellipse([x + s * 0.32, y + s * 0.32, x + s * 0.68, y + s * 0.68],
              fill=(232, 164, 32))


def icon_dome(d, x, y, s, col):
    d.rectangle([x + s * 0.08, y + s * 0.55, x + s * 0.92, y + s], fill=col)
    d.pieslice([x + s * 0.2, y + s * 0.05, x + s * 0.8, y + s * 0.75],
               180, 360, fill=col)
    d.rectangle([x + s * 0.86, y + s * 0.15, x + s * 0.94, y + s], fill=col)
    d.ellipse([x + s * 0.84, y + s * 0.08, x + s * 0.96, y + s * 0.2],
              fill=col)


def icon_acacia(d, x, y, s, col):
    d.polygon([(x + s * 0.46, y + s * 0.45), (x + s * 0.54, y + s * 0.45),
               (x + s * 0.56, y + s), (x + s * 0.44, y + s)], fill=(90, 60, 30))
    d.ellipse([x, y, x + s, y + s * 0.5], fill=col)
    d.ellipse([x + s * 0.68, y + s * 0.18, x + s, y + s], fill=(232, 164, 32))


def icon_pagoda(d, x, y, s, col):
    for i in range(3):
        wy = y + s * (0.25 + i * 0.25)
        ww = s * (0.95 - i * 0.18)
        d.polygon([(x + (s - ww) / 2, wy), (x + s / 2, wy - s * 0.12),
                   (x + (s + ww) / 2, wy)], fill=col)
        d.rectangle([x + s * 0.32, wy, x + s * 0.68, wy + s * 0.14],
                    fill=col)
    d.rectangle([x + s * 0.42, y + s * 0.85, x + s * 0.58, y + s], fill=col)


def icon_globe(d, x, y, s, col):
    draw_globe(d, x + s / 2, y + s / 2, s / 2 - 1, (150, 200, 215),
               (18, 96, 92), INK)


ICONS = {
    "skyline": icon_skyline,
    "mountains": icon_mountains,
    "stars": icon_stars,
    "dome": icon_dome,
    "acacia": icon_acacia,
    "pagoda": icon_pagoda,
    "globe": icon_globe,
}

# (region, colour, icon, [(lead, detail), ...])
REGIONS = [
    ("NORTH AMERICA", BLUE, "skyline", [
        ("Nvidia brings back Jensen Huang",
         "Board reinstates CEO after Trump push; Nasdaq jumps 6.5%."),
        ("Trump pardons turkeys Freedom, Feather",
         "White House Thanksgiving rite for two West Virginia birds."),
        ("Measles kills ninth in Pennsylvania",
         "State outbreak reaches 1,638 cases across 46 counties."),
        ("Army to detonate unstable explosives",
         "Court clears Iowa blast of nearly five tons of lead azide."),
        ("States sue SpaceX over Grok images",
         "Oregon and Virginia allege AI-made child abuse images."),
    ]),
    ("EUROPE", (90, 40, 90), "stars", [
        ("Russia warns Estonia of open war",
         "Moscow fumes over plan to close border crossings on Dec. 1."),
        ("Spain amnesties Puigdemont",
         "Top court ends cases over 2017 Catalan independence bid."),
        ("Germany gets Ukraine's Delta system",
         "First ally granted access to Kyiv's battlefield software."),
        ("UK warns of Russian sabotage risk",
         "Firms supplying Ukraine told to guard against attacks."),
        ("EU to rethink climate summit rules",
         "After COP31 collapsed in Antalya with no fossil-fuel deal."),
        ("Bomb threats hit schools in Denmark",
         "Hundreds of schools emailed; police say carry on as normal."),
    ]),
    ("ASIA-PACIFIC", TEAL, "pagoda", [
        ("Russian jets enter Korea defence zone",
         "Seoul scrambles jets; island shelter alert issued, then lifted."),
        ("China probes Politburo member Chen",
         "Shanghai party chief faces corruption investigation."),
        ("Hasina plans return to Bangladesh",
         "Ousted PM says she will come home on Dec. 16, Victory Day."),
        ("Malaysia to send Rohingya back",
         "Thousands to be returned to Myanmar by ship and plane."),
        ("Court: Myanmar committed genocide",
         "World Court rules on Rohingya; UK sanctions five generals."),
        ("Hanoi restaurant blast kills six",
         "Hot-pot eatery explosion injures at least ten in Dong Da."),
        ("Quake shakes Nepal's Koshi province",
         "Magnitude 5.3 tremor reported; no major damage yet known."),
    ]),
    ("LATIN AMERICA", (150, 70, 20), "mountains", [
        ("Car bomb injures 23 in Colombia",
         "Blast outside regional offices in Villavicencio."),
        ("Mexico captures 'El Chapo Isidro'",
         "Cartel figure held with US intelligence help, officials say."),
        ("Salvadoran troops die in Haiti blast",
         "Soldiers killed in explosion at their camp in Haiti."),
        ("Brazil cuts 2027 growth forecast",
         "Economy ministry trims outlook as the real weakens."),
    ]),
    ("MIDDLE EAST", RED, "dome", [
        ("Israel kills Hamas security chief",
         "Gaza strike kills Naeem Abu Nahel and six others, medics say."),
        ("Houthis hit Riyadh's tallest tower",
         "Second strike in five days injures 11; fighters near Aden."),
        ("Iraq takes over Kurdish oilfields",
         "PM orders ministry to run fields in four provinces."),
        ("Ukraine sinks Russian ship off Libya",
         "Naval drones hit corvette in Benghazi port; UN seeks probe."),
        ("Libya's Haftar visits Turkey",
         "Commander in Ankara for first time, to meet Erdogan."),
    ]),
    ("AFRICA", (120, 90, 10), "acacia", [
        ("Senegal champions again, court rules",
         "CAS restores AFCON title; Morocco's forfeit win overturned."),
        ("Fighting traps Ebola teams in Congo",
         "Clashes near Ituri hospital halt responders for a day."),
        ("Congo pushes miners to share locally",
         "Foreign miners told to open units to Congolese shareholders."),
        ("Somalia, Uganda step up al-Shabaab fight",
         "Allies intensify operations as troop withdrawal begins."),
        ("UN urges probe into Benghazi attacks",
         "Mission calls for inquiry after strikes on Libyan port."),
    ]),
    ("SCIENCE & SPORT", (40, 90, 60), "globe", [
        ("Super Bowl LXI heads to IMAX",
         "NFL and ESPN to show the big game on cinema screens."),
        ("Pope Francis diary made public",
         "Vatican publishes notes; he wrote of seeing the devil."),
        ("Rocket test keeps medicine stable",
         "Adelaide coating survives launch and weightlessness."),
        ("Cargo ship heads for space station",
         "Russia's Progress 97 launches; docks on Thanksgiving Day."),
    ]),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_mast = font(SERIF, 44)
    f_date = font(SANSB, 17)
    f_tag = font(SANS, 12)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 12), title, font=f_mast, fill=INK)
    d.line([16, 66, W - 16, 66], fill=RED, width=3)
    date_line = "TUESDAY  24  NOVEMBER  2026"
    dw = d.textlength(date_line, font=f_date)
    d.text(((W - dw) / 2, 74), date_line, font=f_date, fill=RED)
    tag = "ONE DAY  •  ONE PAGE  •  37 STORIES FROM SEVEN REGIONS"
    tw2 = d.textlength(tag, font=f_tag)
    d.text(((W - tw2) / 2, 98), tag, font=f_tag, fill=GREY)

    # ---- headline zone ----
    y = 122
    d.line([16, y, W - 16, y], fill=INK, width=2)
    y += 10
    f_kick = font(SANSB, 14)
    f_head = font(SERIF, 33)
    f_deck = font(SANS, 15)
    d.text((18, y), "THE STRAIT OF HORMUZ", font=f_kick, fill=RED)
    y += 22
    head_lines = [
        "Tankers hit mines in Hormuz",
        "as Iran vows to defy the",
        "US blockade",
    ]
    for ln in head_lines:
        d.text((18, y), ln, font=f_head, fill=INK)
        y += 38
    y += 4
    deck = ("Tehran says ships that defied its rules struck mines and "
            "caught fire. The US Navy holds the strait as Vance and "
            "Rubio meet Qatar's prime minister at the White House.")
    for ln in wrap(d, deck, f_deck, 600):
        d.text((18, y), ln, font=f_deck, fill=(50, 48, 44))
        y += 20
    # headline illustration, right side
    draw_tanker_scene(d, 648, 132, 1008, 312)
    d.text((648, 316), "A tanker in the Strait of Hormuz.",
           font=font(SANS, 11), fill=GREY)

    # ---- region grid: two columns ----
    grid_y = 336
    grid_bottom = 994
    col_w = 492
    cols = [[REGIONS[0], REGIONS[1], REGIONS[2]],
            [REGIONS[3], REGIONS[4], REGIONS[5], REGIONS[6]]]
    f_reg = font(SANSB, 15)
    f_lead = font(SANSB, 12)
    f_det = font(SANS, 11)
    for ci, col in enumerate(cols):
        x = 16 + ci * (col_w + 8)
        cy = grid_y
        for name, colr, icon, stories in col:
            # header
            d.rectangle([x, cy, x + col_w, cy + 24], fill=colr)
            ICONS[icon](d, x + 6, cy + 2, 20, (247, 243, 232))
            d.text((x + 34, cy + 4), name, font=f_reg, fill=(255, 255, 255))
            cy += 24
            for lead, det in stories:
                cy += 2
                d.text((x + 2, cy), lead, font=f_lead, fill=INK)
                cy += 13
                d.text((x + 2, cy), det, font=f_det, fill=(60, 58, 52))
                cy += 12
            cy += 4
            d.line([x, cy, x + col_w, cy], fill=RULE, width=1)
            cy += 6
        assert cy <= grid_bottom, (ci, cy)

    # ---- footer ----
    d.line([16, 998, W - 16, 998], fill=INK, width=1)
    f_foot = font(SANS, 10)
    foot = ("Sources: AP, Reuters, Just Security, Nature, NASA, Court of Arbitration "
            "for Sport, UN News  •  Drawn by code; no photographs  •  Tuesday 24 November 2026")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 1006), foot, font=f_foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
