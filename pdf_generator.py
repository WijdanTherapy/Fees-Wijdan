"""
pdf_generator.py
Generates the branded Wijdan Therapy fee-sheet PDF.
• Dynamic layout — zero-price sessions and empty items are skipped entirely
• Fixed pricing row spacing (label / strikethrough / value on separate lines)
• Client name + issue date personalisation strip
• WhatsApp badge in header
• Payment methods with clickable hyperlinks
"""

import io
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm

W, H = A4

# ── Brand palette ─────────────────────────────────────────────────────────────
GREEN        = colors.HexColor("#3C7850")
GREEN_MID    = colors.HexColor("#4E8F64")
GREEN_LIGHT  = colors.HexColor("#6AAF82")
GREEN_PALE   = colors.HexColor("#E8F2EC")
GREEN_DARK2  = colors.HexColor("#2E5E3A")
CREAM        = colors.HexColor("#F9F5F0")
DARK         = colors.HexColor("#1A2E22")
GREY         = colors.HexColor("#5A6B5E")
BORDER       = colors.HexColor("#C8DDCE")
GOLD         = colors.HexColor("#C8A84A")
GOLD_BG      = colors.HexColor("#FFF8E7")
GOLD_TEXT    = colors.HexColor("#7A6010")
PAY_BG       = colors.HexColor("#F0F7F3")
PAY_BORDER   = colors.HexColor("#A8CDB8")
WA_GREEN     = colors.HexColor("#25D366")
WHITE        = colors.white

MARGIN       = 1.6 * cm
CONTENT_W    = W - 2 * MARGIN
ACCENT_COLS  = [GREEN, GREEN_MID, colors.HexColor("#5FA070")]


# ── Low-level helpers ─────────────────────────────────────────────────────────
def rr(cv, x, y, w, h, r, fill, stroke=None, sw=0.5):
    cv.saveState()
    cv.setFillColor(fill)
    if stroke:
        cv.setStrokeColor(stroke); cv.setLineWidth(sw)
        cv.roundRect(x, y, w, h, r, fill=1, stroke=1)
    else:
        cv.roundRect(x, y, w, h, r, fill=1, stroke=0)
    cv.restoreState()


def txt(cv, s, x, y, font="Helvetica", size=10, color=DARK, anchor="left"):
    cv.saveState()
    cv.setFillColor(color); cv.setFont(font, size)
    if   anchor == "center": cv.drawCentredString(x, y, s)
    elif anchor == "right":  cv.drawRightString(x, y, s)
    else:                    cv.drawString(x, y, s)
    cv.restoreState()


def hline(cv, x1, x2, y, color=BORDER, width=0.5):
    cv.saveState()
    cv.setStrokeColor(color); cv.setLineWidth(width)
    cv.line(x1, y, x2, y)
    cv.restoreState()


def fmt(n):
    return f"{int(n):,}"


def section_label(cv, label, cursor):
    txt(cv, label, MARGIN, cursor, font="Helvetica-Bold", size=8.5, color=GREEN)
    hline(cv, MARGIN, MARGIN + len(label) * 0.55 * cm,
          cursor - 0.14*cm, color=GREEN_LIGHT, width=1)
    return cursor - 0.45*cm


# ═════════════════════════════════════════════════════════════════════════════
def generate_fees_pdf(cfg: dict) -> bytes:

    # ── Filter empty data ─────────────────────────────────────────────────────
    sessions  = [s for s in cfg.get("sessions", [])
                 if s.get("title", "").strip() and s.get("price", 0) > 0]
    pkg_items = [i for i in cfg.get("pkg_items", [])
                 if i.get("label", "").strip()]
    show_pkg  = bool(pkg_items) and cfg.get("discounted_price", 0) > 0
    show_pay  = bool(cfg.get("payment_methods", []))
    notes     = [n for n in cfg.get("notes", []) if n.strip()]

    buf = io.BytesIO()
    cv  = canvas.Canvas(buf, pagesize=A4)
    cv.setTitle(f"Session Fees – {cfg.get('practice_name','')}")

    # ── Page background ───────────────────────────────────────────────────────
    cv.setFillColor(CREAM)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    # ══════════════════════════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════════════════════════
    HDR_H   = 3.6 * cm
    hdr_bot = H - HDR_H

    cv.setFillColor(GREEN)
    cv.rect(0, hdr_bot, W, HDR_H, fill=1, stroke=0)
    cv.setFillColor(GREEN_MID)
    cv.rect(0, hdr_bot, 0.45*cm, HDR_H, fill=1, stroke=0)
    cv.setFillColor(GREEN_LIGHT)
    cv.rect(0, hdr_bot - 0.05*cm, W, 0.05*cm, fill=1, stroke=0)

    txt(cv,
        f"{cfg.get('practice_name','').upper()}   ·   "
        f"{cfg.get('practice_tagline','').upper()}",
        0.9*cm, H - 0.85*cm, size=8, color=GREEN_LIGHT)
    txt(cv, "Session Fees & Service Packages",
        0.9*cm, H - 1.85*cm, font="Helvetica-Bold", size=20, color=WHITE)
    txt(cv, f"Psychotherapy Services  ·  "
            f"{cfg.get('therapist_name','')},"
            f" {cfg.get('therapist_title','')}",
        0.9*cm, H - 2.65*cm, size=10, color=GREEN_LIGHT)

    # WhatsApp badge (top-right inside header)
    wa = cfg.get("whatsapp", "").strip()
    if wa:
        wa_cx = W - MARGIN - 0.35*cm
        wa_ty = H - 1.25*cm
        # circle
        cv.setFillColor(WA_GREEN)
        cv.circle(W - MARGIN - 4.9*cm, wa_ty - 0.08*cm, 0.3*cm, fill=1, stroke=0)
        txt(cv, "✆", W - MARGIN - 4.9*cm, wa_ty - 0.22*cm,
            font="Helvetica-Bold", size=9, color=WHITE, anchor="center")
        txt(cv, f"WhatsApp: {wa}",
            W - MARGIN - 4.4*cm, wa_ty,
            size=9, color=WHITE)
        txt(cv, cfg.get("practice_website", ""),
            W - MARGIN - 4.4*cm, wa_ty - 0.38*cm,
            size=8.5, color=GREEN_LIGHT)

    # ══════════════════════════════════════════════════════════════════════════
    # CLIENT + DATE STRIP
    # ══════════════════════════════════════════════════════════════════════════
    STRIP_H  = 1.0 * cm
    strip_y  = hdr_bot - STRIP_H
    rr(cv, 0, strip_y, W, STRIP_H, 0, GREEN_PALE)
    hline(cv, 0, W, strip_y,   color=BORDER, width=0.5)
    hline(cv, 0, W, hdr_bot,   color=BORDER, width=0.5)

    client = cfg.get("client_name", "").strip()
    if client:
        txt(cv, "Prepared for:", MARGIN, strip_y + 0.64*cm, size=8, color=GREY)
        txt(cv, client, MARGIN + 2.2*cm, strip_y + 0.64*cm,
            font="Helvetica-Bold", size=10, color=DARK)

    txt(cv, f"Issued: {date.today().strftime('%d %B %Y')}",
        W - MARGIN, strip_y + 0.64*cm, size=9, color=GREY, anchor="right")

    # ── Cursor ────────────────────────────────────────────────────────────────
    cursor = strip_y - 0.65*cm

    # Intro
    intro = cfg.get("intro_text", "").strip()
    if intro:
        txt(cv, intro, MARGIN, cursor, size=9, color=GREY)
        cursor -= 0.75*cm

    # ══════════════════════════════════════════════════════════════════════════
    # INDIVIDUAL SESSIONS
    # ══════════════════════════════════════════════════════════════════════════
    if sessions:
        cursor = section_label(cv, "INDIVIDUAL SESSIONS", cursor)

        n   = len(sessions)
        gap = 0.4 * cm
        CW  = (CONTENT_W - gap * (n - 1)) / n
        CH  = 3.1 * cm

        for i, sess in enumerate(sessions):
            cx = MARGIN + i * (CW + gap)
            cy = cursor - CH

            rr(cv, cx, cy, CW, CH, 7, WHITE, BORDER, 0.7)
            cv.setFillColor(ACCENT_COLS[i % len(ACCENT_COLS)])
            cv.roundRect(cx, cy, 0.32*cm, CH, 4, fill=1, stroke=0)

            txt(cv, sess["title"],
                cx + 0.65*cm, cy + CH - 0.62*cm,
                font="Helvetica-Bold", size=11, color=DARK)
            txt(cv, sess.get("line1", ""),
                cx + 0.65*cm, cy + CH - 1.08*cm, size=8.5, color=GREY)
            txt(cv, sess.get("line2", ""),
                cx + 0.65*cm, cy + CH - 1.42*cm, size=8.5, color=GREY)

            hline(cv, cx + 0.5*cm, cx + CW - 0.3*cm, cy + 0.92*cm)

            bw = min(CW - 0.8*cm, 3.4*cm)
            bx = cx + (CW - bw) / 2
            by = cy + 0.14*cm
            rr(cv, bx, by, bw, 0.68*cm, 5, GREEN_PALE)
            txt(cv, f"{fmt(sess['price'])} EGP",
                bx + bw / 2, by + 0.17*cm,
                font="Helvetica-Bold", size=14, color=GREEN, anchor="center")

        cursor -= (CH + 0.55*cm)

    # ══════════════════════════════════════════════════════════════════════════
    # MONTHLY PACKAGE
    # ══════════════════════════════════════════════════════════════════════════
    if show_pkg:
        cursor = section_label(cv, "MONTHLY PACKAGE", cursor)

        PKG_STRIP_H  = 1.15 * cm
        ITEM_H       = 0.94 * cm
        DIV_GAP      = 0.38 * cm
        # Pricing row: label line + value line + padding = ~1.5 cm
        PRICE_ROW_H  = 1.55 * cm
        PAD_BOT      = 0.32 * cm

        PKG_H = (PKG_STRIP_H
                 + 0.35*cm
                 + len(pkg_items) * ITEM_H
                 + DIV_GAP
                 + PRICE_ROW_H
                 + PAD_BOT)

        pkg_top = cursor
        pkg_bot = pkg_top - PKG_H

        # shadow + card
        rr(cv, MARGIN + 0.08*cm, pkg_bot - 0.08*cm,
           CONTENT_W, PKG_H, 9, colors.HexColor("#D0E4D8"))
        rr(cv, MARGIN, pkg_bot, CONTENT_W, PKG_H, 9, WHITE, BORDER, 0.7)

        # green header stripe
        s_bot = pkg_top - PKG_STRIP_H
        cv.setFillColor(GREEN)
        cv.roundRect(MARGIN, s_bot, CONTENT_W, PKG_STRIP_H, 9, fill=1, stroke=0)
        cv.rect(MARGIN, s_bot, CONTENT_W, PKG_STRIP_H / 2, fill=1, stroke=0)

        txt(cv, cfg.get("pkg_title", "Monthly Therapy Package"),
            MARGIN + 0.8*cm, s_bot + 0.33*cm,
            font="Helvetica-Bold", size=14, color=WHITE)

        # RECOMMENDED badge
        rbw = 3.2*cm
        rbx = MARGIN + CONTENT_W - rbw - 0.45*cm
        rby = s_bot + 0.22*cm
        rr(cv, rbx, rby, rbw, 0.68*cm, 4, GOLD)
        txt(cv, "RECOMMENDED", rbx + rbw/2, rby + 0.19*cm,
            font="Helvetica-Bold", size=8, color=WHITE, anchor="center")

        # items
        iy = s_bot - 0.35*cm
        for item in pkg_items:
            iy -= ITEM_H
            cix, ciy = MARGIN + 0.85*cm, iy + ITEM_H / 2
            cv.setFillColor(GREEN_PALE)
            cv.circle(cix, ciy, 0.27*cm, fill=1, stroke=0)
            txt(cv, str(item["num"]), cix, ciy - 0.09*cm,
                font="Helvetica-Bold", size=10, color=GREEN, anchor="center")
            txt(cv, item["label"],
                MARGIN + 1.38*cm, iy + ITEM_H * 0.65,
                font="Helvetica-Bold", size=10.5, color=DARK)
            txt(cv, item["note"],
                MARGIN + 1.38*cm, iy + ITEM_H * 0.18, size=9, color=GREY)

        # divider
        div_y = iy - DIV_GAP
        hline(cv, MARGIN + 0.4*cm, MARGIN + CONTENT_W - 0.4*cm,
              div_y, color=BORDER, width=0.6)

        # ── PRICING ROW ───────────────────────────────────────────────────────
        # Positions within the price_row area (below divider):
        #   lbl_y   = top label ("Standard rate:")
        #   val_y   = value line with strikethrough (~0.42 cm below label)
        # Right side: green box centred in full price-row height
        row_top = div_y - 0.12*cm
        row_bot = pkg_bot + PAD_BOT

        lbl_y = row_top - 0.26*cm          # "Standard rate:" baseline
        val_y = lbl_y   - 0.45*cm          # "3,800 EGP / month" baseline

        txt(cv, "Standard rate:",
            MARGIN + 0.6*cm, lbl_y, size=8.5, color=GREY)
        txt(cv, f"{fmt(cfg['standard_price'])} EGP / month",
            MARGIN + 0.6*cm, val_y,
            font="Helvetica-Bold", size=11.5, color=GREY)
        # strikethrough on value text
        hline(cv, MARGIN + 0.6*cm, MARGIN + 5.5*cm,
              val_y + 0.3*cm, color=GREY, width=1.2)

        # green price box — right side, centred vertically in row
        dp_h  = row_top - row_bot - 0.05*cm
        dp_w  = 7.2 * cm
        dp_x  = MARGIN + CONTENT_W - dp_w - 0.4*cm
        dp_y  = row_bot
        rr(cv, dp_x, dp_y, dp_w, dp_h, 6, GREEN_PALE, GREEN, 0.8)

        txt(cv, "PACKAGE PRICE:",
            dp_x + 0.4*cm, dp_y + dp_h - 0.35*cm,
            font="Helvetica-Bold", size=8.5, color=GREEN)
        txt(cv, f"{fmt(cfg['discounted_price'])} EGP / month",
            dp_x + 0.4*cm, dp_y + 0.18*cm,
            font="Helvetica-Bold", size=17, color=GREEN)

        savings = cfg.get("savings", 0)
        if savings > 0:
            sw2 = 2.15*cm
            sx  = dp_x + dp_w - sw2 - 0.25*cm
            sy  = dp_y + dp_h - 0.7*cm
            rr(cv, sx, sy, sw2, 0.56*cm, 4, GREEN_DARK2)
            txt(cv, f"Save {fmt(savings)} EGP",
                sx + sw2/2, sy + 0.15*cm,
                font="Helvetica-Bold", size=7.5, color=WHITE, anchor="center")

        cursor = pkg_bot - 0.55*cm

    # ══════════════════════════════════════════════════════════════════════════
    # PAYMENT METHODS
    # ══════════════════════════════════════════════════════════════════════════
    if show_pay:
        cursor = section_label(cv, "PAYMENT METHODS", cursor)

        methods      = cfg["payment_methods"]
        instructions = [i for i in cfg.get("payment_instructions", []) if i.strip()]

        LINE_H   = 0.58*cm
        PAD_V    = 0.38*cm
        INSTR_H  = len(instructions) * 0.44*cm + (0.3*cm if instructions else 0)

        PM_H = PAD_V + len(methods) * LINE_H + (0.2*cm if instructions else 0) + INSTR_H + PAD_V
        pm_top = cursor
        pm_bot = pm_top - PM_H

        rr(cv, MARGIN, pm_bot, CONTENT_W, PM_H, 7, PAY_BG, PAY_BORDER, 0.7)

        py = pm_top - PAD_V

        for method in methods:
            icon       = method.get("icon", "•")
            label      = method.get("label", "")
            value      = method.get("value", "")
            url        = method.get("url", "")
            link_text  = method.get("link_text", value)

            # icon glyph
            txt(cv, icon, MARGIN + 0.45*cm, py, size=11, color=GREEN)

            # label in bold
            cv.saveState()
            cv.setFillColor(DARK)
            cv.setFont("Helvetica-Bold", 9.5)
            cv.drawString(MARGIN + 1.1*cm, py, label + ":")
            lbl_w = cv.stringWidth(label + ":", "Helvetica-Bold", 9.5)
            cv.restoreState()

            val_x = MARGIN + 1.1*cm + lbl_w + 4

            if url:
                cv.saveState()
                cv.setFillColor(GREEN)
                cv.setFont("Helvetica", 9.5)
                cv.drawString(val_x, py, link_text)
                tw = cv.stringWidth(link_text, "Helvetica", 9.5)
                cv.setStrokeColor(GREEN)
                cv.setLineWidth(0.5)
                cv.line(val_x, py - 1.5, val_x + tw, py - 1.5)
                cv.linkURL(url, (val_x, py - 3, val_x + tw, py + 9), relative=0)
                cv.restoreStore() if False else None
                cv.restoreState()
            else:
                txt(cv, value, val_x, py, size=9.5, color=GREY)

            py -= LINE_H

        # instructions divider + lines
        if instructions:
            py -= 0.1*cm
            hline(cv, MARGIN + 0.4*cm, MARGIN + CONTENT_W - 0.4*cm,
                  py, color=PAY_BORDER, width=0.5)
            py -= 0.32*cm
            for instr in instructions:
                txt(cv, instr, MARGIN + 0.5*cm, py, size=8.5, color=GOLD_TEXT)
                py -= 0.44*cm

        cursor = pm_bot - 0.5*cm

    # ══════════════════════════════════════════════════════════════════════════
    # NOTES BOX
    # ══════════════════════════════════════════════════════════════════════════
    if notes:
        NLH     = 0.44*cm
        NOTES_H = 0.4*cm + len(notes) * NLH + 0.28*cm
        n_top   = cursor
        n_bot   = n_top - NOTES_H
        rr(cv, MARGIN, n_bot, CONTENT_W, NOTES_H, 6, GOLD_BG, GOLD, 0.8)
        txt(cv, "Notes", MARGIN + 0.5*cm, n_top - 0.34*cm,
            font="Helvetica-Bold", size=9, color=GOLD_TEXT)
        ny = n_top - 0.72*cm
        for note in notes:
            txt(cv, f"\u2022  {note}", MARGIN + 0.5*cm, ny,
                size=8.5, color=GOLD_TEXT)
            ny -= NLH
        cursor = n_bot - 0.3*cm

    # ══════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════════════════════════════════
    cv.setFillColor(GREEN)
    cv.rect(0, 0, W, 1.3*cm, fill=1, stroke=0)
    cv.setFillColor(GREEN_LIGHT)
    cv.rect(0, 1.3*cm, W, 0.04*cm, fill=1, stroke=0)

    txt(cv, cfg.get("practice_name", ""),
        MARGIN, 0.78*cm, font="Helvetica-Bold", size=9, color=WHITE)
    txt(cv, f"{cfg.get('practice_website','')}  ·  {cfg.get('practice_tagline','')}",
        MARGIN, 0.42*cm, size=8, color=GREEN_LIGHT)
    txt(cv, cfg.get("footer_cta", ""),
        W - MARGIN, 0.58*cm, size=8.5, color=WHITE, anchor="right")

    cv.save()
    buf.seek(0)
    return buf.read()
