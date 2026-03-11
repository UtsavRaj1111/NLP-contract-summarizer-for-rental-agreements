from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_report(summary, clauses, info, risks, quality_score):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("ClauseCraft AI – Rental Agreement Analysis Report", styles['Title']))
    elements.append(Spacer(1,20))

    # Summary Section
    elements.append(Paragraph("Contract Summary", styles['Heading2']))
    elements.append(Spacer(1,10))
    elements.append(Paragraph(summary, styles['BodyText']))
    elements.append(Spacer(1,20))

    # Agreement Information
    elements.append(Paragraph("Extracted Agreement Information", styles['Heading2']))
    elements.append(Spacer(1,10))

    info_table = [["Field", "Value"]]

    for k,v in info.items():
        info_table.append([k,v])

    table = Table(info_table, colWidths=[2.5*inch,3.5*inch])
    elements.append(table)
    elements.append(Spacer(1,20))

    # Clause Analysis
    elements.append(Paragraph("Clause Analysis", styles['Heading2']))
    elements.append(Spacer(1,10))

    clause_table = [["Clause","Status","Risk"]]

    for clause,status in clauses.items():

        state = "Present" if "Present" in status else "Missing"

        clause_table.append([
            clause,
            state,
            risks.get(clause,"Unknown")
        ])

    table = Table(clause_table, colWidths=[2*inch,2*inch,2*inch])
    elements.append(table)

    elements.append(Spacer(1,20))

    # Quality Score
    elements.append(Paragraph(f"Agreement Quality Score: {quality_score}/100", styles['Heading2']))

    doc.build(elements)

    buffer.seek(0)

    return buffer