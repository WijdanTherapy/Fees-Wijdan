# 🌿 Wijdan Therapy — Fee Sheet Generator

A Streamlit app that lets you fill in all variables and instantly generate a
professionally branded, printable PDF fee sheet — matching the exact colors,
layout, and structure of the Wijdan Therapy design.

---

## 📸 What it does

- Fill in practice name, therapist info, session types, prices, package details, notes
- Click **Generate & Download PDF**
- Get a pixel-perfect branded PDF — same green palette, card layout, pricing row, save badge, and footer

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/wijdan-fees-generator.git
cd wijdan-fees-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 📁 File Structure

```
wijdan-fees-generator/
├── app.py               # Streamlit UI — all form fields
├── pdf_generator.py     # ReportLab PDF engine — layout & rendering
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🎨 Customising the Brand Colors

All colors are defined at the top of `pdf_generator.py`:

```python
GREEN       = colors.HexColor("#3C7850")   # primary brand green
GREEN_MID   = colors.HexColor("#4E8F64")   # mid green (card 2 accent)
GREEN_LIGHT = colors.HexColor("#6AAF82")   # light green accents
GREEN_PALE  = colors.HexColor("#E8F2EC")   # pale green backgrounds
CREAM       = colors.HexColor("#F9F5F0")   # page background
GOLD        = colors.HexColor("#C8A84A")   # RECOMMENDED badge
```

Change these hex values to instantly re-brand for any other practice.

---

## ☁️ Deploy on Streamlit Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set **Main file** to `app.py`
4. Click **Deploy** — live in ~60 seconds, no server needed

---

## 📋 Variables You Can Configure in the App

| Field | Example |
|---|---|
| Practice Name | Wijdan Therapy |
| Practice Tagline | Unleash Inner Peace |
| Practice Website | wijdantherapy.com |
| Therapist Name | Yusuf Abdelatti |
| Therapist Title | Psychotherapist |
| Intro / Disclaimer | All fees managed through... |
| Session 1 Title | Individual Therapy Session |
| Session 1 Price | 700 EGP |
| Session 2 Title | Parent / Family Session |
| Session 2 Price | 500 EGP |
| Package Title | Monthly Therapy Package |
| Package Item 1–3 | 4× Individual Sessions... |
| Standard Monthly Rate | 3,800 EGP |
| Discounted Package Price | 3,000 EGP |
| Notes (1 per line) | Cancellation policy... |
| Footer CTA | Contact the center directly |

---

## 🛠 Tech Stack

- **[Streamlit](https://streamlit.io)** — UI framework
- **[ReportLab](https://www.reportlab.com)** — PDF generation (no LaTeX needed)

---

## 📄 License

MIT — free to use, adapt, and deploy.
