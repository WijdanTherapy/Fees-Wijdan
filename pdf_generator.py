"""
pdf_generator.py
Generates the branded fee-sheet PDF from a config dict.
Returns raw bytes so Streamlit can serve it as a download.
"""

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm

W, H = A4

# ── Brand palette ─────────────────────────────────────────────────────────────
GREEN       = colors.HexColor("#3C7850")
GREEN_MID   = colors.HexColor("#4E8F64")
GREEN_LIGHT = colors.HexColor("#6AAF82")
GREEN_PALE  = colors.HexColor("#E8F2EC")
GREEN_DARK2 = colors.HexColor("#2E5E3A")
CREAM       = colors.HexColor("#F9F5F0")
DARK        = colors.HexColor("#1A2E22")
GREY        = colors.HexColor("#5A6B5E")
BORDER      = colors.HexColor("#C8DDCE")
GOLD        = colors.HexColor("#C8A84A")
GOLD_BG     = colors.HexColor("#FFF8E7")
GOLD_TEXT   = colors.HexColor("#7A6010")
WHITE       = colors.white

MARGIN    = 1.6 * cm
CONTENT_W = W - 2 * MARGIN


# ── Drawing helpers ───────────────────────────────────────────────────────────
def rr(cv, x, y, w, h, r, fill, stroke=None, sw=0.5):
    cv.saveState()
    cv.setFillColor(fill)
    if stroke:
        cv.setStrokeColor(stroke)
        cv.setLineWidth(sw)
        cv.roundRect(x, y, w, h, r, fill=1, stroke=1)
    else:
        cv.roundRect(x, y, w, h, r, fill=1, stroke=0)
    cv.restoreState()


def txt(cv, s, x, y, font="Helvetica", size=10, color=DARK, anchor="left"):
    cv.saveState()
    cv.setFillColor(color)
    cv.setFont(font, size)
    if   anchor == "center": cv.drawCentredString(x, y, s)
    elif anchor == "right":  cv.drawRightString(x, y, s)
    else:                    cv.drawString(x, y, s)
    cv.restoreState()


def hline(cv, x1, x2, y, color=BORDER, width=0.5):
    cv.saveState()
    cv.setStrokeColor(color)
    cv.setLineWidth(width)
    cv.line(x1, y, x2, y)
    cv.restoreState()


def fmt(n):
    """Format integer with thousands comma."""
    return f"{int(n):,}"


# ── Main generator ────────────────────────────────────────────────────────────
def generate_fees_pdf(cfg: dict) -> bytes:
    buf = io.BytesIO()
    cv  = canvas.Canvas(buf, pagesize=A4)
    cv.setTitle(f"Session Fees – {cfg['practice_name']}")

    # PAGE BACKGROUND
    cv.setFillColor(CREAM)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    # ══════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════
    HEADER_H = 3.4 * cm
    hdr_bot  = H - HEADER_H

    cv.setFillColor(GREEN)
    cv.rect(0, hdr_bot, W, HEADER_H, fill=1, stroke=0)

    cv.setFillColor(GREEN_MID)
    cv.rect(0, hdr_bot, 0.45*cm, HEADER_H, fill=1, stroke=0)

    cv.setFillColor(GREEN_LIGHT)
    cv.rect(0, hdr_bot - 0.05*cm, W, 0.05*cm, fill=1, stroke=0)

    tagline_upper = (
        f"{cfg['practice_name'].upper()}   ·   "
        f"{cfg['practice_tagline'].upper()}"
    )
    txt(cv, tagline_upper,
        0.9*cm, H - 0.85*cm, size=8, color=GREEN_LIGHT)

    txt(cv, "Session Fees & Service Packages",
        0.9*cm, H - 1.85*cm, font="Helvetica-Bold", size=20, color=WHITE)

    subtitle = f"Psychotherapy Services  ·  {cfg['therapist_name']}, {cfg['therapist_title']}"
    txt(cv, subtitle,
        0.9*cm, H - 2.7*cm, size=10, color=GREEN_LIGHT)

    # ══════════════════════════════════════════════════════
    # Cursor starts just below header
    # ══════════════════════════════════════════════════════
    cursor = hdr_bot - 0.8*cm

    # INTRO LINE
    txt(cv, cfg["intro_text"], MARGIN, cursor, size=9, color=GREY)
    cursor -= 0.9*cm

    # ══════════════════════════════════════════════════════
    # SECTION: INDIVIDUAL SESSIONS
    # ══════════════════════════════════════════════════════
    txt(cv, "INDIVIDUAL SESSIONS", MARGIN, cursor,
        font="Helvetica-Bold", size=8.5, color=GREEN)
    hline(cv, MARGIN, MARGIN + 4.8*cm, cursor - 0.14*cm,
          color=GREEN_LIGHT, width=1)
    cursor -= 0.45*cm

    sessions   = cfg["sessions"]
    n_sessions = len(sessions)
    gap        = 0.4*cm
    CARD_H     = 3.0 * cm
    CARD_W     = (CONTENT_W - gap * (n_sessions - 1)) / n_sessions

    accent_colors = [GREEN, GREEN_MID, GREEN_LIGHT]

    for i, sess in enumerate(sessions):
        cx = MARGIN + i * (CARD_W + gap)
        cy = cursor - CARD_H

        rr(cv, cx, cy, CARD_W, CARD_H, 7, WHITE, BORDER, 0.7)

        cv.setFillColor(accent_colors[i % len(accent_colors)])
        cv.roundRect(cx, cy, 0.32*cm, CARD_H, 4, fill=1, stroke=0)

        txt(cv, sess["title"],
            cx + 0.65*cm, cy + CARD_H - 0.65*cm,
            font="Helvetica-Bold", size=11, color=DARK)
        txt(cv, sess["line1"],
            cx + 0.65*cm, cy + CARD_H - 1.15*cm, size=8.5, color=GREY)
        txt(cv, sess["line2"],
            cx + 0.65*cm, cy + CARD_H - 1.5*cm,  size=8.5, color=GREY)

        hline(cv, cx + 0.5*cm, cx + CARD_W - 0.3*cm, cy + 0.9*cm)

        badge_w, badge_h = 3.2*cm, 0.68*cm
        badge_x = cx + (CARD_W - badge_w) / 2
        badge_y = cy + 0.12*cm
        rr(cv, badge_x, badge_y, badge_w, badge_h, 5, GREEN_PALE)
        txt(cv, f"{fmt(sess['price'])} EGP",
            badge_x + badge_w/2, badge_y + 0.17*cm,
            font="Helvetica-Bold", size=14, color=GREEN, anchor="center")

    cursor -= (CARD_H + 0.55*cm)

    # ══════════════════════════════════════════════════════
    # SECTION: MONTHLY PACKAGE
    # ══════════════════════════════════════════════════════
    txt(cv, "MONTHLY PACKAGE", MARGIN, cursor,
        font="Helvetica-Bold", size=8.5, color=GREEN)
    hline(cv, MARGIN, MARGIN + 4.3*cm, cursor - 0.14*cm,
          color=GREEN_LIGHT, width=1)
    cursor -= 0.45*cm

    pkg_items = cfg["pkg_items"]
    N_ITEMS   = len(pkg_items)

    STRIP_H       = 1.15*cm
    ITEM_H        = 0.9*cm
    DIVIDER_GAP   = 0.35*cm
    PRICE_ROW_H   = 1.35*cm
    CARD_PAD_BOT  = 0.25*cm

    PKG_H = (STRIP_H
             + 0.3*cm
             + N_ITEMS * ITEM_H
             + DIVIDER_GAP
             + 0.05*cm
             + PRICE_ROW_H
             + CARD_PAD_BOT)

    pkg_top = cursor
    pkg_bot = pkg_top - PKG_H

    # shadow + card
    rr(cv, MARGIN + 0.08*cm, pkg_bot - 0.08*cm,
       CONTENT_W, PKG_H, 9, colors.HexColor("#D0E4D8"))
    rr(cv, MARGIN, pkg_bot, CONTENT_W, PKG_H, 9, WHITE, BORDER, 0.7)

    # green header stripe
    strip_top = pkg_top
    strip_bot = strip_top - STRIP_H
    cv.setFillColor(GREEN)
    cv.roundRect(MARGIN, strip_bot, CONTENT_W, STRIP_H, 9, fill=1, stroke=0)
    cv.rect(MARGIN, strip_bot, CONTENT_W, STRIP_H / 2, fill=1, stroke=0)

    txt(cv, cfg["pkg_title"],
        MARGIN + 0.8*cm, strip_bot + 0.32*cm,
        font="Helvetica-Bold", size=14, color=WHITE)

    # RECOMMENDED badge
    badge_w2 = 3.2*cm
    badge_x2 = MARGIN + CONTENT_W - badge_w2 - 0.45*cm
    badge_y2 = strip_bot + 0.22*cm
    rr(cv, badge_x2, badge_y2, badge_w2, 0.68*cm, 4, GOLD)
    txt(cv, "RECOMMENDED",
        badge_x2 + badge_w2/2, badge_y2 + 0.19*cm,
        font="Helvetica-Bold", size=8, color=WHITE, anchor="center")

    # INCLUDED ITEMS
    item_y = strip_bot - 0.3*cm
    for item in pkg_items:
        item_y -= ITEM_H
        cx2 = MARGIN + 0.85*cm
        cy2 = item_y + ITEM_H / 2
        cv.setFillColor(GREEN_PALE)
        cv.circle(cx2, cy2, 0.27*cm, fill=1, stroke=0)
        txt(cv, str(item["num"]), cx2, cy2 - 0.09*cm,
            font="Helvetica-Bold", size=10, color=GREEN, anchor="center")
        txt(cv, item["label"],
            MARGIN + 1.38*cm, item_y + ITEM_H * 0.62,
            font="Helvetica-Bold", size=10.5, color=DARK)
        txt(cv, item["note"],
            MARGIN + 1.38*cm, item_y + ITEM_H * 0.18,
            size=9, color=GREY)

    # DIVIDER
    divider_y = item_y - DIVIDER_GAP
    hline(cv, MARGIN + 0.4*cm, MARGIN + CONTENT_W - 0.4*cm,
          divider_y, color=BORDER, width=0.6)

    # PRICING ROW
    price_area_top = divider_y - 0.08*cm
    price_area_bot = pkg_bot + CARD_PAD_BOT
    price_mid      = (price_area_top + price_area_bot) / 2

    # Left: standard rate
    txt(cv, "Standard rate:",
        MARGIN + 0.6*cm, price_mid + 0.25*cm, size=8, color=GREY)
    txt(cv, f"{fmt(cfg['standard_price'])} EGP / month",
        MARGIN + 0.6*cm, price_mid - 0.12*cm,
        font="Helvetica-Bold", size=11, color=GREY)
    hline(cv, MARGIN + 0.6*cm, MARGIN + 5.1*cm,
          price_mid + 0.18*cm, color=GREY, width=1)

    # Right: discounted price box
    dp_h = price_area_top - price_area_bot
    dp_w = 7.0*cm
    dp_x = MARGIN + CONTENT_W - dp_w - 0.4*cm
    dp_y = price_area_bot
    rr(cv, dp_x, dp_y, dp_w, dp_h, 6, GREEN_PALE, GREEN, 0.8)

    txt(cv, "PACKAGE PRICE:",
        dp_x + 0.35*cm, dp_y + dp_h - 0.32*cm,
        font="Helvetica-Bold", size=8, color=GREEN)
    txt(cv, f"{fmt(cfg['discounted_price'])} EGP / month",
        dp_x + 0.35*cm, dp_y + 0.14*cm,
        font="Helvetica-Bold", size=17, color=GREEN)

    # Save badge (inside the box, top-right)
    save_w = 2.0*cm
    save_h = 0.62*cm
    save_x = dp_x + dp_w - save_w - 0.3*cm
    save_y = dp_y + dp_h - save_h - 0.18*cm
    rr(cv, save_x, save_y, save_w, save_h, 4, GREEN_DARK2)
    txt(cv, f"Save {fmt(cfg['savings'])} EGP",
        save_x + save_w/2, save_y + 0.17*cm,
        font="Helvetica-Bold", size=7.5, color=WHITE, anchor="center")

    cursor = pkg_bot - 0.55*cm

    # ══════════════════════════════════════════════════════
    # NOTES BOX
    # ══════════════════════════════════════════════════════
    note_line_h = 0.43*cm
    NOTES_H     = 0.42*cm + len(cfg["notes"]) * note_line_h + 0.3*cm
    notes_top   = cursor
    notes_bot   = notes_top - NOTES_H

    rr(cv, MARGIN, notes_bot, CONTENT_W, NOTES_H, 6, GOLD_BG, GOLD, 0.8)

    txt(cv, "Notes",
        MARGIN + 0.5*cm, notes_top - 0.38*cm,
        font="Helvetica-Bold", size=9, color=GOLD_TEXT)

    ny = notes_top - 0.76*cm
    for note in cfg["notes"]:
        txt(cv, f"\u2022  {note}", MARGIN + 0.5*cm, ny, size=8.5, color=GOLD_TEXT)
        ny -= note_line_h

    # ══════════════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════════════
    FOOTER_H = 1.3*cm
    cv.setFillColor(GREEN)
    cv.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    cv.setFillColor(GREEN_LIGHT)
    cv.rect(0, FOOTER_H, W, 0.04*cm, fill=1, stroke=0)

    txt(cv, cfg["practice_name"],
        MARGIN, 0.78*cm, font="Helvetica-Bold", size=9, color=WHITE)
    txt(cv, f"{cfg['practice_website']}  ·  {cfg['practice_tagline']}",
        MARGIN, 0.42*cm, size=8, color=GREEN_LIGHT)
    txt(cv, cfg["footer_cta"],
        W - MARGIN, 0.58*cm, size=8.5, color=WHITE, anchor="right")

    cv.save()
    buf.seek(0)
    return buf.read()
