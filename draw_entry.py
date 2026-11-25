#!/usr/bin/env python3
"""Draw entry.png: one front page summing up the world news of
Wednesday 25 November 2026. Editorial newspaper design, Pillow only.
Every story happened, or was first reported, on 25 November 2026
(verified against wire reports that day).
Run: python3 draw_entry.py  ->  writes entry.png (1024x1024).
"""
import math

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (247, 242, 228)
DARK = (14, 32, 58)
SEA = (24, 68, 100)
CRIMSON = (178, 34, 22)
SOFTRED = (255, 122, 92)
GOLD = (255, 198, 110)
BLACK = (22, 22, 22)
GREY = (70, 70, 70)
SNOW = (255, 255, 255)
BEACH = (216, 190, 134)
TEAL = (13, 116, 108)
VIOLET = (112, 54, 208)
ROYAL = (28, 76, 214)

BOLD_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def shrink_to(draw, text, path, size, width):
    """Biggest size at or under `size` that fits `width`."""
    while size > 10:
        trial = face(path, size)
        if draw.textlength(text, font=trial) <= width:
            return trial
        size -= 2
    return face(path, 10)


def flow(draw, text, fnt, width):
    """Word-wrap `text` to lines no wider than `width`."""
    out, current = [], ""
    for word in text.split():
        nxt = f"{current} {word}".strip()
        if draw.textlength(nxt, font=fnt) <= width:
            current = nxt
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def burst(draw, cx, cy, outer, colour):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = outer if i % 2 == 0 else outer * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=colour)


canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
pen = ImageDraw.Draw(canvas)
pen.rectangle([0, 0, PAGE - 1, PAGE - 1], outline=DARK, width=6)

# ---------- masthead ----------
pen.text((PAGE // 2, 30), "THE WORLD  ·  ONE DAY  ·  ONE PICTURE",
         font=face(BOLD, 26), fill=CRIMSON, anchor="ma")
date_face = shrink_to(pen, "WEDNESDAY 25 NOVEMBER 2026", BOLD_SERIF, 60, PAGE - 60)
pen.text((PAGE // 2, 62), "WEDNESDAY 25 NOVEMBER 2026", font=date_face,
         fill=DARK, anchor="ma")
pen.line([(28, 148), (PAGE - 28, 148)], fill=DARK, width=3)
pen.text((PAGE // 2, 156), "Every story below happened, or was first reported, on this day.",
         font=face(PLAIN, 22), fill=BLACK, anchor="ma")

# ---------- hero: Hormuz ----------
pen.rounded_rectangle([28, 190, PAGE - 28, 538], radius=18, fill=DARK)
pen.text((56, 212), "THE GULF  ·  MINES IN THE STRAIT", font=face(BOLD, 26),
         fill=SOFTRED)
pen.text((56, 246), "TWO TANKERS", font=face(BOLD_SERIF, 58), fill=SNOW)
pen.text((56, 306), "HIT BY MINES", font=face(BOLD_SERIF, 58), fill=SNOW)
hero_body = ("Iran says two oil tankers hit sea mines and burned "
             "in the Strait of Hormuz. Brent crude nears $91.")
body_face = face(PLAIN, 26)
for i, ln in enumerate(flow(pen, hero_body, body_face, 520)):
    pen.text((56, 388 + i * 35), ln, font=body_face, fill=(218, 228, 238))
pen.text((56, 496), "Houthis claim a strike on Ras Tanura refinery.",
         font=face(BOLD, 22), fill=GOLD)

# hero map panel: strait channel, two tankers, flames, mine burst
px0, py0, px1, py1 = 640, 212, 968, 518
pen.rounded_rectangle([px0, py0, px1, py1], radius=12, fill=SEA)
pen.polygon([(px0, py0), (px1, py0), (px1, py0 + 44), (px0 + 150, py0 + 88),
             (px0, py0 + 62)], fill=BEACH)
pen.polygon([(px0, py1), (px1, py1), (px1, py1 - 40), (px0 + 130, py1 - 80),
             (px0, py1 - 54)], fill=BEACH)
pen.text((px0 + 16, py0 + 118), "STRAIT OF", font=face(BOLD, 20), fill=SNOW)
pen.text((px0 + 16, py0 + 142), "HORMUZ", font=face(BOLD, 20), fill=SNOW)
# tanker one, with flame
pen.rectangle([px0 + 176, py0 + 176, px0 + 262, py0 + 198], fill=SNOW)
pen.rectangle([px0 + 200, py0 + 162, px0 + 226, py0 + 176], fill=SNOW)
pen.polygon([(px0 + 206, py0 + 162), (px0 + 218, py0 + 132),
             (px0 + 230, py0 + 162)], fill=GOLD)
# tanker two, with flame
pen.rectangle([px0 + 88, py0 + 216, px0 + 174, py0 + 238], fill=SNOW)
pen.rectangle([px0 + 112, py0 + 202, px0 + 138, py0 + 216], fill=SNOW)
pen.polygon([(px0 + 118, py0 + 202), (px0 + 130, py0 + 172),
             (px0 + 142, py0 + 202)], fill=GOLD)
burst(pen, px0 + 92, py0 + 92, 24, CRIMSON)

# ---------- four stories, 2 x 2 ----------
stories = [
    ("SPACE", ROYAL, "rocket",
     "Pakistan's first astronaut reaches orbit",
     "Shenzhou-24 docks at Tiangong in about 3\u00bd hours; Muhammad Zeeshan Ali aboard."),
    ("UKRAINE", (29, 78, 216), "drone",
     "Ukrainian drones hit Russian refineries",
     "Two Rosneft plants burn in Samara; Kyiv claims a Russian warship sunk off Libya."),
    ("COLOMBIA", VIOLET, "shield",
     "All hostages freed in Cartagena",
     "Dawn raid ends a ~17-hour siege at an \u00c9xito supermarket; 1 gunman killed, 4 held."),
    ("INDONESIA", CRIMSON, "mountain",
     "Illegal gold mine floods in Bogor",
     "9 dead, 18 trapped as a river floods a 100-metre pit; rescuers pump water."),
]
ox, oy = 28, 554
cw, ch, gp = 478, 146, 12
for n, (tag, tint, glyph, head, summ) in enumerate(stories):
    x = ox + (n % 2) * (cw + gp)
    y = oy + (n // 2) * (ch + gp)
    pen.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=SNOW,
                          outline=DARK, width=2)
    pen.rounded_rectangle([x, y, x + cw, y + 10], radius=5, fill=tint)
    pen.text((x + 16, y + 18), tag, font=face(BOLD, 22), fill=tint)
    ix, iy = x + cw - 54, y + 12
    if glyph == "rocket":
        pen.polygon([(ix + 20, iy + 2), (ix + 32, iy + 22), (ix + 20, iy + 30),
                     (ix + 8, iy + 22)], fill=tint)
        pen.polygon([(ix + 14, iy + 30), (ix + 20, iy + 42), (ix + 26, iy + 30)],
                    fill=GOLD)
    elif glyph == "drone":
        pen.rectangle([ix + 8, iy + 14, ix + 32, iy + 24], fill=tint)
        pen.line([(ix + 4, iy + 8), (ix + 12, iy + 8)], fill=tint, width=4)
        pen.line([(ix + 28, iy + 8), (ix + 36, iy + 8)], fill=tint, width=4)
        pen.line([(ix + 4, iy + 30), (ix + 12, iy + 30)], fill=tint, width=4)
        pen.line([(ix + 28, iy + 30), (ix + 36, iy + 30)], fill=tint, width=4)
    elif glyph == "shield":
        pen.polygon([(ix + 20, iy + 2), (ix + 36, iy + 8), (ix + 36, iy + 22),
                     (ix + 20, iy + 38), (ix + 4, iy + 22), (ix + 4, iy + 8)],
                    outline=tint, width=4)
        pen.text((ix + 13, iy + 12), "\u2713", font=face(BOLD, 20), fill=tint)
    else:  # mountain
        pen.polygon([(ix + 2, iy + 36), (ix + 16, iy + 6), (ix + 26, iy + 24),
                     (ix + 32, iy + 12), (ix + 40, iy + 36)], fill=tint)
    head_face = shrink_to(pen, head, BOLD_SERIF, 28, cw - 32)
    head_lines = flow(pen, head, head_face, cw - 32)[:2]
    for j, ln in enumerate(head_lines):
        pen.text((x + 16, y + 54 + j * 31), ln, font=head_face, fill=BLACK)
    sum_face = face(PLAIN, 20)
    base = y + 54 + len(head_lines) * 31
    for j, ln in enumerate(flow(pen, summ, sum_face, cw - 32)[:2]):
        pen.text((x + 16, base + j * 24), ln, font=sum_face, fill=GREY)

# ---------- bottom ticker ----------
pen.rounded_rectangle([28, 870, PAGE - 28, 994], radius=14, fill=DARK)
pen.text((56, 886), "ALSO ON 25 NOVEMBER", font=face(BOLD, 24), fill=GOLD)
pen.text((56, 920), "KOSPI plunges 6.16%  \u00b7  Dow closes above 50,000 for the first time",
         font=face(PLAIN, 23), fill=SNOW)
pen.text((56, 952), "Huawei guilty on 10 of 12 charges  \u00b7  Australia\u2013Solomon pact  \u00b7  19 killed in Sudan",
         font=face(PLAIN, 21), fill=SNOW)

canvas.save("entry.png", optimize=True)
print("wrote entry.png", canvas.size)
