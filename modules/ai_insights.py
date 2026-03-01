import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle
import joblib
import numpy as np
from modules.translator import get_text

def show_ai_insights(df, lang="en", theme="dark"):

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
            🤖 {t("ai_insights")}
        </h1>
        <p style='color:{accent}; font-size:0.78rem; letter-spacing:2px;
                  text-transform:uppercase; margin:4px 0 0 0;'>
            AI-Powered Recommendations & Predictions
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load Model ──
    model_loaded = False
    try:
        model    = joblib.load('models/campaign_model.pkl')
        with open('models/features.pkl', 'rb') as f:
            features = pickle.load(f)
        with open('models/encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        model_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Model not loaded: {e}")

    # ══════════════════════════════════════
    # SECTION 1 — AI Recommendations
    # ══════════════════════════════════════
    st.markdown(f"""
    <p style='color:{accent}; font-size:0.75rem; text-transform:uppercase;
              letter-spacing:2px; font-weight:700; margin-bottom:12px;'>
        💡 {t("ai_recommendation")}
    </p>
    """, unsafe_allow_html=True)

    best_platform  = df.groupby('Channel_Used')['ROI'].mean().idxmax()
    best_roi_val   = df.groupby('Channel_Used')['ROI'].mean().max()
    best_goal      = df.groupby('Campaign_Goal')['ROI'].mean().idxmax()
    best_month     = df.groupby('Month')['ROI'].mean().idxmax()
    best_segment   = df.groupby('Customer_Segment')['Conversion_Rate'].mean().idxmax()
    worst_platform = df.groupby('Channel_Used')['ROI'].mean().idxmin()

    recs = [
        {
            "icon":  "📱",
            "title": f"Best Platform: {best_platform}",
            "desc":  f"Achieves highest average ROI of {best_roi_val:.2f}x — focus budget here",
            "color": accent
        },
        {
            "icon":  "🎯",
            "title": f"Top Campaign Goal: {best_goal}",
            "desc":  f"This goal consistently delivers above-average ROI across all clients",
            "color": "#51CF66"
        },
        {
            "icon":  "📅",
            "title": f"Best Month to Launch: Month {best_month}",
            "desc":  f"Campaigns launched in month {best_month} show peak performance",
            "color": accent3
        },
        {
            "icon":  "👥",
            "title": f"Top Customer Segment: {best_segment}",
            "desc":  f"Highest conversion rate — prioritize this audience in targeting",
            "color": accent2
        },
        {
            "icon":  "⚠️",
            "title": f"Underperforming: {worst_platform}",
            "desc":  f"Consider reducing budget here and reallocating to {best_platform}",
            "color": "#FFB347"
        },
    ]

    col1, col2 = st.columns(2)
    for i, rec in enumerate(recs):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div style='background:{card_bg}; border:1px solid {border};
                        border-left:4px solid {rec["color"]};
                        border-radius:14px; padding:16px 18px; margin-bottom:12px;
                        backdrop-filter:blur(10px);'>
                <div style='display:flex; align-items:flex-start; gap:12px;'>
                    <span style='font-size:1.4rem; line-height:1.2;'>{rec["icon"]}</span>
                    <div>
                        <p style='color:{text_color}; font-size:0.88rem; font-weight:700;
                                  font-family:Syne,sans-serif; margin:0 0 4px 0;'>
                            {rec["title"]}
                        </p>
                        <p style='color:{subtext}; font-size:0.76rem;
                                  margin:0; line-height:1.5;'>
                            {rec["desc"]}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════
    # SECTION 2 — ROI Trend + Prediction
    # ══════════════════════════════════════
    st.markdown(f"<hr style='border-color:{border}; opacity:0.5;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color:{accent}; font-size:0.75rem; text-transform:uppercase;
              letter-spacing:2px; font-weight:700; margin-bottom:12px;'>
        📈 {t("prediction")}
    </p>
    """, unsafe_allow_html=True)

    monthly = df.groupby('Month')['ROI'].mean().reset_index()

    last_month  = int(monthly['Month'].max())
    last_roi    = float(monthly['ROI'].iloc[-1])
    growth_rate = 0.05

    pred_months = [last_month + 1, last_month + 2, last_month + 3]
    pred_rois   = [
        round(last_roi * (1 + growth_rate),      2),
        round(last_roi * (1 + growth_rate) ** 2, 2),
        round(last_roi * (1 + growth_rate) ** 3, 2),
    ]

    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly['Month'], y=monthly['ROI'],
            mode='lines+markers',
            name='Actual ROI',
            line=dict(color=accent, width=3),
            marker=dict(size=8, color=accent,
                       line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(233,30,140,0.08)'
        ))

        fig.add_trace(go.Scatter(
            x=[last_month] + pred_months,
            y=[last_roi]   + pred_rois,
            mode='lines+markers',
            name='Predicted ROI',
            line=dict(color=accent2, width=3, dash='dot'),
            marker=dict(size=10, color=accent2, symbol='star',
                       line=dict(width=2, color='white'))
        ))

        fig.add_vrect(
            x0=last_month, x1=last_month + 3,
            fillcolor=f"rgba(255,107,53,0.05)",
            line_width=0,
            annotation_text="Predicted",
            annotation_position="top left",
            annotation_font_color=accent2
        )

        fig.update_layout(
            template=template,
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=30, b=20, l=10, r=10),
            xaxis_title="Month",
            yaxis_title="Average ROI",
            legend=dict(
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="right",  x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown(f"""
        <div style='background:{card_bg}; border:1px solid {border};
                    border-radius:14px; padding:18px;'>
            <p style='color:{subtext}; font-size:0.68rem; text-transform:uppercase;
                      letter-spacing:1.5px; margin:0 0 14px 0;'>
                📊 Forecast
            </p>
            {''.join([f"""
            <p style='color:{subtext}; font-size:0.70rem; margin:0 0 4px 0;'>Month {m}</p>
            <p style='color:{accent}; font-size:1.2rem; font-weight:800;
                      font-family:Syne,sans-serif; margin:0 0 12px 0;'>{r}x</p>
            """ for m, r in zip(pred_months, pred_rois)])}
            <div style='background:rgba(233,30,140,0.08);
                        border-radius:8px; padding:10px;'>
                <p style='color:{accent}; font-size:0.70rem;
                          margin:0; text-align:center;'>
                    +5% growth/month
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════
    # SECTION 3 — Feature Importance
    # ══════════════════════════════════════
    if model_loaded:
        st.markdown(f"<hr style='border-color:{border}; opacity:0.5;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='color:{accent}; font-size:0.75rem; text-transform:uppercase;
                  letter-spacing:2px; font-weight:700; margin-bottom:12px;'>
            🔑 Key Success Factors
        </p>
        """, unsafe_allow_html=True)

        importance_df = pd.DataFrame({
            'Feature':    features,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True).tail(10)

        fig2 = px.bar(
            importance_df,
            x='Importance', y='Feature',
            orientation='h',
            color='Importance',
            color_continuous_scale=[[0,'#2D0A1E'],[1,'#E91E8C']],
            template=template,
            text='Importance'
        )
        fig2.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig2.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=20, b=20, l=10, r=60),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Importance Score",
            yaxis_title=""
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ══════════════════════════════════════
    # SECTION 4 — Platform Deep Dive
    # ══════════════════════════════════════
    st.markdown(f"<hr style='border-color:{border}; opacity:0.5;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color:{accent}; font-size:0.75rem; text-transform:uppercase;
              letter-spacing:2px; font-weight:700; margin-bottom:12px;'>
        📱 Platform Deep Dive
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        platform_scatter = df.groupby('Channel_Used').agg(
            ROI=('ROI','mean'),
            CTR=('CTR','mean'),
            Clicks=('Clicks','sum'),
        ).reset_index()

        fig3 = px.scatter(
            platform_scatter,
            x='CTR', y='ROI',
            size='Clicks',
            color='Channel_Used',
            text='Channel_Used',
            color_discrete_sequence=CHART_COLORS,
            template=template,
            title="ROI vs CTR by Platform"
        )
        fig3.update_traces(textposition='top center')
        fig3.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=40, b=20, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        goal_conv = df.groupby('Campaign_Goal').agg(
            Conversion=('Conversion_Rate','mean'),
            ROI=('ROI','mean')
        ).reset_index()
        goal_conv['Conversion'] = (goal_conv['Conversion'] * 100).round(2)

        fig4 = px.bar(
            goal_conv,
            x='Campaign_Goal', y='Conversion',
            color='ROI',
            color_continuous_scale=[[0,'#2D0A1E'],[1,'#E91E8C']],
            template=template,
            text='Conversion',
            title="Conversion Rate by Campaign Goal"
        )
        fig4.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig4.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            margin=dict(t=40, b=20, l=10, r=10),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title="Conversion Rate %"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ══════════════════════════════════════
    # SECTION 5 — Summary Stats
    # ══════════════════════════════════════
    st.markdown(f"<hr style='border-color:{border}; opacity:0.5;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color:{accent}; font-size:0.75rem; text-transform:uppercase;
              letter-spacing:2px; font-weight:700; margin-bottom:16px;'>
        📊 Overall Performance Summary
    </p>
    """, unsafe_allow_html=True)

    stats = [
        ("🏢", "Total Clients",   f"{df['Company'].nunique()}",         accent),
        ("📢", "Total Campaigns", f"{df.shape[0]:,}",                   accent2),
        ("💰", "Avg ROI",         f"{df['ROI'].mean():.2f}x",           accent),
        ("👆", "Avg CTR",         f"{df['CTR'].mean():.2f}%",           accent3),
        ("🎯", "Avg Conversion",  f"{df['Conversion_Rate'].mean():.2%}", accent2),
        ("💸", "Avg Cost",        f"${df['Acquisition_Cost'].mean():,.0f}", accent3),
    ]

    cols = st.columns(6)
    for col, (icon, label, val, color) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style='background:{card_bg}; border:1px solid {border};
                        border-top:3px solid {color};
                        border-radius:12px; padding:14px; text-align:center;
                        backdrop-filter:blur(8px);'>
                <p style='font-size:1.4rem; margin:0 0 4px 0;'>{icon}</p>
                <p style='color:{color}; font-size:1rem; font-weight:800;
                          font-family:Syne,sans-serif; margin:0;'>{val}</p>
                <p style='color:{subtext}; font-size:0.65rem; text-transform:uppercase;
                          letter-spacing:1px; margin:3px 0 0 0;'>{label}</p>
            </div>
            """, unsafe_allow_html=True)
