#!/usr/bin/env python3
"""Draw the 25 Nov 2026 news-image entry (1024x1024 PNG).

Build tooling: lives OUTSIDE the entry repository, copied in for
transparency. Run `python3 draw.py` to regenerate entry.png.
All 37 stories happened or were first reported on 25 Nov 2026.
Sources: Reuters, AP, BBC, The Guardian, Economic Times, TechCrunch,
Variety, Mongabay, NWS, Sportradar.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 245, 238)
INK = (18, 18, 18)
RED = (179, 32, 44)
BLUE = (24, 64, 128)
GREY = (110, 108, 100)
LINE = (200, 196, 186)
LEAD_BG = (255, 255, 255)
STAT_BG = (232, 222, 200)

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, font, max_w):
    while draw.textlength(text, font=font) > max_w and len(text) > 3:
        text = text[:-4] + "..."
    return text


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


LEAD = {
    "tag": "MARKETS · THE SELL-OFF",
    "head": ["AI rally fizzles — Asia tumbles", "as tariff threat returns"],
    "summ": ("Fresh US tariff threats hit sentiment as the AI rebound stalls; "
              "chip-heavy markets bear the brunt, with Seoul and Taipei down "
              "over 5%."),
    "stat": "-2.8%",
    "stat_label": "Nikkei 225",
    "stat_sub": "Kospi -5.3% · Taiwan -5.1%",
    "stat_sub2": "Nvidia -5.9% Tuesday",
}

CARDS = [
    ("CHINA", "Shanghai pledges loyalty after Politburo probe",
     "Chen Jining probed; Shanghai leaders vow to see it through.", "Reuters"),
    ("SPACE", "Shenzhou-24 lifts off with first foreign astronaut",
     "Pakistan's Zeeshan Ali joins two Chinese crew bound for Tiangong.", "Reuters"),
    ("USA", "Trump: pardoning Jensen Huang is 'an option'",
     "Trump floats a pardon for the Nvidia chief amid conduct probes.", "TechCrunch"),
    ("FIFA", "Leaked papers reveal Infantino's 96-year plan",
     "Papers show a private equity plan for the World Cup, 96 years long.", "AP"),
    ("USA", "Army to blow up bomb-chemical stockpile in Iowa",
     "Five tons of unstable lead azide blown up before Thanksgiving.", "AP"),
    ("SPAIN", "Right challenges Sánchez in regional votes",
     "Conservative and far-right candidates take on a Socialist leader.", "AP"),
    ("AUSTRALIA", "Australia signs security pact with Solomons",
     "The deal is read as a blow to China's influence in the Pacific.", "Guardian"),
    ("AUSTRALIA", "Inflation jumps to 4.9%",
     "Prices climb faster than expected, deepening the cost-of-living crisis.", "Guardian"),
    ("USA", "Groups sue Trump over slavery exhibit",
     "Changes to a Philadelphia slavery exhibit draw a lawsuit.", "AP"),
    ("NVIDIA", "Huang apologises to staff: 'I'm in therapy'",
     "The reinstated chief faces staff after his hardest meeting and opens up.", "ET"),
]

TICKER = [
    "Nvidia shares slide as Trump's role is questioned",
    "US preparing to unveil new tariffs on partners",
    "Huang told staff he violated conduct code, source says",
    "Yale's Sonnenfeld: Nvidia a 'detriment' to US industry",
    "Trump's Nvidia move ties his fortunes to the AI boom",
    "Nvidia 'a good corporate citizen', says US attorney general",
    "UK consults on changing the age of consent",
    "UK energy price cap announced; bills set to soar",
    "Indian households squeezed by rising food prices",
    "Iran's Araghchi accuses US of hypocrisy at OPCW",
    "Jamaat-linked students renew anti-India rhetoric",
    "US GDP and inflation data due today",
    "Nikkei seen at 65,000 by June 2027, poll says",
    "East Coast storm brings rain and 50mph gusts",
    "Leipzig beat Lens 3-1 in the Champions League",
    "Beau Lamarre-Condon guilty of two murders",
    "Philip Rosenberg, Oscar-winning designer, dies at 91",
    "Oscars VFX top 20: Disney leads with four",
    "Dancing With the Stars finale tonight",
    "Species down to last 50 can still recover",
    "England has largest frailty gap in 31 countries",
    "Tiny cars take off across Europe",
    "UK White Christmas chances assessed",
    "Golden Goose flags India luxury hurdle",
    "North Koreans 'spied on, beaten, jailed for being Christian'",
    "Rangers dig it out against Aberdeen",
]

NUMBERS = [
    ("-2.8%", "Nikkei"),
    ("-5.3%", "Kospi"),
    ("-5.1%", "Taiwan shares"),
    ("4.9%", "Australia inflation"),
    ("5 tons", "bomb chemicals in Iowa"),
    ("96 yrs", "Infantino's World Cup plan"),
]

FOOTER = ("Sources: Reuters, AP, BBC, The Guardian, Economic Times, "
          "TechCrunch, Variety, Mongabay, NWS, Sportradar")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 24

    # ---- header ----
    d.text((m, 16), "THE WORLD", font=f(SERIF_B, 44), fill=INK)
    d.text((m, 66), "WEDNESDAY", font=f(SANS_B, 15), fill=RED)
    d.text((m, 84), "25 NOVEMBER 2026", font=f(SANS_B, 15), fill=INK)
    d.text((W - m, 66), "37 stories, all reported today",
           font=f(SANS, 13), fill=GREY, anchor="ra")
    d.line([(m, 100), (W - m, 100)], fill=INK, width=2)

    # ---- lead ----
    y = 104
    d.rectangle([m, y, W - m, y + 136], fill=LEAD_BG)
    d.text((m + 12, y + 8), LEAD["tag"], font=f(SANS_B, 12), fill=RED)
    d.text((m + 12, y + 28), LEAD["head"][0], font=f(SANS_B, 32), fill=INK)
    d.text((m + 12, y + 64), LEAD["head"][1], font=f(SANS_B, 32), fill=INK)
    for i, line in enumerate(wrap(d, LEAD["summ"], f(SANS, 14), 700)):
        d.text((m + 12, y + 100 + i * 18), line, font=f(SANS, 14), fill=INK)
    sx = W - m - 226
    d.rectangle([sx, y + 14, W - m - 12, y + 122], fill=STAT_BG)
    d.text((sx + 110, y + 26), LEAD["stat"], font=f(SANS_B, 44),
           fill=RED, anchor="ma")
    d.text((sx + 110, y + 74), LEAD["stat_label"], font=f(SANS_B, 13),
           fill=INK, anchor="ma")
    d.text((sx + 110, y + 94), LEAD["stat_sub"], font=f(SANS, 12),
           fill=INK, anchor="ma")
    d.text((sx + 110, y + 108), LEAD["stat_sub2"], font=f(SANS, 12),
           fill=INK, anchor="ma")
    d.line([(m, 246), (W - m, 246)], fill=LINE, width=1)

    # ---- cards: 2 cols x 5 rows ----
    cw, ch, cg = 488, 60, 8
    cy0 = 252
    for i, (tag, head, summ, src) in enumerate(CARDS):
        x = m + (i % 2) * (cw + cg)
        yy = cy0 + (i // 2) * 65
        d.text((x, yy), tag, font=f(SANS_B, 11), fill=RED)
        d.text((x + d.textlength(tag, font=f(SANS_B, 11)) + 8, yy), src,
               font=f(SANS, 11), fill=GREY)
        d.text((x, yy + 15), fit(d, head, f(SANS_B, 15), cw - 4),
               font=f(SANS_B, 15), fill=INK)
        d.text((x, yy + 36), fit(d, summ, f(SANS, 12), cw - 4),
               font=f(SANS, 12), fill=INK)
        d.line([(x, yy + 56), (x + cw, yy + 56)], fill=LINE, width=1)
    d.line([(m, 580), (W - m, 580)], fill=LINE, width=1)

    # ---- ticker ----
    d.text((m, 588), "THE DAY IN BRIEF", font=f(SANS_B, 13), fill=INK)
    d.line([(m, 610), (W - m, 610)], fill=INK, width=1)
    tw = (W - 2 * m - 16) // 2
    ty0, th = 620, 24
    for i, item in enumerate(TICKER):
        col, row = i % 2, i // 2
        x = m + col * (tw + 16)
        yy = ty0 + row * th
        d.text((x, yy), fit(d, item, f(SANS, 13), tw - 16),
               font=f(SANS, 13), fill=INK)
    d.line([(m, 936), (W - m, 936)], fill=INK, width=1)

    # ---- numbers strip ----
    n = len(NUMBERS)
    cw2 = (W - 2 * m) // n
    for i, (num, label) in enumerate(NUMBERS):
        cx = m + i * cw2 + cw2 // 2
        d.text((cx, 946), num, font=f(SANS_B, 20), fill=BLUE, anchor="ma")
        d.text((cx, 970), label, font=f(SANS, 11), fill=INK, anchor="ma")

    # ---- footer ----
    d.text((W - m, 1006), FOOTER, font=f(SANS, 10), fill=GREY, anchor="ra")

    out = "/home/hatch/workspace/makefun-setup/entries/news-image-20261125/entry.png"
    img.save(out, optimize=True)
    print("saved", out)


if __name__ == "__main__":
    main()
