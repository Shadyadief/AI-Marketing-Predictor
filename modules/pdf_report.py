from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import io
from datetime import datetime

def generate_pdf(df, client_name, lang="en"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)
    story = []
    styles = getSampleStyleSheet()

    # ── Colors (matching logo) ──
    PINK     = colors.HexColor('#E91E8C')
    ORANGE   = colors.HexColor('#FF6B35')
    PURPLE   = colors.HexColor('#9C27B0')
    LIGHT_ROW = colors.HexColor('#FDF0F8')

    # ── Title Style ──
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=26,
        textColor=PINK,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#9988BB'),
        alignment=TA_CENTER,
        spaceAfter=16
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=PURPLE,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )

    rec_style = ParagraphStyle(
        'Rec',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=0,
        leftIndent=0,
        textColor=colors.HexColor('#1A0A2E')
    )

    # ── Header ──
    story.append(Paragraph("AI-Marketing-Predictor", title_style))
    story.append(Paragraph(
        "AI-Powered Marketing Intelligence | Built by ENG. Shadya Dief",
        subtitle_style
    ))

    # ── Divider line ──
    divider_data = [['']]
    divider = Table(divider_data, colWidths=[6.5*inch])
    divider.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 2, PINK),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 0.2*inch))

    # ── Report Title ──
    title_text = f"Campaign Performance Report — {client_name}" if lang == "en" \
        else f"تقرير أداء الحملات — {client_name}"
    story.append(Paragraph(title_text, section_style))

    date_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
    story.append(Paragraph(date_text, subtitle_style))
    story.append(Spacer(1, 0.25*inch))

    # ── KPIs Table ──
    kpi_title = "Key Performance Indicators" if lang == "en" else "مؤشرات الأداء الرئيسية"
    story.append(Paragraph(kpi_title, section_style))
    story.append(Spacer(1, 0.1*inch))

    kpi_data = [
        ["Metric", "Value"],
        ["Total Clicks",          f"{df['Clicks'].sum():,}"],
        ["Total Impressions",     f"{df['Impressions'].sum():,}"],
        ["Average ROI",           f"{df['ROI'].mean():.2f}x"],
        ["Average CTR",           f"{df['CTR'].mean():.2f}%"],
        ["Avg Acquisition Cost",  f"${df['Acquisition_Cost'].mean():,.2f}"],
        ["Avg Conversion Rate",   f"{df['Conversion_Rate'].mean():.2%}"],
    ]

    table = Table(kpi_data, colWidths=[3.25*inch, 3.25*inch])
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND',    (0, 0), (-1, 0),  PINK),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  12),
        # Data rows
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [colors.white, LIGHT_ROW]),
        ('FONTSIZE',      (0, 1), (-1, -1), 10),
        ('TEXTCOLOR',     (0, 1), (-1, -1), colors.HexColor('#1A0A2E')),
        # All cells
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('GRID',          (0, 0), (-1, -1), 0.5, colors.HexColor('#E0C0D8')),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))

    # ── AI Recommendations ──
    best_platform = df.groupby('Channel_Used')['ROI'].mean().idxmax()
    best_roi      = df.groupby('Channel_Used')['ROI'].mean().max()
    best_goal     = df.groupby('Campaign_Goal')['ROI'].mean().idxmax()
    best_segment  = df.groupby('Customer_Segment')['Conversion_Rate'].mean().idxmax()
    best_month    = df.groupby('Month')['ROI'].mean().idxmax()

    platform_title = "AI Recommendations" if lang == "en" else "توصيات الذكاء الاصطناعي"
    story.append(Paragraph(platform_title, section_style))
    story.append(Spacer(1, 0.1*inch))

    # ✅ إصلاح المشكلة: استخدام Paragraph مع تنسيقات مختلفة لكل سطر
    recommendations = [
        (PINK,   f"🏆  Best Platform: {best_platform}  (ROI: {best_roi:.2f}x)"),
        (ORANGE, f"🎯  Best Campaign Goal: {best_goal}"),
        (PURPLE, f"👥  Best Customer Segment: {best_segment}"),
        (PINK,   f"📅  Best Month for Campaigns: Month {best_month}"),
        (ORANGE, f"📈  Next Month ROI Prediction: {df['ROI'].mean() * 1.05:.2f}x  (+5% expected growth)"),
    ]

    # إنشاء جدول بدون استخدام <font> tag
    rec_table_data = []
    for color, text in recommendations:
        # تحويل اللون من reportlab.lib.colors.Color إلى string سداسي عشري
        color_hex = color.hexval()
        if len(color_hex) == 7:
            color_hex = color_hex[1:]  # إزالة الـ # إذا كان موجوداً
        
        # إنشاء نص مع رمز ● ملون
        formatted_text = f"●  {text}"
        
        # إنشاء Paragraph مع اللون المطلوب
        rec_style_temp = ParagraphStyle(
            f'Rec_{color_hex}',
            parent=rec_style,
            textColor=color,
            fontSize=11,
            leftIndent=12,
            spaceAfter=4
        )
        
        rec_table_data.append([Paragraph(formatted_text, rec_style_temp)])

    rec_table = Table(rec_table_data, colWidths=[6.5*inch])
    rec_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, LIGHT_ROW]),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('GRID',          (0, 0), (-1, -1), 0.3, colors.HexColor('#E0C0D8')),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 0.4*inch))

    # ── Footer ──
    story.append(divider)
    story.append(Spacer(1, 0.1*inch))

    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor('#9988BB'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "AI-Marketing-Predictor  |  Built by <b>ENG. Shadya Dief</b>  |  "
        "linkedin.com/in/shadya-dief-ml  |  github.com/Shadyadief",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()