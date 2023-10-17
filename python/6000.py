# Create a pdf document that is a timeline for the last 6000 years
# We are using reportlab https://pypi.org/project/reportlab/
# Documentation found on https://docs.reportlab.com/reportlab/userguide/ch1_intro/
# Userguide https://www.reportlab.com/docs/reportlab-userguide.pdf 

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# font_path = os.path.join(os.getcwd(), "calibri.ttf")

pdfmetrics.registerFont(TTFont('Aptos', 'aptos.ttf'))
pdfmetrics.registerFont(TTFont('Aptos-bold', 'aptos-bold.ttf'))

# Some general settings
language = "en"
filename = "p6000_" + language + ".pdf"
page_width  = 297*mm   # 4x A4 landscape
page_height = 210*mm     #    A4 landscape
border_lr   = 10*mm
border_tb   = 10*mm
pdf_author  = "Matthias Kreier"
pdf_title   = "6000 years human history visualized"
pdf_subject = "Timeline of humankind"

# database settings
db_adam_moses = "https://raw.githubusercontent.com/kreier/timeline/main/db/adam-joseph_" + language + ".csv"

# Create the canvas
c = canvas.Canvas(filename, pagesize=(page_width,page_height))
c.setAuthor(pdf_author)
c.setTitle(pdf_title)
c.setSubject(pdf_subject)


# border around drawing area
c.setLineWidth(0.8)
c.setStrokeColorCMYK(1.00, 1.00, 0, 0.50) 
x1 = border_lr
y1 = border_tb
c.rect(x1, y1, page_width - 2*border_lr, page_height - 2*border_tb, stroke=1, fill=0)

# create coordinate system


# canvas.setFillColorCMYK(c, m, y, k) 
# canvas.setStrikeColorCMYK(c, m, y, k) 
# canvas.setFillColorRGB(r, g, b) 
# c.setFillColor(colors.grey)

c.setFont("Aptos-bold", 20)
c.drawString(50, 400, "Timeline of 6000 years humankind")

c.setFillColor(colors.black)
# c.setFont("Helvetica", 11)
c.setFont('Aptos', 11)
c.drawString(50, 360, "In this tutorial, Прискилла активно сотрудничали.")
c.drawString(50, 340, "Brüder việc với sứ đồ Phao-lô đểerent types of files, including PDFs.")
c.drawString(50, 320, "By the end of this tutoriausing Python and the ReportLab library.")

c.setFont("Aptos", 4)
c.drawString(border_lr + 5*mm, border_tb + 5*mm, "document created 2023-10-15")

# Drawing
d = Drawing(400, 200)
d.add(Rect(50, 50, 300, 100, fillColor=colors.yellow))
d.setFont("Aptos", 18)
d.add(String(150,100, "Hello World", fontSize=18, fillColor=colors.red))
special_characters = "Special characters Brüder việc với sứ đồ Phao-lô để"
d.add(String(180,86, special_characters, fillColor=colors.red))

# image_path = os.path.join(os.getcwd(), "python_logo.png")
# c.drawImage(image_path, 50, 400, width=150, height=150)

renderPDF.draw(d, c, 0, 0)
c.showPage()
c.save()
    
print(f"The file {filename} was created.")
