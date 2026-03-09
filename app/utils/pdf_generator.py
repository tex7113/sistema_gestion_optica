from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

env = Environment(loader= FileSystemLoader("app/templates"))

def generar_ticket(data):
    template = env.get_template("ticket.html")

    html_content = template.render(**data)

    pdf = HTML(string=html_content).write_pdf()

    return pdf