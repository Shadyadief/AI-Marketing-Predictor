import streamlit as st
import pandas as pd
import os

# ==============================
# Page Config — أول سطر دايماً
# ==============================
st.set_page_config(
    page_title="AI-Marketing-Predictor | Smart Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Load CSS
# ==============================
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ==============================
# Force Sidebar Always Visible
# ==============================
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    transform: none !important;
    z-index: 99998 !important;
    min-width: 240px !important;
}

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: linear-gradient(135deg, #E91E8C, #9C27B0) !important;
    border-radius: 0 12px 12px 0 !important;
    border: none !important;
    width: 30px !important;
    height: 60px !important;
    position: fixed !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 999999 !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 4px 0 20px rgba(233,30,140,0.6) !important;
    cursor: pointer !important;
}

[data-testid="collapsedControl"] svg {
    fill: white !important;
    color: white !important;
    display: block !important;
    width: 16px !important;
    height: 16px !important;
}

button[kind="header"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Session State
# ==============================
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

lang  = st.session_state['lang']
theme = st.session_state['theme']

# ==============================
# Theme Colors
# ==============================
if theme == 'dark':
    TEXT       = "#FFFFFF"
    SUBTEXT    = "#9988BB"
    BORDER     = "rgba(233,30,140,0.2)"
    ACCENT     = "#E91E8C"
    ACCENT2    = "#FF6B35"
    ACCENT3    = "#9C27B0"
    GLASS_CARD = "rgba(255,255,255,0.04)"
else:
    TEXT       = "#1A0A2E"
    SUBTEXT    = "#6A4080"
    BORDER     = "rgba(233,30,140,0.25)"
    ACCENT     = "#C2185B"
    ACCENT2    = "#E64A19"
    ACCENT3    = "#7B1FA2"
    GLASS_CARD = "rgba(255,255,255,0.55)"

# ==============================
# Dynamic Theme CSS
# ==============================
st.markdown(f"""
<style>
.stApp {{
    background: {"linear-gradient(135deg,#0D0520 0%,#12062A 60%,#0D0520 100%)"
                 if theme == "dark" else
                 "linear-gradient(135deg,#F5EEF8 0%,#EDE0F5 100%)"} !important;
    color: {TEXT} !important;
}}

.block-container {{
    background: {"rgba(18,6,42,0.55)"
                 if theme == "dark" else
                 "rgba(240,232,248,0.55)"} !important;
}}

[data-testid="stSidebar"] {{
    background: {"rgba(10,3,24,0.75)"
                 if theme == "dark" else
                 "rgba(220,200,240,0.65)"} !important;
}}

[data-testid="stMetricValue"] {{
    background: linear-gradient(135deg, {ACCENT2}, {ACCENT});
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}}

[data-testid="stMetricLabel"] {{
    color: {SUBTEXT} !important;
}}

[data-testid="collapsedControl"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT3}) !important;
}}

.stButton > button {{
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT3} 100%) !important;
}}
</style>
""", unsafe_allow_html=True)

# ==============================
# Translations
# ==============================
TRANSLATIONS = {
    "en": {
        "dashboard_title":      "AI-Marketing-Predictor",
        "overview":             "Overview",
        "client_view":          "Client View",
        "ai_insights":          "AI Insights",
        "upload_data":          "Upload Data",
        "total_clicks":         "Total Clicks",
        "total_impressions":    "Total Impressions",
        "avg_roi":              "Average ROI",
        "avg_ctr":              "Average CTR",
        "avg_conversion":       "Conversion Rate",
        "avg_cost":             "Avg Acquisition Cost",
        "best_platform":        "Best Platform",
        "best_campaign":        "Best Campaign Goal",
        "campaign_performance": "Campaign Performance",
        "platform_comparison":  "Platform Comparison",
        "monthly_trend":        "Monthly ROI Trend",
        "ai_recommendation":    "AI Recommendations",
        "prediction":           "Next Month Prediction",
        "generate_report":      "📄 Generate PDF Report",
        "select_client":        "Select Client",
        "upload_csv":           "Upload CSV or Parquet File",
        "dark_mode":            "🌙 Dark",
        "light_mode":           "☀️ Light",
        "theme":                "Theme",
        "language":             "Language",
        "live_stats":           "Live Stats",
        "total_records":        "Total Records",
        "active_clients":       "Active Clients",
        "owner":                "Project Engineer",
        "follow_us":            "Follow Us",
    },
    "ar": {
        "dashboard_title":      "منصة التنبؤ الذكي للتسويق",
        "overview":             "نظرة عامة",
        "client_view":          "عرض العميل",
        "ai_insights":          "توصيات الذكاء الاصطناعي",
        "upload_data":          "رفع بيانات",
        "total_clicks":         "إجمالي النقرات",
        "total_impressions":    "إجمالي المشاهدات",
        "avg_roi":              "متوسط العائد",
        "avg_ctr":              "متوسط النقر",
        "avg_conversion":       "معدل التحويل",
        "avg_cost":             "متوسط تكلفة الاكتساب",
        "best_platform":        "أفضل منصة",
        "best_campaign":        "أفضل هدف حملة",
        "campaign_performance": "أداء الحملات",
        "platform_comparison":  "مقارنة المنصات",
        "monthly_trend":        "الاتجاه الشهري للعائد",
        "ai_recommendation":    "توصيات الذكاء الاصطناعي",
        "prediction":           "توقعات الشهر الجاي",
        "generate_report":      "📄 توليد تقرير PDF",
        "select_client":        "اختر العميل",
        "upload_csv":           "ارفع ملف CSV أو Parquet",
        "dark_mode":            "🌙 داكن",
        "light_mode":           "☀️ فاتح",
        "theme":                "المظهر",
        "language":             "اللغة",
        "live_stats":           "إحصائيات مباشرة",
        "total_records":        "إجمالي السجلات",
        "active_clients":       "العملاء النشطين",
        "owner":                "مهندسة المشروع",
        "follow_us":            "تابعنا",
    }
}

def t(key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_parquet('data/campaigns_clean.parquet')
    if 'CTR' not in df.columns:
        df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)
    if 'Month' not in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
    return df

df = load_data()

# ==============================
# Sidebar
# ==============================
with st.sidebar:

    # ── Logo ──
    if os.path.exists('assets/logo.png'):
        st.image('assets/logo.png', width=155)
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:16px 0;'>
            <span style='font-family:Syne,sans-serif; font-size:1.3rem;
                         font-weight:800;
                         background:linear-gradient(135deg,{ACCENT2},{ACCENT});
                         -webkit-background-clip:text;
                         -webkit-text-fill-color:transparent;'>AI-Marketing</span>
            <span style='font-family:Syne,sans-serif; font-size:0.9rem; color:{SUBTEXT};
                         display:block; letter-spacing:5px;'>PREDICTOR</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Language ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>&#127760; {t('language')}</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("EN", use_container_width=True, key="btn_en"):
            st.session_state['lang'] = 'en'
            st.rerun()
    with c2:
        if st.button("AR", use_container_width=True, key="btn_ar"):
            st.session_state['lang'] = 'ar'
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Theme ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>&#127912; {t('theme')}</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button(t("dark_mode"), use_container_width=True, key="btn_dark"):
            st.session_state['theme'] = 'dark'
            st.rerun()
    with c4:
        if st.button(t("light_mode"), use_container_width=True, key="btn_light"):
            st.session_state['theme'] = 'light'
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 8px 0;'>&#128204; Navigation</p>", unsafe_allow_html=True)

    pages = {
        f"&#128202;  {t('overview')}":    "overview",
        f"&#128100;  {t('client_view')}": "client",
        f"&#129302;  {t('ai_insights')}": "ai",
        f"&#128193;  {t('upload_data')}": "upload",
    }

    page         = st.radio("", list(pages.keys()), label_visibility="collapsed")
    current_page = pages[page]

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Live Stats ──
    st.markdown(f"""
    <div style='background:{GLASS_CARD}; backdrop-filter:blur(12px);
                border:1px solid {BORDER}; border-radius:14px;
                padding:16px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.68rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 10px 0;'>
            &#128225; {t('live_stats')}
        </p>
        <p style='font-size:1.4rem; font-weight:800; font-family:Syne,sans-serif;
                  margin:0; line-height:1;
                  background:linear-gradient(135deg,{ACCENT2},{ACCENT});
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            {df.shape[0]:,}
        </p>
        <p style='color:{SUBTEXT}; font-size:0.70rem; margin:2px 0 12px 0;'>
            {t('total_records')}
        </p>
        <p style='font-size:1.4rem; font-weight:800; font-family:Syne,sans-serif;
                  margin:0; line-height:1;
                  background:linear-gradient(135deg,{ACCENT},{ACCENT3});
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            {df['Company'].nunique()}
        </p>
        <p style='color:{SUBTEXT}; font-size:0.70rem; margin:2px 0 0 0;'>
            {t('active_clients')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Owner Card ──
    st.markdown(f"""
    <div style='background:{GLASS_CARD}; backdrop-filter:blur(12px);
                border:1px solid {BORDER}; border-top:2px solid {ACCENT};
                border-radius:14px; padding:14px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.66rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 6px 0;'>
            &#128100; {t('owner')}
        </p>
        <p style='font-size:0.92rem; font-weight:700;
                  font-family:Syne,sans-serif; margin:0;
                  background:linear-gradient(135deg,{ACCENT2},{ACCENT});
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            ENG. Shadya Dief
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Social Links ──
    st.markdown(f"""
    <div style='background:{GLASS_CARD}; backdrop-filter:blur(12px);
                border:1px solid {BORDER}; border-radius:14px; padding:14px;'>
        <p style='color:{SUBTEXT}; font-size:0.66rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 10px 0;'>
            &#128279; {t('follow_us')}
        </p>
        <a href='https://www.linkedin.com/in/shadya-dief-ml/'
           target='_blank'
           style='display:flex; align-items:center; gap:10px;
                  text-decoration:none; padding:8px 10px;
                  border-radius:10px; margin-bottom:8px;
                  background:rgba(233,30,140,0.06);
                  border:1px solid rgba(233,30,140,0.2);'>
            <span style='font-size:1.2rem;'>&#128101;</span>
            <div>
                <p style='margin:0; font-size:0.80rem; font-weight:700;
                          color:{TEXT};'>Shadya Dief</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>LinkedIn</p>
            </div>
        </a>
        <a href='https://github.com/Shadyadief/AI-Marketing-Predictor/tree/main'
           target='_blank'
           style='display:flex; align-items:center; gap:10px;
                  text-decoration:none; padding:8px 10px;
                  border-radius:10px;
                  background:rgba(156,39,176,0.08);
                  border:1px solid rgba(156,39,176,0.25);'>
            <span style='font-size:1.2rem;'>&#128736;</span>
            <div>
                <p style='margin:0; font-size:0.80rem; font-weight:700;
                          color:{ACCENT3};'>AI-Marketing-Predictor</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>GitHub</p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center; padding:8px 0;'>
        <p style='color:{SUBTEXT}; font-size:0.62rem; margin:0; letter-spacing:1px;'>
            BUILT WITH &#10024; BY SHADYA DIEF
        </p>
        <p style='font-size:0.72rem; font-weight:700;
                  font-family:Syne,sans-serif; margin:3px 0 0 0;
                  background:linear-gradient(135deg,{ACCENT2},{ACCENT},{ACCENT3});
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            AI-Marketing-Predictor
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# Active Data
# ==============================
active_df = st.session_state.get('uploaded_df', df)

# ==============================
# Render Page
# ==============================
from modules.overview    import show_overview
from modules.client_view import show_client_view
from modules.ai_insights import show_ai_insights
from modules.data_upload import show_data_upload

if current_page == "overview":
    show_overview(active_df, lang, theme)
elif current_page == "client":
    show_client_view(active_df, lang, theme)
elif current_page == "ai":
    show_ai_insights(active_df, lang, theme)
elif current_page == "upload":
    show_data_upload(lang, theme)
