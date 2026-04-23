import streamlit as st
import io
from pdf_generator import generate_fees_pdf

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wijdan Therapy – Fee Sheet Generator",
    page_icon="🌿",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background: #F9F5F0; }

  /* Top brand banner */
  .brand-banner {
    background: #3C7850;
    border-radius: 12px;
    padding: 28px 32px 22px 32px;
    margin-bottom: 28px;
    border-left: 6px solid #6AAF82;
  }
  .brand-banner h1 {
    color: white;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0 0 4px 0;
  }
  .brand-banner p {
    color: #A8D4B8;
    font-size: 0.9rem;
    margin: 0;
  }

  /* Section cards */
  .section-card {
    background: white;
    border: 1px solid #C8DDCE;
    border-radius: 10px;
    padding: 22px 24px;
    margin-bottom: 18px;
  }
  .section-title {
    color: #3C7850;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid #E8F2EC;
  }

  /* Streamlit input tweaks */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stNumberInput > div > div > input {
    border: 1px solid #C8DDCE !important;
    border-radius: 6px !important;
    background: #FAFCFB !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus,
  .stNumberInput > div > div > input:focus {
    border-color: #3C7850 !important;
    box-shadow: 0 0 0 2px #E8F2EC !important;
  }

  /* Generate button */
  .stDownloadButton > button {
    background: #3C7850 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100%;
    margin-top: 8px;
  }
  .stDownloadButton > button:hover {
    background: #2E5E3E !important;
  }

  div[data-testid="stForm"] { border: none; padding: 0; }

  /* Preview box */
  .preview-box {
    background: #E8F2EC;
    border-radius: 10px;
    padding: 18px 22px;
    margin-top: 10px;
    border: 1px solid #C8DDCE;
  }
  .preview-box h4 { color: #1A2E22; margin: 0 0 10px 0; font-size: 0.95rem; }
  .preview-row {
    display: flex; justify-content: space-between;
    padding: 5px 0; border-bottom: 1px solid #C8DDCE;
    font-size: 0.88rem; color: #3C7850;
  }
  .preview-row:last-child { border-bottom: none; }
  .preview-label { color: #5A6B5E; }
  .preview-value { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Brand banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-banner">
  <h1>🌿 Fee Sheet Generator</h1>
  <p>Wijdan Therapy &nbsp;·&nbsp; Unleash Inner Peace &nbsp;·&nbsp;
     Fill in the fields below to generate a branded, printable PDF fee sheet.</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FORM
# ═══════════════════════════════════════════════════════════════════════════════
with st.form("fee_form"):

    # ── 1. Practice / Therapist Info ─────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">🏥 Practice & Therapist</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        practice_name = st.text_input("Practice Name", value="Wijdan Therapy")
        therapist_name = st.text_input("Therapist Name", value="Yusuf Abdelatti")
    with col2:
        practice_tagline = st.text_input("Practice Tagline", value="Unleash Inner Peace")
        therapist_title = st.text_input("Therapist Title / Credential", value="Psychotherapist")
    practice_website = st.text_input("Website", value="wijdantherapy.com")
    intro_text = st.text_area(
        "Intro / Disclaimer Text",
        value="All fee information is managed through Wijdan Therapy. "
              "Please contact the center to arrange payment or discuss any questions.",
        height=68,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 2. Session Types ──────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">🗂 Individual Session Types</div>', unsafe_allow_html=True)
    st.caption("Define up to 2 individual session types (shown as side-by-side cards).")

    col1, col2 = st.columns(2)
    with col1:
        s1_title    = st.text_input("Session 1 – Title",    value="Individual Therapy Session")
        s1_line1    = st.text_input("Session 1 – Line 1",   value="50-min session  ·  In-person (online on request)")
        s1_line2    = st.text_input("Session 1 – Line 2",   value="CBT / ACT / Behavioral Therapy")
        s1_price    = st.number_input("Session 1 – Price (EGP)", min_value=0, value=700, step=50)
    with col2:
        s2_title    = st.text_input("Session 2 – Title",    value="Parent / Family Session")
        s2_line1    = st.text_input("Session 2 – Line 1",   value="45-min session  ·  In-person or online")
        s2_line2    = st.text_input("Session 2 – Line 2",   value="Guidance, coordination & coaching")
        s2_price    = st.number_input("Session 2 – Price (EGP)", min_value=0, value=500, step=50)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 3. Monthly Package ────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📦 Monthly Package</div>', unsafe_allow_html=True)

    pkg_title = st.text_input("Package Title", value="Monthly Therapy Package")

    st.caption("Package includes (up to 3 items)")
    col1, col2, col3 = st.columns(3)
    with col1:
        i1_num   = st.text_input("Item 1 – Count", value="4")
        i1_label = st.text_input("Item 1 – Label", value="Individual Sessions")
        i1_note  = st.text_input("Item 1 – Note",  value="Weekly  ·  50 minutes each")
    with col2:
        i2_num   = st.text_input("Item 2 – Count", value="2")
        i2_label = st.text_input("Item 2 – Label", value="Parent / Family Sessions")
        i2_note  = st.text_input("Item 2 – Note",  value="Biweekly  ·  Online or in-person")
    with col3:
        i3_num   = st.text_input("Item 3 – Count", value="1")
        i3_label = st.text_input("Item 3 – Label", value="School Follow-up Call")
        i3_note  = st.text_input("Item 3 – Note",  value="Monthly  ·  Online  ·  20 minutes")

    col1, col2 = st.columns(2)
    with col1:
        standard_price  = st.number_input("Standard Monthly Rate (EGP)", min_value=0, value=3800, step=100)
    with col2:
        discounted_price = st.number_input("Discounted Package Price (EGP)", min_value=0, value=3000, step=100)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── 4. Notes ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📝 Notes (shown at bottom)</div>', unsafe_allow_html=True)
    st.caption("One note per line — up to 4 lines.")
    notes_raw = st.text_area(
        "Notes",
        value=(
            "Sessions are held weekly (individual) and biweekly (parent). School follow-up is online.\n"
            "The monthly package is arranged at the start of each month through Wijdan Therapy.\n"
            "Cancellations require 24-hour notice. Late cancellations may incur the standard session fee."
        ),
        height=110,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 5. Footer CTA ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📣 Footer Call-to-Action</div>', unsafe_allow_html=True)
    footer_cta = st.text_input(
        "Footer right-hand message",
        value="For appointments & fee enquiries, please contact the center directly.",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("⬇️  Generate & Download PDF", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE
# ═══════════════════════════════════════════════════════════════════════════════
if submitted:
    savings = standard_price - discounted_price

    sessions = [
        {"title": s1_title, "line1": s1_line1, "line2": s1_line2, "price": s1_price},
        {"title": s2_title, "line1": s2_line1, "line2": s2_line2, "price": s2_price},
    ]
    pkg_items = [
        {"num": i1_num, "label": i1_label, "note": i1_note},
        {"num": i2_num, "label": i2_label, "note": i2_note},
        {"num": i3_num, "label": i3_label, "note": i3_note},
    ]
    # Filter out empty items
    pkg_items = [i for i in pkg_items if i["label"].strip()]
    notes_list = [n.strip() for n in notes_raw.strip().splitlines() if n.strip()]

    config = {
        "practice_name":    practice_name,
        "practice_tagline": practice_tagline,
        "practice_website": practice_website,
        "therapist_name":   therapist_name,
        "therapist_title":  therapist_title,
        "intro_text":       intro_text,
        "sessions":         sessions,
        "pkg_title":        pkg_title,
        "pkg_items":        pkg_items,
        "standard_price":   standard_price,
        "discounted_price": discounted_price,
        "savings":          savings,
        "notes":            notes_list,
        "footer_cta":       footer_cta,
    }

    pdf_bytes = generate_fees_pdf(config)

    # Live preview summary
    st.markdown(f"""
    <div class="preview-box">
      <h4>✅ PDF Ready — Preview Summary</h4>
      <div class="preview-row">
        <span class="preview-label">Practice</span>
        <span class="preview-value">{practice_name}  ·  {practice_tagline}</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">Therapist</span>
        <span class="preview-value">{therapist_name}, {therapist_title}</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">{s1_title}</span>
        <span class="preview-value">{s1_price:,} EGP / session</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">{s2_title}</span>
        <span class="preview-value">{s2_price:,} EGP / session</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">Monthly Package (standard)</span>
        <span class="preview-value">{standard_price:,} EGP</span>
      </div>
      <div class="preview-row">
        <span class="preview-label">Monthly Package (discounted)</span>
        <span class="preview-value">{discounted_price:,} EGP &nbsp;(save {savings:,} EGP)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇️  Download PDF",
        data=pdf_bytes,
        file_name=f"{practice_name.replace(' ', '_')}_Session_Fees.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
