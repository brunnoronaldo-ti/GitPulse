#arquivo responsável por gerar o PDF com o gráfico e as informações do usuário
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import io
import matplotlib.pyplot as plt
import tempfile
import os

def generate_language_chart(language_percentages):
    languages = list(language_percentages.keys())
    values = list(language_percentages.values())

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_path = temp_file.name
    temp_file.close()

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=languages, autopct="%1.1f%%", startangle=140)
    plt.title("Distribuição de Linguagens")
    plt.tight_layout()
    plt.savefig(temp_path)
    plt.close()

    return temp_path


def generate_pdf(username, language_percentages):
    chart_path = generate_language_chart(language_percentages)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 2 * cm

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(2 * cm, y, "GitPulse — Relatório de Linguagens")

    pdf.drawImage(
        chart_path,
        2 * cm,
        y - 10 * cm,
        width=12 * cm,
        height=12 * cm,
        preserveAspectRatio=True
    )

    y -= 12 * cm

    pdf.setFont("Helvetica", 12)
    pdf.drawString(2 * cm, y, f"Usuário: {username}")

    y -= 1 * cm
    pdf.drawString(2 * cm, y, "Distribuição de linguagens:")

    y -= 1 * cm
    pdf.setFont("Helvetica", 11)

    for lang, percent in language_percentages.items():
        pdf.drawString(3 * cm, y, f"{lang}: {percent}%")
        y -= 0.7 * cm

        if y < 2 * cm:
            pdf.showPage()
            y = height - 2 * cm
            pdf.setFont("Helvetica", 11)

    pdf.showPage()
    pdf.save()

    os.remove(chart_path)
    buffer.seek(0)

    return buffer
