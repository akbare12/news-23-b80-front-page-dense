#!/usr/bin/env python3
"""news-23 b80 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

def font(name, size):
    paths = {
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except Exception:
        return ImageFont.load_default()

def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(d, x, y, label, fill):
    f = font("sansb", 8)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill="white")
    return w

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 50], fill="black")
d.text((12, 5), "THE WORLD TODAY", font=font("serifb", 40), fill="white")
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 12 - d.textlength(dt, font=font("sansb", 18)), 15), dt,
       font=font("sansb", 18), fill="#E8B93C")

# ---------- kicker ----------
d.rectangle([0, 50, W, 74], fill="#A6192E")
kick = "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B"
kf = font("sansb", 16)
d.text(((W - d.textlength(kick, font=kf)) / 2, 54), kick, font=kf, fill="white")

# ---------- number strip (2 rows x 5) ----------
strip = [
    [("-3.3%", "KOSPI", "#C0392B"), ("5.3", "US-CHINA POWER GAP", "#1F4E79"),
     ("11,762", "EBOLA CASES, DRC", "#1E7A34"), ("10T won", "SEOUL STABILISATION FUND", "#8B6914"),
     ("2%", "BILLIONAIRE TAX IN PARIS", "#6A3FA0")],
    [("$450M", "SKUBAL DEAL", "#1F4E79"), ("165", "RUSSIAN MISSILES/WEEK", "#C0392B"),
     ("12,000", "CLEARED IN MANCHESTER", "#1E7A34"), ("264 kg", "EXPLOSIVES SEIZED", "#8B6914"),
     ("$107.3B", "ANTHROPIC IPO", "#6A3FA0")],
]
colw = W // 5
for r, row in enumerate(strip):
    y0 = 76 + r * 27
    for c, (val, lab, col) in enumerate(row):
        x = c * colw + 10
        d.text((x, y0), val, font=font("sansb", 18), fill=col)
        d.text((x, y0 + 18), lab, font=font("sans", 8), fill="#555555")

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", 7, "#1F4E79"), ("AMERICAS 8", 8, "#A6192E"),
           ("MIDDLE EAST 6", 6, "#8B6914"), ("EUROPE 5", 5, "#0E7C6B"),
           ("AFRICA 3", 3, "#6A3FA0"), ("WORLD 2", 2, "#333333")]
x = 0
for name, cnt, col in regions:
    w = round(cnt / 31 * W)
    d.rectangle([x, 132, x + w, 152], fill=col)
    tf = font("sansb", 11)
    d.text((x + (w - d.textlength(name, font=tf)) / 2, 137), name, font=tf, fill="white")
    x += w

# ---------- UTC strip ----------
d.text((10, 155), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
       font=font("sans", 10), fill="#444444")
d.text((W - 10 - d.textlength("~ APPROX", font=font("sans", 10)), 155), "~ APPROX",
       font=font("sans", 10), fill="#888888")

# ---------- heroes ----------
heroes = [
    dict(scene="kospi", headline="AI ROUT HITS ASIA",
         body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="KOREA EXCHANGE"),
    dict(scene="guterres", headline="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         src="UNITED NATIONS"),
    dict(scene="power", headline="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
         src="LOWY INSTITUTE"),
]
hx = [8, 350, 692]
hw = 324
hy = 170          # scene top
scene_h = 112
src_y = hy + scene_h          # 280, black source strip
head_y = src_y + 18           # 298
for i, hr in enumerate(heroes):
    x0 = hx[i]
    # scene
    if hr["scene"] == "kospi":
        d.rectangle([x0, hy, x0 + hw, hy + scene_h], fill="#101B33")
        # buildings with lit windows
        import random
        rnd = random.Random(23)
        bx = x0 + 8
        while bx < x0 + hw - 24:
            bw = rnd.randint(18, 30)
            bh = rnd.randint(38, 78)
            d.rectangle([bx, hy + scene_h - bh, bx + bw, hy + scene_h], fill="#1E2F52")
            for wy in range(hy + scene_h - bh + 5, hy + scene_h - 4, 9):
                for wx in range(bx + 3, bx + bw - 3, 7):
                    if rnd.random() < 0.55:
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill="#F2C94C")
            bx += bw + 4
        # orange chart line, kept below the big -3.3% label
        pts = [(x0 + 12, hy + 88), (x0 + 60, hy + 78), (x0 + 110, hy + 84),
               (x0 + 160, hy + 66), (x0 + 210, hy + 72), (x0 + 260, hy + 56),
               (x0 + 312, hy + 48)]
        d.line(pts, fill="#F2994A", width=3)
        for p in pts:
            d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill="white")
        d.text((x0 + 10, hy + 6), "-3.3%", font=font("sansb", 28), fill="#FF5A4E")
    elif hr["scene"] == "guterres":
        d.rectangle([x0, hy, x0 + hw, hy + scene_h], fill="#0E6B5C")
        gf = font("sansb", 24)
        for j, ln in enumerate(["150 DELEGATES", "BACK A RISK", "FRAMEWORK"]):
            d.text((x0 + 10, hy + 10 + j * 30), ln, font=gf, fill="#E8B93C")
        # globe, right side, clear of text
        cx, cy, r = x0 + hw - 48, hy + 56, 36
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#BFE3D8", outline="white", width=2)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline="#0E6B5C", width=2)
        d.line([cx - r, cy, cx + r, cy], fill="#0E6B5C", width=2)
        d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill="#0E6B5C", width=2)
        d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill="#0E6B5C", width=2)
    else:  # power index bars
        d.rectangle([x0, hy, x0 + hw, hy + scene_h], fill="#F7F1DC")
        d.text((x0 + 10, hy + 6), "NARROWEST SINCE 2018", font=font("sans", 10), fill="#666666")
        d.text((x0 + hw - 10 - d.textlength("GAP 5.3", font=font("sansb", 10)), hy + 6),
               "GAP 5.3", font=font("sansb", 10), fill="#C0392B")
        bars = [("78.9", "US", 70, "#1F4E79"), ("73.6", "CHINA", 65, "#C0392B"),
                ("40.5", "INDIA", 36, "#D9A441")]
        bw, gap = 62, 34
        bx = x0 + 28
        base = hy + scene_h - 6
        for val, lab, bh, col in bars:
            d.text((bx + (bw - d.textlength(val, font=font("sansb", 15))) / 2, base - bh - 20),
                   val, font=font("sansb", 15), fill="#222222")
            d.rectangle([bx, base - bh, bx + bw, base], fill=col)
            lf = font("sansb", 11)
            d.text((bx + (bw - d.textlength(lab, font=lf)) / 2, base - 16), lab, font=lf, fill="white")
            bx += bw + gap
    # black source strip
    d.rectangle([x0, src_y, x0 + hw, src_y + 16], fill="black")
    d.text((x0 + 6, src_y + 3), hr["src"], font=font("sansb", 9), fill="white")
    # headline (max 2 lines, clear of the strip above)
    hf = font("sansb", 19)
    hlines = wrap(d, hr["headline"], hf, hw)
    for j, ln in enumerate(hlines[:2]):
        d.text((x0, head_y + j * 21), ln, font=hf, fill="black")
    # body (max 2 lines)
    bf = font("sans", 12)
    blines = wrap(d, hr["body"], bf, hw)
    by = head_y + len(hlines[:2]) * 21 + 4
    for j, ln in enumerate(blines[:2]):
        d.text((x0, by + j * 15), ln, font=bf, fill="#222222")
    # chip on its own row below the body
    chip(d, x0, by + len(blines[:2]) * 15 + 4, "REPORTED", "#1F4E79")

# ---------- MORE OF THE DAY bar ----------
d.rectangle([0, 410, W, 432], fill="black")
d.text((10, 415), "MORE OF THE DAY  —  10 STORIES", font=font("sansb", 14), fill="white")

# ---------- cards ----------
cards = [
    ("AMERICAS", 1, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", "#1F4E79"),
    ("FBI", 2, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", "#2E5090"),
    ("WHITE HOUSE", 3, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", "#8B6914"),
    ("MARKETS", 4, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", "#0E7C6B"),
    ("SPORT", 5, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", "#A6192E"),
    ("SPORT", 6, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", "#A6192E"),
    ("LEGAL", 7, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", "#6A3FA0"),
    ("TECH", 8, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", "#1F6FB2"),
    ("EUROPE", 9, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", "#B05A00"),
    ("SPACE", 10, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", "#5B2D8E"),
]
cw, chh = 196, 86
cgap = 7
for idx, (cat, num, head, body, src, tag, col) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = 8 + c * (cw + cgap)
    y0 = 440 + r * (chh + 7)
    # category bar
    d.rectangle([x0, y0, x0 + cw, y0 + 16], fill=col)
    d.text((x0 + 5, y0 + 3), cat, font=font("sansb", 10), fill="white")
    nstr = str(num)
    d.text((x0 + cw - 5 - d.textlength(nstr, font=font("sansb", 10)), y0 + 3),
           nstr, font=font("sansb", 10), fill="white")
    # headline, max 2 lines
    hf = font("sansb", 13)
    hlines = wrap(d, head, hf, cw - 4)
    for j, ln in enumerate(hlines[:2]):
        d.text((x0 + 2, y0 + 20 + j * 15), ln, font=hf, fill="black")
    # body on its own line(s) below headline
    bf = font("sans", 11)
    by = y0 + 20 + len(hlines[:2]) * 15 + 2
    blines = wrap(d, body, bf, cw - 4)
    for j, ln in enumerate(blines[:1]):
        d.text((x0 + 2, by + j * 13), ln, font=bf, fill="#333333")
    # source + chip on the bottom row, chip clear of the body
    d.text((x0 + 2, y0 + chh - 13), src, font=font("sans", 9), fill="#666666")
    chip(d, x0 + cw - 68, y0 + chh - 14, tag, "#1F4E79" if tag == "REPORTED" else "#C0392B")

# ---------- map + ALSO ----------
my = 626
d.rectangle([0, my, W, my + 22], fill="black")
d.text((10, my + 4), "WHERE IT HAPPENED", font=font("sansb", 14), fill="white")
d.text((350, my + 4), "ALSO ON MONDAY", font=font("sansb", 14), fill="white")

# map box
mx, mw = 8, 330
mh = 218
d.rectangle([mx, my + 26, mx + mw, my + 26 + mh], outline="#999999", width=1, fill="#EFF7EC")
# blobs (stylised continents)
d.polygon([(mx + 22, my + 66), (mx + 52, my + 46), (mx + 82, my + 52), (mx + 102, my + 76),
           (mx + 92, my + 126), (mx + 72, my + 186), (mx + 52, my + 206), (mx + 32, my + 166),
           (mx + 17, my + 106)], fill="#BFDDB0")
d.polygon([(mx + 142, my + 56), (mx + 212, my + 41), (mx + 292, my + 46), (mx + 312, my + 76),
           (mx + 292, my + 116), (mx + 232, my + 126), (mx + 172, my + 116), (mx + 142, my + 86)],
          fill="#BFDDB0")
d.polygon([(mx + 162, my + 146), (mx + 202, my + 141), (mx + 217, my + 171), (mx + 192, my + 206),
           (mx + 167, my + 186)], fill="#BFDDB0")
pins = [(300, 732), (75, 817), (285, 722), (55, 712), (75, 697), (245, 717),
        (60, 747), (35, 747), (50, 772), (65, 792), (225, 707), (205, 702), (265, 702)]
# pins are absolute canvas coords, inside the map blobs (box top my+26=652,
# Americas blob y 672-832, Eurasia blob y 667-752); all pairs >=18px apart.
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill="#C0392B", outline="white", width=1)
    ns = str(i)
    d.text((px - d.textlength(ns, font=font("sansb", 9)) / 2, py - 5), ns,
           font=font("sansb", 9), fill="white")
# legend, 3 lines inside the box
lf = font("sans", 9)
for j, ln in enumerate(["Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing",
                        "4 Washington · 5 New York · 6 Kyiv · 7 Chicago · 8 SF",
                        "9 Denver · 10 Austin · 11 Warsaw · 12 London · 13 Moscow"]):
    d.text((mx + 6, my + 26 + mh - 40 + j * 12), ln, font=lf, fill="#333333")

# ALSO list
also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: the day after pact rejected", False),
    ("18. Benghazi: UN demands port probe [CLAIM]", True),
    ("19. Israel unity talks resume", False),
    ("20. Gaza: two killed in Israeli strike", False),
    ("21. West Bank settler attacks", False),
    ("22. Iran war: no deal in sight", False),
    ("23. Lebanon seizes 264 kg explosives", False),
    ("24. Bahrain: strike hits plant, 2 hurt", False),
    ("25. Sudan: defences down drones [CLAIM]", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits in exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
af = font("sans", 11)
for j, (txt, claim) in enumerate(also):
    y = my + 30 + j * 12
    if claim:
        base, tag = txt.rsplit(" [CLAIM]", 1)
        d.text((350, y), base, font=af, fill="black")
        d.text((350 + d.textlength(base + " ", font=af), y), "[CLAIM]",
               font=font("sansb", 11), fill="#C0392B")
    else:
        d.text((350, y), txt, font=af, fill="black")

# ---------- DATE CHECK ----------
dy = 878
d.rectangle([8, dy, W - 8, dy + 58], outline="#C0392B", width=2)
d.text((16, dy + 5), "DATE CHECK", font=font("sansb", 13), fill="#C0392B")
d.text((W - 16 - d.textlength("READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY",
                              font=font("sans", 9)), dy + 7),
       "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", font=font("sans", 9),
       fill="#C0392B")
d.text((16, dy + 24), "LEFT OUT — NOT 23 NOV: Dems 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo (22 Nov) · EU–Indonesia (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar (19 Nov)",
       font=font("sans", 11), fill="black")
d.text((16, dy + 40), "NOT YET — Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
       font=font("sans", 11), fill="black")

# ---------- footer ----------
fy = 944
ff = font("sans", 10)
d.text((10, fy), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
       font=ff, fill="#555555")
d.text((10, fy + 14), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
       font=ff, fill="#555555")
d.text((10, fy + 28), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=ff, fill="#555555")
gold = "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions"
gf = font("sansb", 13)
d.text(((W - d.textlength(gold, font=gf)) / 2, fy + 52), gold, font=gf, fill="#8B6914")

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
