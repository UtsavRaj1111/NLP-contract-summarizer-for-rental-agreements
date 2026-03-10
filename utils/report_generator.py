from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_report(summary, clauses, info, risks, quality_score):

    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "ClauseCraft AI Report")

    y -= 40

    c.setFont("Helvetica", 12)

    # SUMMARY
    c.drawString(50, y, "Contract Summary:")
    y -= 20

    for line in summary.split("."):
        c.drawString(50, y, line.strip())
        y -= 15

        if y < 100:
            c.showPage()
            y = 750

    y -= 20

    # AGREEMENT INFO
    c.drawString(50, y, "Agreement Information")
    y -= 20

    for k, v in info.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 15

    y -= 20

    # CLAUSES
    c.drawString(50, y, "Clause Analysis")
    y -= 20

    for clause, status in clauses.items():
        risk = risks.get(clause, "Unknown")
        c.drawString(50, y, f"{clause} → {status} | Risk: {risk}")
        y -= 15

    y -= 20

    # QUALITY SCORE
    c.drawString(50, y, f"Agreement Quality Score: {quality_score}/100")

    c.save()

    buffer.seek(0)

    return buffer