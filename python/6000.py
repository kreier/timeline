# Create a pdf document that is a timeline for the last 6000 years
# We are using reportlab https://pypi.org/project/reportlab/
# Documentation found on https://docs.reportlab.com/reportlab/userguide/ch1_intro/
# Userguide https://www.reportlab.com/docs/reportlab-userguide.pdf 

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.axes import XValueAxis
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import os

pdfmetrics.registerFont(TTFont('Aptos', 'aptos.ttf'))
pdfmetrics.registerFont(TTFont('Aptos-bold', 'aptos-bold.ttf'))

# Some general settings
language = "en"
filename = "p6000_" + language + ".pdf"
page_width  = 4*297*mm   # 4x A4 landscape
page_height = 210*mm     #    A4 landscape
border_lr   = 10*mm
border_tb   = 10*mm
pdf_author  = "Matthias Kreier"
pdf_title   = "6000 years human history visualized"
pdf_subject = "Timeline of humankind"

# Create the canvas
c = canvas.Canvas(filename, pagesize=(page_width,page_height))
c.setAuthor(pdf_author)
c.setTitle(pdf_title)
c.setSubject(pdf_subject)

# create drawing area
drawing_width  = page_width - 2 * border_lr
drawing_height = page_height - 2 * border_tb
d = Drawing(drawing_width, drawing_height) 

# The drawing should span from 4075 BCE to 2075 CE, so we have to calculate
# the length of one year in dots from drawing_with for this 6150 years
dots_year = drawing_width / 6150
text = {}

def import_data(text):
    print("Data imported from local file.")
    # database settings
    db_adam_moses = "https://raw.githubusercontent.com/kreier/timeline/main/db/adam-joseph_" + language + ".csv"
    text = {
        "BCE" : "B.C.E."
    }
    # print(text["BCE"])

def create_horizontal_axis(c):
    # axis around drawing area
    c.setLineWidth(0.8)
    c.setStrokeColorCMYK(1.00, 1.00, 0, 0.50) 
    x1 = border_lr
    y1 = border_tb
    y2 = y1 + drawing_height
    c.line(x1, y1, x1 + drawing_width, y1)
    c.line(x1, y2, x1 + drawing_width, y2)

    # tickmarks and years for 61 centuries
    c.setFont('Aptos', 11)
    for i in range(61):
        # main tickmark
        tick_x = x1 + (75 + 100 * i) * dots_year
        c.line(tick_x, y1, tick_x, y1 - 2*mm)
        c.line(tick_x, y2, tick_x, y2 + 2*mm)

        # smaler ticks left and right
        for l in range (-40, 0, 10):
            tick_s = tick_x + l * dots_year
            c.line(tick_s, y1, tick_s, y1 - 1*mm)
            c.line(tick_s, y2, tick_s, y2 + 1*mm)
        for r in range (10, 60, 10):
            tick_s = tick_x + r * dots_year
            c.line(tick_s, y1, tick_s, y1 - 1*mm)
            c.line(tick_s, y2, tick_s, y2 + 1*mm)

        # label the year
        year = str(abs((100 * i) - 4000))
        offset_x = stringWidth(year, 'Aptos', 11) * 0.5
        c.drawString(tick_x - offset_x, y1 - 16, year)
        c.drawString(tick_x - offset_x, y2 + 8, year)
    c.drawString(x1, y1 - 16, "BCE")
    c.drawString(x1, y2 + 8 , "BCE")

    # c.rect(x1, y1, page_width - 2*border_lr, page_height - 2*border_tb, stroke=1, fill=0)

    # data = [(-4050, 2050)]
    # xAxis = XValueAxis()
    # xAxis.setPosition(0, 0, drawing_width)
    # xAxis.valueMin = -4050
    # xAxis.valueMax = 2050
    # xAxis.valueStep = 100

    # d.add(xAxis)

# canvas.setFillColorCMYK(c, m, y, k) 
# canvas.setStrikeColorCMYK(c, m, y, k) 
# canvas.setFillColorRGB(r, g, b) 
# c.setFillColor(colors.grey)

# c.setFont("Aptos-bold", 20)
# c.drawString(50, 400, "Timeline of 6000 years humankind")

# c.setFillColor(colors.black)
# c.setFont('Aptos', 11)
# c.drawString(50, 360, "In this tutorial, Прискилла активно сотрудничали.")
# c.drawString(50, 340, "Brüder việc với sứ đồ Phao-lô đểerent types of files, including PDFs.")
# c.drawString(50, 320, "By the end of this tutoriausing Python and the ReportLab library.")

# c.setFont("Aptos", 4)
# c.drawString(border_lr + 5*mm, border_tb + 5*mm, "document created 2023-10-15")

# Drawing
# d = Drawing(400, 200)
# d.add(Rect(50, 50, 300, 100, fillColor=colors.yellow))
# d.add(String(150,100, "Hello World Brüder việc", fontSize=18, fontName="Aptos", fillColor=colors.red))
# special_characters = "Special characters with German Brüder việc với sứ đồ Phao-lô để."
# d.add(String(180,86, special_characters, fillColor=colors.blue, fontName="Aptos"))

# image_path = os.path.join(os.getcwd(), "python_logo.png")
# c.drawImage(image_path, 50, 400, width=150, height=150)

def render_to_file():
    renderPDF.draw(d, c, border_lr, border_tb)
    c.showPage()
    c.save()
    print(f"File exported: {filename}")

if __name__ == "__main__":
    import_data(text)
    create_horizontal_axis(c)
    render_to_file()
