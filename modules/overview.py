import streamlit as st
import plotly.express as px
import pandas as pd
from modules.translator import get_text

def show_overview(df, lang="en", theme="dark"):

    # Theme settings
    template   = "plotly_dark"   if theme == "dark" else "plotly_white"
    bg_color   = "rgba(0,0,0,0)" if theme == "dark" else "rgba(255,255,255,0.6)"
    accent     = "#E91E8C"       if theme == "dark" else "#C2185B"
    accent2    = "#FF6B35"       if theme == "dark" else "#E64A19"
    accent3    = "#9C27B0"       if theme == "dark" else "#7B1FA2"
    text_color = "#FFFFFF"       if theme == "dark" else "#1A0A2E"
    subtext    = "#9988BB"       if theme == "dark" else "#6A4080"
    card_bg    = "rgba(233,30,140,0.06)"  if theme == "dark" else "rgba(194,24,91,0.05)"
    border     = "rgba(233,30,140,0.2)"   if theme == "dark" else "rgba(194,24,91,0.2)"

    # Chart colors matching logo gradient
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
            📊 {t("dashboard_title")}
        </h1>
        <p style='color:{accent}; font-size:0.78rem; letter-spacing:2px;
                  text-transform:uppercase; margin:4px 0 0 0;'>
            Campaign Overview — All Clients
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("total_clicks"),      f"{df['Clicks'].sum():,}")
    with col2:
        st.metric(t("total_impressions"), f"{df['Impressions'].sum():,}")
    with col3:
        st.metric(t("avg_roi"),           f"{df['ROI'].mean():.2f}x")
    with col4:
        st.metric(t("avg_ctr"),           f"{df['CTR'].mean():.2f}%")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Charts Row 1 ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>{t('platform_comparison')}</p>", unsafe_allow_html=True)
        platform_data = df.groupby('Channel_Used').agg(
            ROI=('ROI','mean'),
            Clicks=('Clicks','sum')
        ).reset_index()

        fig = px.bar(
            platform_data, x='Channel_Used', y='ROI',
            color='Channel_Used',
            color_discrete_sequence=CHART_COLORS,
            template=template,
            text='ROI'
        )
        fig.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
        fig.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            showlegend=False,
            margin=dict(t=20,b=20,l=10,r=10),
            xaxis_title="", yaxis_title="ROI"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>{t('campaign_performance')}</p>", unsafe_allow_html=True)
        goal_data = df.groupby('Campaign_Goal')['ROI'].mean().reset_index()

        fig2 = px.pie(
            goal_data, values='ROI', names='Campaign_Goal',
            color_discrete_sequence=CHART_COLORS,
            template=template,
            hole=0.4
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
        monthly = df.groupby('Month').agg(
            ROI=('ROI','mean'),
            Clicks=('Clicks','sum')
        ).reset_index()

        fig3 = px.line(
            monthly, x='Month', y='ROI',
            markers=True,
            color_discrete_sequence=[accent],
            template=template
        )
        fig3.update_traces(
            line=dict(width=3),
            marker=dict(size=8, color=accent,
                       line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(233,30,140,0.08)'
        )
        fig3.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=20,b=20,l=10,r=10),
            xaxis_title="Month", yaxis_title="Avg ROI"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown(f"<p style='color:{accent}; font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; font-weight:700;'>Top 10 Clients by ROI</p>", unsafe_allow_html=True)
        top_clients = df.groupby('Company')['ROI'].mean()\
                        .sort_values(ascending=True).tail(10).reset_index()

        fig4 = px.bar(
            top_clients, x='ROI', y='Company',
            orientation='h',
            color='ROI',
            color_continuous_scale=['#2D0A1E', '#E91E8C'],
            template=template
        )
        fig4.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=20,b=20,l=10,r=10),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Avg ROI", yaxis_title=""
        )
        st.plotly_chart(fig4, use_container_width=True)
