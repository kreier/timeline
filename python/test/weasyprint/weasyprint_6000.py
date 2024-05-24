# Create a pdf document that is a timeline

print("Let's get started!")

from weasyprint import HTML
HTML('https://weasyprint.org/').write_pdf('./weasyprint-website.pdf')
