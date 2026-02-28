from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import io
from datetime import datetime

def generate_pdf(df, client_name, lang="en"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Colors
    PRIMARY = colors.HexColor('#00D4FF')
    DARK = colors.HexColor('#0A0A0A')
    PURPLE = colors.HexColor('#7B2FBE')

    # Title Style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Header
    story.append(Paragraph("3M4Media", title_style))
    story.append(Paragraph("Smart Marketing Solutions | Promote Your Dreams ⭐", subtitle_style))
    story.append(Spacer(1, 0.2*inch))

    # Report Title
    report_title = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=PURPLE,
        spaceAfter=10
    )

    title_text = f"Campaign Performance Report — {client_name}" if lang == "en" \
        else f"تقرير أداء الحملات — {client_name}"
    story.append(Paragraph(title_text, report_title))

    date_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
    story.append(Paragraph(date_text, subtitle_style))
    story.append(Spacer(1, 0.3*inch))

    # KPIs Table
    kpi_title = "Key Performance Indicators" if lang == "en" else "مؤشرات الأداء الرئيسية"
    story.append(Paragraph(kpi_title, report_title))
    story.append(Spacer(1, 0.1*inch))

    kpi_data = [
        ["Metric", "Value"],
        ["Total Clicks", f"{df['Clicks'].sum():,}"],
        ["Total Impressions", f"{df['Impressions'].sum():,}"],
        ["Average ROI", f"{df['ROI'].mean():.2f}x"],
        ["Average CTR", f"{df['CTR'].mean():.2f}%"],
        ["Avg Acquisition Cost", f"${df['Acquisition_Cost'].mean():,.2f}"],
        ["Avg Conversion Rate", f"{df['Conversion_Rate'].mean():.2%}"],
    ]

    table = Table(kpi_data, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F8FF')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))

    # Best Platform
    best_platform = df.groupby('Channel_Used')['ROI'].mean().idxmax()
    best_roi = df.groupby('Channel_Used')['ROI'].mean().max()

    platform_title = "AI Recommendations" if lang == "en" else "توصيات الذكاء الاصطناعي"
    story.append(Paragraph(platform_title, report_title))
    story.append(Spacer(1, 0.1*inch))

    rec_style = ParagraphStyle(
        'Rec', parent=styles['Normal'],
        fontSize=11, spaceAfter=8, leftIndent=20
    )

    best_goal = df.groupby('Campaign_Goal')['ROI'].mean().idxmax()
    best_segment = df.groupby('Customer_Segment')['Conversion_Rate'].mean().idxmax()
    best_month = df.groupby('Month')['ROI'].mean().idxmax()

    recommendations = [
        f"✅ Best Platform: {best_platform} (ROI: {best_roi:.2f}x)",
        f"🎯 Best Campaign Goal: {best_goal}",
        f"👥 Best Customer Segment: {best_segment}",
        f"📅 Best Month for Campaigns: Month {best_month}",
        f"📈 Next Month ROI Prediction: {df['ROI'].mean() * 1.05:.2f}x (+5% expected growth)",
    ]

    for rec in recommendations:
        story.append(Paragraph(rec, rec_style))

    story.append(Spacer(1, 0.5*inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=9, textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph("━" * 60, footer_style))
    story.append(Paragraph(
        "3M4Media | Smart Marketing Solutions | www.3m4media.com",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
