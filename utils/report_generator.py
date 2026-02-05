from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filename, clauses_data):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    title = Paragraph("Legal Contract Analysis Report", styles["Title"])
    content.append(title)
    content.append(Spacer(1, 12))

    for i, item in enumerate(clauses_data, 1):
        clause_title = Paragraph(f"Clause {i} - Risk: {item['risk']}", styles["Heading3"])
        clause_text = Paragraph(item["clause"], styles["BodyText"])
        explanation = Paragraph(item["explanation"], styles["Italic"])

        content.extend([clause_title, clause_text, explanation, Spacer(1, 12)])

    doc.build(content)
