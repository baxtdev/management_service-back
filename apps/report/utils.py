import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from io import BytesIO


def generate_sales_report(data: dict) -> BytesIO:
    html_string = render_to_string("report_template.html", data)
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_file)
    pdf_file.seek(0)
    return pdf_file
