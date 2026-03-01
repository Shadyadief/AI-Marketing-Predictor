import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules.translator import get_text
from modules.pdf_report import generate_pdf

def show_client_view(df, lang="en", theme="dark"):

    # ── Theme Settings ──
    template   = "plotly_dark"   if theme == "dark" else "plotly_white"
    bg_color   = "rgba(0,0,0,0)" if theme == "dark" else "rgba(255,255,255,0.6)"
    accent     = "#E91E8C"       if theme == "dark" else "#C2185B"
    accent2    = "#FF6B35"       if theme == "dark" else "#E64A19"
    accent3    = "#9C27B0"       if theme == "dark" else "#7B1FA2"
    text_color = "#FFFFFF"       if theme == "dark" else "#1A0A2E"
    subtext    = "#9988BB"       if theme == "dark" else "#6A4080"
    card_bg    = "rgba(233,30,140,0.06)"  if theme == "dark" else "rgba(194,24,91,0.05)"
    border     = "rgba(233,30,140,0.2)"   if theme == "dark" else "rgba(194,24,91,0.2)"

    CHART_COLORS = ['#E91E8C', '#FF6B35', '#9C27B0', '#FF9800']

    t = lambda key: get_text(key, lang)

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
            👤 {t("client_view")}
        </h1>
        <p style='color:{accent}; font-size:0.78rem; letter-spacing:2px;
                  text-transform:uppercase; margin:4px 0 0 0;'>
            Detailed Client Performance Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Client Selector ──
    clients = sorted(df['Company'].unique().tolist())
    col_sel, col_empty = st.columns([2, 3])
    with col_sel:
        selected = st.selectbox(
            t("select_client"),
            clients,
            key="client_selector"
        )

    client_df = df[df['Company'] == selected].copy()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Client Header ──
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, {card_bg}, rgba(0,0,0,0));
                border:1px solid {border}; border-left:4px solid {accent};
                border-radius:14px; padding:18px 24px; margin-bottom:20px;
                backdrop-filter:blur(10px);'>
        <h2 style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800;
                   color:{text_color}; margin:0;'>📊 {selected}</h2>
        <p style='color:{subtext}; font-size:0.75rem; margin:4px 0 0 0;
                  letter-spacing:1px;'>
            {client_df.shape[0]:,} campaigns &nbsp;|&nbsp;
            {client_df['Channel_Used'].nunique()} platforms &nbsp;|&nbsp;
            {client_df['Campaign_Goal'].nunique()} goals
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(t("total_clicks"),      f"{client_df['Clicks'].sum():,}")
    with col2:
        st.metric(t("total_impressions"), f"{client_df['Impressions'].sum():,}")
    with col3:
        st.metric(t("avg_roi"),           f"{client_df['ROI'].mean():.2f}x")
    with col4:
        st.metric(t("avg_ctr"),           f"{client_df['CTR'].mean():.2f}%")
    with col5:
        st.metric(t("avg_cost"),          f"${client_df['Acquisition_Cost'].mean():,.0f}")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Charts Row 1 ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>{t('platform_comparison')}</p>", unsafe_allow_html=True)

        platform = client_df.groupby('Channel_Used').agg(
            ROI=('ROI','mean'),
            Clicks=('Clicks','sum'),
            Campaigns=('Campaign_ID','count')
        ).reset_index()

        fig1 = px.bar(
            platform, x='Channel_Used', y='ROI',
            color='Channel_Used',
            color_discrete_sequence=CHART_COLORS,
            template=template,
            text='ROI',
            hover_data=['Clicks','Campaigns']
        )
        fig1.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
        fig1.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            showlegend=False,
            margin=dict(t=20,b=20,l=10,r=10),
            xaxis_title="", yaxis_title="Avg ROI"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>{t('campaign_performance')}</p>", unsafe_allow_html=True)

        goal = client_df.groupby('Campaign_Goal')['ROI'].mean().reset_index()

        fig2 = px.pie(
            goal, values='ROI', names='Campaign_Goal',
            color_discrete_sequence=CHART_COLORS,
            template=template,
            hole=0.45
        )
        fig2.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=20,b=20,l=10,r=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Charts Row 2 ──
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>{t('monthly_trend')}</p>", unsafe_allow_html=True)

        monthly = client_df.groupby('Month').agg(
            ROI=('ROI','mean'),
            Clicks=('Clicks','sum'),
            Conversions=('Conversion_Rate','mean')
        ).reset_index()

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=monthly['Month'], y=monthly['ROI'],
            mode='lines+markers',
            name='ROI',
            line=dict(color=accent, width=3),
            marker=dict(size=8, color=accent,
                       line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(233,30,140,0.08)'
        ))
        fig3.update_layout(
            template=template,
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=20,b=20,l=10,r=10),
            xaxis_title="Month",
            yaxis_title="Avg ROI",
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>Conversion Rate by Platform</p>", unsafe_allow_html=True)

        conv = client_df.groupby('Channel_Used')['Conversion_Rate'].mean().reset_index()
        conv['Conversion_Rate'] = (conv['Conversion_Rate'] * 100).round(2)

        fig4 = px.bar(
            conv, x='Channel_Used', y='Conversion_Rate',
            color='Channel_Used',
            color_discrete_sequence=CHART_COLORS,
            template=template,
            text='Conversion_Rate'
        )
        fig4.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig4.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            showlegend=False,
            margin=dict(t=20,b=20,l=10,r=10),
            xaxis_title="", yaxis_title="Conversion Rate %"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ── Best Cards ──
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    best_month    = client_df.groupby('Month')['ROI'].mean().idxmax()
    best_platform = client_df.groupby('Channel_Used')['ROI'].mean().idxmax()
    best_goal     = client_df.groupby('Campaign_Goal')['ROI'].mean().idxmax()
    best_segment  = client_df.groupby('Customer_Segment')['Conversion_Rate'].mean().idxmax()

    col_a, col_b, col_c, col_d = st.columns(4)
    for col, icon, label, value, color in [
        (col_a, "📱", "Best Platform", best_platform,      accent),
        (col_b, "🎯", "Best Goal",     best_goal,          accent2),
        (col_c, "📅", "Best Month",    f"Month {best_month}", accent3),
        (col_d, "👥", "Best Segment",  best_segment,       accent),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:{card_bg}; border:1px solid {border};
                        border-top:3px solid {color};
                        border-radius:12px; padding:16px; text-align:center;'>
                <p style='color:{subtext}; font-size:0.68rem; text-transform:uppercase;
                          letter-spacing:1.5px; margin:0 0 6px 0;'>{label}</p>
                <p style='color:{color}; font-size:1.0rem; font-weight:800;
                          font-family:Syne,sans-serif; margin:0;'>{icon} {value}</p>
            </div>
            """, unsafe_allow_html=True)

    # ── PDF Report ──
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(f"<hr style='border-color:{border};'>", unsafe_allow_html=True)

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button(t("generate_report"), type="primary", use_container_width=True):
            with st.spinner("Generating PDF..."):
                pdf_bytes = generate_pdf(client_df, selected, lang)
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=f"{selected}_AI-Marketing-Predictor_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    with col_info:
        st.markdown(f"""
        <div style='padding:12px 16px; background:{card_bg};
                    border:1px solid {border}; border-radius:10px;'>
            <p style='color:{subtext}; font-size:0.78rem; margin:0;'>
                📄 Generate a professional PDF report with KPIs, AI recommendations,
                and campaign insights for <strong style='color:{accent};'>{selected}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
