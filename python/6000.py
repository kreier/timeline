# Create a pdf document that is a timeline for the last 6000 years
# We are using reportlab https://pypi.org/project/reportlab/
# Documentation found on https://docs.reportlab.com/reportlab/userguide/ch1_intro/

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

import os

filename = "6000.pdf"
# page_width = 3367.56  # 4x A4 landscape
page_width = 841.89
page_height = 595.28  #    A4 landscape

c = canvas.Canvas(filename, pagesize=(page_width,page_height))
c.setAuthor("Matthias Kreier")
c.setTitle("6000 years human history visualized")
c.setSubject("Timeline")

c.drawString(100, 100, "Hello world")

# c.setFillColor(colors.grey)
c.setFont("Helvetica-Bold", 20)
c.drawString(50, 400, "Timeline of 6000 years humankind")

c.setFillColor(colors.black)
c.setFont("Helvetica", 11)
c.drawString(50, 360, "In this tutorial, we will demonstrate how to create PDF files using Python.")
c.drawString(50, 340, "Python is a versatile programming language that can be used to create different types of files, including PDFs.")
c.drawString(50, 320, "By the end of this tutorial, you will be able to generate PDF files using Python and the ReportLab library.")

# image_path = os.path.join(os.getcwd(), "python_logo.png")
# c.drawImage(image_path, 50, 400, width=150, height=150)
c.showPage()
c.save()
    
print(f"The file {filename} was created.")