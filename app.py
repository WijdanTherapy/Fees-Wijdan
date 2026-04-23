import streamlit as st
from pdf_generator import generate_fees_pdf

st.set_page_config(
    page_title="Wijdan Therapy – Fee Sheet Generator",
    page_icon="🌿",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #F9F5F0; }

.brand-banner {
  background: linear-gradient(135deg, #3C7850 0%, #2E5E3A 100%);
  border-radius: 14px;
  padding: 28px 32px 22px 32px;
  margin-bottom: 26px;
  border-left: 6px solid #6AAF82;
}
.brand-banner h1 { color: white; font-size: 1.55rem; font-weight: 700; margin: 0 0 4px 0; }
.brand-banner p  { color: #A8D4B8; font-size: 0.88rem; margin: 0; }

.section-card {
  background: white;
  border: 1px solid #C8DDCE;
  border-radius: 10px;
  padding: 20px 24px 16px 24px;
  margin-bottom: 16px;
}
.section-title {
  color: #3C7850; font-size: 0.73rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 14px; padding-bottom: 8px;
  border-bottom: 2px solid #E8F2EC;
}

.stTextInput > div > div > input,
.stTextArea  > div > div > textarea,
.stNumberInput > div > div > input {
  border: 1px solid #C8DDCE !important;
  border-radius: 6px !important;
  background: #FAFCFB !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
  border-color: #3C7850 !important;
  box-shadow: 0 0 0 2px #E8F2EC !important;
}

.preview-box {
  background: #E8F2EC; border-radius: 10px;
  padding: 18px 22px; margin-top: 12px;
  border: 1px solid #C8DDCE;
}
.preview-box h4 { color: #1A2E22; margin: 0 0 10px 0; font-size: 0.95rem; }
.preview-row {
  display: flex; justify-content: space-between;
  padding: 5px 0; border-bottom: 1px solid #C8DDCE;
  font-size: 0.87rem;
}
.preview-row:last-child { border-bottom: none; }
.preview-label { color: #5A6B5E; }
.preview-value { font-weight: 600; color: #3C7850; }
</style>
""", unsafe_allow_html=True)

# ── Banner ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-banner">
  <h1>🌿 Fee Sheet Generator</h1>
  <p>Wijdan Therapy &nbsp;·&nbsp; Fill in the fields below and download a personalised,
     branded PDF fee sheet — ready to share with clients via the center.</p>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
with st.form("fee_form"):

    # ── 1. Practice & Therapist ───────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">🏥 Practice & Therapist</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        practice_name    = st.text_input("Practice Name",        value="Wijdan Therapy")
        therapist_name   = st.text_input("Therapist Name",       value="Yusuf Abdelatti")
        practice_website = st.text_input("Website",              value="wijdantherapy.com")
    with c2:
        practice_tagline = st.text_input("Practice Tagline",     value="Unleash Inner Peace")
        therapist_title  = st.text_input("Therapist Credential", value="Psychotherapist")
        whatsapp         = st.text_input("WhatsApp Number",      value="01004304127")
    intro_text = st.text_area(
        "Intro / Disclaimer",
        value="All fee information is managed through Wijdan Therapy. "
              "Please contact the center to arrange payment or discuss any questions.",
        height=64,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 2. Client Info ────────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">👤 Client (Optional)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        client_name = st.text_input("Client Full Name", value="",
                                    placeholder="e.g. Yahia Ahmed Abdel Shafy")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("If provided, the PDF will show 'Prepared for: [name]' and today's date.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 3. Session Types ──────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">🗂 Session Types (leave price = 0 to hide)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        s1_title = st.text_input("Session 1 – Title", value="Individual Therapy Session")
        s1_line1 = st.text_input("Session 1 – Line 1", value="50-min session  ·  In-person (online on request)")
        s1_line2 = st.text_input("Session 1 – Line 2", value="CBT / ACT / Behavioral Therapy")
        s1_price = st.number_input("Session 1 – Price (EGP)", min_value=0, value=700, step=50)
    with c2:
        s2_title = st.text_input("Session 2 – Title", value="Parent / Family Session")
        s2_line1 = st.text_input("Session 2 – Line 1", value="45-min session  ·  In-person or online")
        s2_line2 = st.text_input("Session 2 – Line 2", value="Guidance, coordination & coaching")
        s2_price = st.number_input("Session 2 – Price (EGP)", min_value=0, value=500, step=50)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 4. Monthly Package ────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📦 Monthly Package (set Discounted Price = 0 to hide entire section)</div>', unsafe_allow_html=True)
    pkg_title = st.text_input("Package Title", value="Monthly Therapy Package")
    c1, c2, c3 = st.columns(3)
    with c1:
        i1_num   = st.text_input("Item 1 – Count", value="4")
        i1_label = st.text_input("Item 1 – Label", value="Individual Sessions")
        i1_note  = st.text_input("Item 1 – Note",  value="Weekly  ·  50 min each")
    with c2:
        i2_num   = st.text_input("Item 2 – Count", value="2")
        i2_label = st.text_input("Item 2 – Label", value="Parent / Family Sessions")
        i2_note  = st.text_input("Item 2 – Note",  value="Biweekly  ·  Online or in-person")
    with c3:
        i3_num   = st.text_input("Item 3 – Count", value="1")
        i3_label = st.text_input("Item 3 – Label", value="School Follow-up Call")
        i3_note  = st.text_input("Item 3 – Note",  value="Monthly  ·  Online  ·  20 min")
    c1, c2 = st.columns(2)
    with c1:
        standard_price   = st.number_input("Standard Monthly Rate (EGP)", min_value=0, value=3800, step=100)
    with c2:
        discounted_price = st.number_input("Discounted Package Price (EGP)", min_value=0, value=3000, step=100)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 5. Payment Methods ────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">💳 Payment Methods</div>', unsafe_allow_html=True)
    st.caption("Pre-filled with Wijdan defaults. Edit or clear any field you don't need.")

    show_instapay = st.checkbox("Include Instapay", value=True)
    if show_instapay:
        c1, c2 = st.columns(2)
        with c1:
            instapay_username = st.text_input("Instapay Username", value="wijdan.psyc")
        with c2:
            instapay_url      = st.text_input("Instapay URL", value="https://ipn.eg/S/wijdan.psyc/instapay/5kp4wT")

    show_vodafone = st.checkbox("Include Vodafone Cash", value=True)
    if show_vodafone:
        vodafone_number = st.text_input("Vodafone Cash Number", value="+201004304127")

    st.markdown("**Payment Instructions** (one per line)")
    pay_instructions_raw = st.text_area(
        "Instructions",
        value=(
            "📸 Please send a screenshot of the payment receipt once completed.\n"
            "💡 Booking is confirmed only after payment is received.\n"
            "⏰ Payment must be completed at least 24 hours before your session."
        ),
        height=100,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 6. Notes ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📝 Notes</div>', unsafe_allow_html=True)
    st.caption("One note per line — shown in the gold box at the bottom.")
    notes_raw = st.text_area(
        "Notes",
        value=(
            "Sessions are held weekly (individual) and biweekly (parent). School follow-up is online.\n"
            "The monthly package is arranged at the start of each month through Wijdan Therapy.\n"
            "Cancellations require 24-hour notice. Late cancellations may incur the standard session fee."
        ),
        height=100,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 7. Footer ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📣 Footer Message</div>', unsafe_allow_html=True)
    footer_cta = st.text_input(
        "Footer right-hand text",
        value="For appointments & fee enquiries, please contact the center directly.",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("⬇️  Generate PDF", use_container_width=True)

# ── Generate ──────────────────────────────────────────────────────────────────
if submitted:
    savings = max(0, standard_price - discounted_price)

    # Build payment methods list
    payment_methods = []
    if show_instapay and instapay_url.strip():
        payment_methods.append({
            "icon": "🔹",
            "label": f"Instapay ({instapay_username})" if instapay_username.strip() else "Instapay",
            "value": instapay_url.strip(),
            "url":   instapay_url.strip(),
            "link_text": f"Pay via Instapay — tap here",
        })
    if show_vodafone and vodafone_number.strip():
        payment_methods.append({
            "icon": "🔹",
            "label": "Vodafone Cash",
            "value": vodafone_number.strip(),
            "url":   "",
        })

    cfg = {
        "practice_name":    practice_name,
        "practice_tagline": practice_tagline,
        "practice_website": practice_website,
        "therapist_name":   therapist_name,
        "therapist_title":  therapist_title,
        "whatsapp":         whatsapp,
        "client_name":      client_name,
        "intro_text":       intro_text,
        "sessions": [
            {"title": s1_title, "line1": s1_line1, "line2": s1_line2, "price": s1_price},
            {"title": s2_title, "line1": s2_line1, "line2": s2_line2, "price": s2_price},
        ],
        "pkg_title":        pkg_title,
        "pkg_items": [
            {"num": i1_num, "label": i1_label, "note": i1_note},
            {"num": i2_num, "label": i2_label, "note": i2_note},
            {"num": i3_num, "label": i3_label, "note": i3_note},
        ],
        "standard_price":   standard_price,
        "discounted_price": discounted_price,
        "savings":          savings,
        "payment_methods":  payment_methods,
        "payment_instructions": [
            l.strip() for l in pay_instructions_raw.splitlines() if l.strip()
        ],
        "notes":   [l.strip() for l in notes_raw.splitlines() if l.strip()],
        "footer_cta": footer_cta,
    }

    pdf_bytes = generate_fees_pdf(cfg)

    # Preview card
    client_display = client_name.strip() or "—"
    st.markdown(f"""
    <div class="preview-box">
      <h4>✅ PDF Ready</h4>
      <div class="preview-row">
        <span class="preview-label">Prepared for</span>
        <span class="preview-value">{client_display}</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">Therapist</span>
        <span class="preview-value">{therapist_name}, {therapist_title}</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">{s1_title}</span>
        <span class="preview-value">{s1_price:,} EGP</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">{s2_title}</span>
        <span class="preview-value">{s2_price:,} EGP</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">Monthly Package</span>
        <span class="preview-value">{discounted_price:,} EGP / month &nbsp;(save {savings:,} EGP)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    fname = f"Wijdan_Fees_{client_name.replace(' ','_') if client_name.strip() else 'Client'}.pdf"
    st.download_button(
        label="⬇️  Download PDF",
        data=pdf_bytes,
        file_name=fname,
        mime="application/pdf",
        use_container_width=True,
    )
