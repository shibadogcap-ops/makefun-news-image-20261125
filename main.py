import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("MAKEFUN_BOT_DIR"):
    sys.path.insert(0, os.environ["MAKEFUN_BOT_DIR"])
import draw, font


def main():
    cv = draw.Canvas(1024, 1024, draw.PAPER)

    cv.frame(10, 10, 1004, 1004, draw.INK, 3)
    font.draw_text_center(cv, 512, 24, "THE WORLD IN ONE PICTURE",
                          draw.GREY, scale=2)
    font.draw_text_center(cv, 512, 44, "THE WEDNESDAY LEDGER",
                          draw.INK, scale=8)
    cv.rect(36, 108, 952, 5, draw.INK)
    cv.rect(36, 117, 952, 1, draw.INK)
    font.draw_text_center(cv, 512, 128, "WEDNESDAY, 25 NOVEMBER 2026",
                          draw.INK, scale=3)
    font.draw_text(cv, 36, 128, "NO. 25", draw.GREY, scale=2)
    font.draw_text_right(cv, 988, 128, "ONE PAGE ONLY", draw.GREY, scale=2)
    cv.rect(36, 158, 952, 2, draw.INK)

    font.draw_text(cv, 36, 172, "CHINA / POLITICS", draw.ACCENT, scale=2)
    font.draw_text_right(cv, 988, 172, "THE PURGE WIDENS",
                         draw.GREY, scale=2)
    font.draw_text(cv, 36, 196, "SHANGHAI", draw.INK, scale=11)
    font.draw_text(cv, 36, 281, "CHIEF FALLS", draw.INK, scale=11)

    # Shanghai skyline silhouettes, baseline y=274.
    buildings = [
        (776, 24, 52), (800, 20, 74), (820, 28, 44), (848, 22, 66),
        (870, 30, 38), (900, 26, 84), (926, 18, 58), (944, 26, 48),
        (970, 18, 70),
    ]
    for bx, bw, bh in buildings:
        cv.rect(bx, 274 - bh, bw, bh, draw.INK)

    # Oriental Pearl-style tower.
    cv.rect(906, 196, 6, 78, draw.INK)
    cv.circle(909, 236, 9, draw.INK)
    cv.circle(909, 210, 6, draw.INK)

    # Falling star with motion trail.
    cv.triangle(796, 184, 790, 214, 802, 214, draw.ACCENT)
    cv.triangle(796, 244, 790, 214, 802, 214, draw.ACCENT)
    cv.triangle(776, 214, 796, 208, 796, 220, draw.ACCENT)
    cv.triangle(816, 214, 796, 208, 796, 220, draw.ACCENT)
    cv.circle(796, 214, 5, draw.ACCENT)
    cv.line(806, 206, 826, 196, draw.INK)
    cv.line(810, 216, 834, 204, draw.INK)
    cv.line(804, 226, 820, 218, draw.INK)

    cv.rect(36, 368, 952, 3, draw.ACCENT)
    body = [
        "POLITBURO MEMBER AND SHANGHAI PARTY CHIEF",
        "CHEN JINING IS UNDER INVESTIGATION FOR",
        "CORRUPTION, THE FOURTH MEMBER OF CHINA'S",
        "TOP BODY TO FALL AS XI'S PURGE WIDENS.",
    ]
    for i, line in enumerate(body):
        font.draw_text(cv, 36, 382 + i * 27, line, draw.INK, scale=3)
    cv.rect(36, 496, 952, 2, draw.INK)

    def panel(x, y, band, headline, body):
        cv.frame(x, y, 464, 144, draw.INK, 2)
        cv.rect(x, y, 464, 22, draw.INK)
        font.draw_text(cv, x + 10, y + 4, band, draw.PAPER, scale=2)
        font.draw_text(cv, x + 14, y + 30, headline, draw.INK, scale=4)
        for i, line in enumerate(body):
            font.draw_text(cv, x + 14, y + 66 + i * 18, line,
                           draw.INK, scale=2)

    def icon_tower(ix, iy):
        cv.rect(ix + 24, iy + 8, 16, 50, draw.INK)
        cv.rect(ix + 19, iy + 2, 26, 6, draw.INK)
        for wx in (ix + 27, ix + 35):
            for wy in (iy + 18, iy + 30, iy + 42):
                cv.rect(wx, wy, 3, 3, draw.PAPER)
        cv.circle(ix + 47, iy + 30, 6, draw.ACCENT)
        for dx, dy in ((12, 0), (-12, 0), (0, 12), (0, -12),
                       (10, 7), (-10, -7)):
            cv.line(ix + 47, iy + 30, ix + 47 + dx,
                    iy + 30 + dy, draw.ACCENT)

    def icon_rocket(ix, iy):
        cv.triangle(ix + 32, iy + 2, ix + 22, iy + 24, ix + 42, iy + 24,
                    draw.INK)
        cv.rect(ix + 22, iy + 24, 20, 24, draw.INK)
        cv.circle(ix + 32, iy + 32, 4, draw.PAPER)
        cv.triangle(ix + 22, iy + 40, ix + 12, iy + 52, ix + 22, iy + 52,
                    draw.INK)
        cv.triangle(ix + 42, iy + 40, ix + 52, iy + 52, ix + 42, iy + 52,
                    draw.INK)
        cv.triangle(ix + 26, iy + 50, ix + 38, iy + 50, ix + 32, iy + 62,
                    draw.ACCENT)

    def icon_storefront(ix, iy):
        cv.rect(ix + 4, iy + 10, 56, 5, draw.INK)
        cv.rect(ix + 6, iy + 17, 52, 9, draw.ACCENT)
        for sx in (ix + 8, ix + 20, ix + 32, ix + 44):
            cv.rect(sx, iy + 17, 3, 9, draw.PAPER)
        cv.frame(ix + 8, iy + 26, 48, 32, draw.INK, 2)
        cv.rect(ix + 27, iy + 38, 10, 20, draw.INK)

    def icon_chip(ix, iy):
        cv.frame(ix + 15, iy + 13, 34, 34, draw.INK, 3)
        cv.rect(ix + 26, iy + 24, 12, 12, draw.ACCENT)
        for px in (ix + 16, ix + 28, ix + 40):
            cv.rect(px, iy + 8, 6, 3, draw.INK)
            cv.rect(px, iy + 53, 6, 3, draw.INK)
        for py in (iy + 20, iy + 32, iy + 44):
            cv.rect(ix + 8, py, 3, 6, draw.INK)
            cv.rect(ix + 53, py, 3, 6, draw.INK)

    panel(36, 510, "MIDDLE EAST / RIYADH", "RIYADH STRUCK", [
        "HOUTHI DRONE HIT THE PIF TOWER,",
        "RIYADH'S TALLEST, FOR THE 2ND",
        "TIME IN A WEEK. 11 PEOPLE HURT",
        "AS CREWS FIXED BLAST DAMAGE.",
    ])
    icon_tower(36 + 386, 510 + 28)

    panel(524, 510, "SPACE / SHENZHOU-24", "ALI IN ORBIT", [
        "SHENZHOU-24 LIFTED OFF FROM",
        "JIUQUAN WITH PAKISTAN'S FIRST",
        "ASTRONAUT, FIRST FOREIGNER TO",
        "BOARD THE TIANGONG STATION.",
    ])
    icon_rocket(524 + 386, 510 + 28)

    panel(36, 666, "AMERICAS / COLOMBIA", "HOSTAGE SIEGE", [
        "GUNMEN HOLD ABOUT 20 PEOPLE",
        "IN A CARTAGENA SUPERMARKET",
        "AFTER A FAILED CASH RAID.",
        "10 FREED; TALKS GO ON.",
    ])
    icon_storefront(36 + 386, 666 + 28)

    panel(524, 666, "BUSINESS / NEW YORK", "HUAWEI GUILTY", [
        "US JURY FINDS CHINA'S TECH",
        "GIANT GUILTY OF STEALING",
        "TRADE SECRETS AND OF BANK",
        "FRAUD OVER ITS IRAN DEALS.",
    ])
    icon_chip(524 + 386, 666 + 28)

    font.draw_text(cv, 36, 822, "THE DAY IN NUMBERS", draw.ACCENT, scale=2)
    cv.rect(36, 842, 952, 1, draw.INK)
    numbers = [
        ("4", "POLITBURO MEN", "DOWN THIS TERM"),
        ("11", "INJURED IN THE", "RIYADH STRIKE"),
        ("20", "HOSTAGES HELD", "IN CARTAGENA"),
        ("80", "STOREYS OF THE", "STRUCK TOWER"),
        ("7,000", "MINE CASUALTIES", "A 5-YEAR HIGH"),
    ]
    for i, (num, cap1, cap2) in enumerate(numbers):
        cx = 36 + i * 190 + 95
        font.draw_text_center(cv, cx, 850, num, draw.INK, scale=5)
        font.draw_text_center(cv, cx, 892, cap1, draw.GREY, scale=2)
        font.draw_text_center(cv, cx, 907, cap2, draw.GREY, scale=2)

    font.draw_text(cv, 36, 933, "IN BRIEF", draw.ACCENT, scale=2)
    cv.rect(36, 949, 952, 1, draw.INK)
    briefs = [
        (36, 0, "KYIV: SHIP STRIKES WERE SELF-DEFENCE"),
        (36, 1, "SENEGAL RESTORED AS AFRICA CHAMPIONS"),
        (36, 2, "TRUMP GIVES GIULIANI FREEDOM MEDAL"),
        (524, 0, "SOLDIER ADMITS SELLING US SECRETS"),
        (524, 1, "TURKISH HELICOPTER CRASH KILLS 5"),
        (524, 2, "GUKESH HOLDS SINDAROV IN TITLE GAME"),
    ]
    for bx, row, text in briefs:
        by = 957 + row * 17
        cv.rect(bx, by + 4, 6, 6, draw.ACCENT)
        font.draw_text(cv, bx + 14, by, text, draw.INK, scale=2)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    draw.save_png(cv, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
