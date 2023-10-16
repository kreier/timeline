# Create a pdf document that is a timeline for the last 6000 years
# We are using reportlab https://pypi.org/project/reportlab/
# Documentation found on https://docs.reportlab.com/reportlab/userguide/ch1_intro/
# Userguide https://www.reportlab.com/docs/reportlab-userguide.pdf 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

import os

# Some general settings

filename = "p6000.pdf"
page_width = 4*297*mm   # 4x A4 landscape
# page_width  = 297*mm
page_height = 210*mm    #    A4 landscape
border_lr   = 10*mm
border_tb   = 10*mm
pdf_author  = "Matthias Kreier"
pdf_title   = "6000 years human history visualized"
pdf_subject = "Timeline of humankind"

# database and language settings
language = "en"
db_adam_moses = "adam-moses_"


# Create the canvas

c = canvas.Canvas(filename, pagesize=(page_width,page_height))
c.setAuthor(pdf_author)
c.setTitle(pdf_title)
c.setSubject(pdf_subject)

c.setFont("Helvetica", 4)
c.drawString(border_lr + 5*mm, border_tb + 5*mm, "document created 2023-10-14")

# border around drawing area
x1 = border_lr
x2 = page_width - border_lr
y1 = border_tb
y2 = page_height - border_tb
c.line(x1, y1, x1, y2)
c.line(x2, y1, x2, y2)
c.line(x1, y1, x2, y1)
c.line(x1, y2, x2, y2)

# c.setFillColor(colors.grey)
c.setFont("Helvetica-Bold", 20)
c.drawString(50, 400, "Timeline of 6000 years humankind")

# canvas.setFillColorCMYK(c, m, y, k) 
# canvas.setStrikeColorCMYK(c, m, y, k) 
# canvas.setFillColorRGB(r, g, b) 

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