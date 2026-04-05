from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import datetime

def generate_report(summary, clauses, info, risks, quality_score):
    """
    Generates a premium, branded PDF report for legal analysis.
    Styled with the ClauseCraft AI Emerald-and-Slate brand system.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Designer Styles
    title_style = ParagraphStyle(
        'CC_Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor("#10B981"),
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CC_Heading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=20,
        spaceAfter=15,
        borderPadding=5,
        borderWidth=0,
        leftIndent=0
    )

    metric_style = ParagraphStyle(
        'CC_Metric',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#64748B"),
        leading=14
    )

    elements = []

    # 1. Branded Header
    elements.append(Paragraph("ClauseCraft AI Intelligence", title_style))
    elements.append(Paragraph(f"Analysis Report Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", metric_style))
    elements.append(Spacer(1, 20))

    # 2. Executive Summary Block
    elements.append(Paragraph("I. EXECUTIVE SEMANTIC SUMMARY", heading_style))
    elements.append(Paragraph(summary, styles['BodyText']))
    elements.append(Spacer(1, 20))

    # 3. Agreement Information (Key Metadata)
    elements.append(Paragraph("II. EXTRACTED METADATA", heading_style))
    
    info_data = [["Entity Field", "Extracted Value"]]
    for k, v in info.items():
        info_data.append([str(k).upper(), str(v)])

    t_info = Table(info_data, colWidths=[2*inch, 4*inch])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFBFE")])
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 25))

    # 4. Risk Assessment
    elements.append(Paragraph("III. LEGAL EXPOSURE & RISK LOG", heading_style))
    
    risk_data = [["Exposure Type", "Observation", "Severity"]]
    # Note: risks is usually detailed_risks list of dicts
    if isinstance(risks, list):
        for r in risks:
            level = r.get('level', 'Low')
            risk_data.append([r.get('type'), Paragraph(r.get('explanation'), styles['BodyText']), level])
    
    t_risks = Table(risk_data, colWidths=[1.5*inch, 3.5*inch, 1*inch])
    t_risks.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 10)
    ]))
    elements.append(t_risks)
    elements.append(Spacer(1, 30))

    # 5. Final Quality Score
    elements.append(Paragraph(f"FINAL AUDIT SCORE: {quality_score}/100", heading_style))
    elements.append(Paragraph("Disclaimer: This report is AI-generated for informational purposes only. Consult with legal professionals for binding advice.", metric_style))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer