from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_report(summary, clauses, info, risks, quality_score):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("ClauseCraft AI Report", styles['Title']))

    elements.append(Spacer(1,20))

    elements.append(Paragraph("Contract Summary", styles['Heading2']))

    elements.append(Paragraph(summary, styles['BodyText']))

    elements.append(Spacer(1,20))

    elements.append(Paragraph("Agreement Information", styles['Heading2']))

    info_table = [["Field","Value"]]

    for k,v in info.items():
        info_table.append([k,v])

    elements.append(Table(info_table))

    elements.append(Spacer(1,20))

    elements.append(Paragraph("Clause Analysis", styles['Heading2']))

    clause_table = [["Clause","Status","Risk"]]

    for clause,status in clauses.items():

        state = "Present" if "Present" in status else "Missing"

        clause_table.append([
            clause,
            state,
            risks.get(clause,"Unknown")
        ])

    elements.append(Table(clause_table))

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(f"Agreement Quality Score: {quality_score}/100", styles['Heading2'])
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer