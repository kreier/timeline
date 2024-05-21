from PyPDF2 import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Create a bytes buffer for the PDF
packet = io.BytesIO()

# Create a canvas object using ReportLab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(100, 750, "Hello, World!")  # Coordinates (100, 750) on the PDF
can.save()

# Move the buffer position to the beginning
packet.seek(0)

# Create a new PDF writer object
pdf_writer = PdfWriter()

# Read the content from the buffer
new_pdf = PdfReader(packet)
pdf_writer.add_page(new_pdf.pages[0])

# Write the output PDF to a file
with open("hello_world.pdf", "wb") as output_pdf:
    pdf_writer.write(output_pdf)

print("PDF created successfully!")
