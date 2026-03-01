import streamlit as st
import pandas as pd
from modules.translator import get_text

def show_data_upload(lang="en", theme="dark"):
    t = lambda key: get_text(key, lang)

    accent  = "#E91E8C" if theme == "dark" else "#C2185B"
    accent2 = "#FF6B35" if theme == "dark" else "#E64A19"
    accent3 = "#9C27B0" if theme == "dark" else "#7B1FA2"
    subtext = "#9988BB" if theme == "dark" else "#6A4080"
    border  = "rgba(233,30,140,0.2)"  if theme == "dark" else "rgba(194,24,91,0.2)"
    card_bg = "rgba(233,30,140,0.06)" if theme == "dark" else "rgba(194,24,91,0.05)"
    text_color = "#FFFFFF" if theme == "dark" else "#1A0A2E"

    # ── Mobile CSS ──
    st.markdown("""
    <style>
    @media screen and (max-width: 768px) {
        [data-testid="stFileUploader"] {
            padding: 16px 12px !important;
        }
        [data-testid="stFileUploader"] > div {
            font-size: 0.82rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Page Banner ──
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, rgba(233,30,140,0.08), rgba(156,39,176,0.06));
                border:1px solid {border};
                border-radius:16px; padding:22px 28px; margin-bottom:24px;
                backdrop-filter:blur(12px);'>
        <h1 style='font-family:Syne,sans-serif; font-size:1.8rem; font-weight:800;
                   background:linear-gradient(135deg, {accent2}, {accent}, {accent3});
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   background-clip:text; margin:0;'>
            📁 {t('upload_data')}
        </h1>
        <p style='color:{accent}; font-size:0.78rem; letter-spacing:2px;
                  text-transform:uppercase; margin:4px 0 0 0;'>
            Import New Client Data
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{card_bg}; border:1px solid {border};
                border-radius:12px; padding:14px 18px; margin-bottom:20px;'>
        <p style='color:{subtext}; font-size:0.82rem; margin:0;'>
            📌 ارفع ملف CSV لعميل جديد وهيظهر في الداشبورد فوراً
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        t("upload_csv"),
        type=['csv', 'parquet']
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_parquet(uploaded_file)

            required_cols = ['Clicks', 'Impressions', 'ROI',
                             'Channel_Used', 'Campaign_Goal', 'Company']
            missing = [c for c in required_cols if c not in df.columns]

            if missing:
                st.error(f"❌ أعمدة ناقصة: {missing}")
            else:
                if 'CTR' not in df.columns:
                    df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                    df['Month'] = df['Date'].dt.month

                st.markdown(f"""
                <div style='background:rgba(233,30,140,0.08); border:1px solid {border};
                            border-radius:10px; padding:12px 16px; margin-bottom:12px;'>
                    <p style='color:{accent}; font-size:0.88rem; font-weight:700; margin:0;'>
                        ✅ الملف اتحمل! &nbsp; <span style='color:{subtext}'>{df.shape[0]:,} صف</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.dataframe(df.head(), use_container_width=True)
                st.session_state['uploaded_df']   = df
                st.session_state['uploaded_name'] = uploaded_file.name

        except Exception as e:
            st.error(f"❌ Error: {e}")
