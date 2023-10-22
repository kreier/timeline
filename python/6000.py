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
import pandas as pd
import datetime
import os

# Check execution location, exit if not in /python
if os.getcwd()[-6:] != "python":
    print("This script must be executed inside the python folder.")
    exit()

pdfmetrics.registerFont(TTFont('Aptos', 'aptos.ttf'))
pdfmetrics.registerFont(TTFont('Aptos-bold', 'aptos-bold.ttf'))

# Some general settings
version  = "3.1"
language = "en"
filename = "../timeline/timeline_v" + version + ".pdf"
# filename = "../timeline/timeline_v" + version + "_"+ language + ".pdf"
page_width  = 4*297*mm   # 4x A4 landscape
page_height = 210*mm     #    A4 landscape
border_lr   = 10*mm
border_tb   = 10*mm
pdf_author  = "Matthias Kreier"
pdf_title   = "6000 years human history visualized"
pdf_subject = "Timeline of humankind"
number_persons = 0
number_kings   = 0
number_periods = 0
number_events  = 0

# Create the canvas
c = canvas.Canvas(filename, pagesize=(page_width,page_height))
c.setAuthor(pdf_author)
c.setTitle(pdf_title)
c.setSubject(pdf_subject)

# create drawing area
drawing_width  = page_width - 2 * border_lr
drawing_height = page_height - 2 * border_tb
d = Drawing(drawing_width, drawing_height)
x1 = border_lr
y1 = border_tb
x2 = x1 + drawing_width
y2 = y1 + drawing_height

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

def drawString(text, fontsize, x_string, y_string, position):
    c.setFont("Aptos", fontsize)
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1)
    white_width = stringWidth(text, "Aptos", fontsize)
    if position == "r":
        c.rect(x_string, y_string - 2, white_width, fontsize + 1, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_string, y_string, text)
    elif position == "l":
        c.rect(x_string - white_width, y_string - 2, white_width, fontsize + 1, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        c.drawRightString(x_string, y_string, text)
    elif position == "c":
        c.setFont("Aptos-bold", fontsize)
        c.setFillColorRGB(1, 1, 1)
        c.drawCentredString(x_string, y_string, text)

def create_horizontal_axis(c):
    # axis around drawing area
    c.setLineWidth(0.8)
    c.setStrokeColorCMYK(1.00, 1.00, 0, 0.50) 
    c.line(x1, y1, x1 + drawing_width, y1)
    c.line(x1, y2, x1 + drawing_width, y2)

    # tickmarks and years for 61 centuries
    c.setFont('Aptos', 11)
    for i in range(61):
        # main tickmark
        tick_x = x1 + (75 + 100 * i) * dots_year
        c.setLineWidth(1.0)
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
        # offset_x = stringWidth(year, 'Aptos', 11) * 0.5
        c.drawCentredString(tick_x, y1 - 16, year)
        c.drawCentredString(tick_x, y2 + 8, year)

        # vertical lines for centuries
        c.setLineWidth(0.1)
        c.line(tick_x, y1, tick_x, y2)

        # from 1100 to 600 BCE also every 50 years
        if i > 28 and i < 35:
            c.line(tick_x + 50 * dots_year, y1, tick_x + 50 * dots_year, y2)


    c.drawString(x1, y1 - 16, "BCE")
    c.drawString(x1, y2 + 8 , "BCE")
    # x_shift = stringWidth("CE", 'Aptos', 11)
    c.drawRightString(x2, y1 - 16, "CE")
    c.drawRightString(x2, y2 + 8, "CE")


def create_adam_moses(c):
    global number_persons
    # Start with a blue line for the deluge during this timespan
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 1)
    location_deluge = x1 + (4075 - 2370) * dots_year
    c.line(location_deluge, y1, location_deluge, y2)
    drawString("Deluge 2370 BCE", 12, location_deluge + 2, y2 - 16, "r")

    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data Adam to Solomo")
    persons = pd.read_csv("../db/adam-moses.csv", encoding='utf8')
    c.setFont("Aptos", 12)
    for index, row in persons.iterrows():
        born = int(row.born[0:4])
        died = int(row.died[0:4])
        person = f"{row.person}"
        details_r = f"{born} to {died} BCE - {born - died} years"
        x_box = x1 + (4075 - born) * dots_year
        y_box = y2 - index*21 - 21
        x_boxwidth = (born - died) * dots_year
        x_text = x_box + x_boxwidth * 0.5
        if index < 10:
            c.setFillColorRGB(0, 0, 1)
        else:
            c.setFillColorRGB(0, 0.7, 0)
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.3)
        c.rect(x_box, y_box, x_boxwidth, 19, fill = 1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Aptos-bold", 15)
        c.drawCentredString(x_text, y_box + 5, person)
        drawString(details_r, 12, x_box + x_boxwidth + 2, y_box + 3.5, "r")
        # c.setFillColorRGB(0, 0, 0)
        # c.drawString(x_box + x_boxwidth + 2, y_box + 3.5, details_r)
        if index > 0 and index < 23:
            drawString(f"{father_born - born} years", 10, x_box - 2, y_box + 3.5, "l")
            # c.drawRightString(x_box - 2, y_box + 3.5, f"{father_born - born} years")
        father_born = born
        number_persons += 1

def create_kings(c):
    global number_kings
    # Start with a blue line for the deluge during this timespan
    c.setLineWidth(1)
    c.setStrokeColorRGB(0.8, 0, 0)
    division_kingdom = x1 + (4075 - 997) * dots_year
    c.line(division_kingdom, y1 + drawing_height * 0.5, division_kingdom, y2)
    drawString("Division of the kingdom Israel 997 BCE", 12, division_kingdom - 2, y2 - 14*7, "l")

    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data of kings")
    kings = pd.read_csv("../db/kings.csv", encoding='utf8')
    c.setFont("Aptos", 11)
    c.setLineWidth(0.3)
    for index, row in kings.iterrows():
        # if row.born:
        #     born  = int(row.born[0:4])
        start = int(row.start[0:4])
        end   = int(row.end[0:4])
        row_y = row.row_y
        detail_l = f"{row.king}"
        detail_r = f"{start} - {end} ({start - end} years)"
        x_box = x1 + (4075 - start) * dots_year
        y_box = y2 - row_y*14 - 16
        x_boxwidth = (start - end) * dots_year
        c.setFillColorRGB(row.R, row.G, row.B)
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box, x_boxwidth, 14, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail_r, 12, x_box + x_boxwidth + 2, y_box + 3, "r")
        # c.drawString(x_box + x_boxwidth + 2, y_box + 2 + y_offset, detail_r)
        drawString(detail_l, 12, x_box - 2, y_box + 3, "l")
        # c.drawRightString(x_box - 2, y_box + 2 + y_offset, detail_l)
        number_kings += 1

def create_periods(c):
    global number_periods
    # Import the perios with start and end as pandas dataframe
    print("Import data of periods")
    periods = pd.read_csv("../db/periods.csv", encoding='utf8')
    c.setFont("Aptos", 11)
    c.setLineWidth(0.3)
    for index, row in periods.iterrows():
        start = int(row.start[0:4])
        end   = int(row.end[0:4])
        row_y = row.row_y
        if len(row.text) > 0:
            detail_c = f"{row.text}"
        if len(row.text_l) > 0:
            detail_l = f"{row.text_l}"
        if len(row.text_r) > 0:
            detail_r = f"{row.text_r}"
        x_box = x1 + (4075 - start) * dots_year
        y_box = y2 - row_y*14 - 16
        x_boxwidth = (start - end) * dots_year
        c.setFillColorRGB(row.R, row.G, row.B)
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box, x_boxwidth, 14, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail_c, 12, x_box + x_boxwidth * 0.5, y_box + 3, "c")
        drawString(detail_r, 12, x_box + x_boxwidth + 2, y_box + 3, "r")
        drawString(detail_l, 12, x_box - 2, y_box + 3, "l")
        number_periods += 1

def create_timestamp(c):
    drawString(f"Timeline {version} - created {str(datetime.datetime.now())[0:16]} ", 4, x1, y1 + 20, "r")
    drawString(f"persons",          4, x1 + 6,   y1 + 15.5, "r")
    drawString(str(number_persons), 4, x1 + 5.4, y1 + 15.5, "l")
    drawString(f"kings",            4, x1 + 6,   y1 + 11, "r")
    drawString(str(number_kings),   4, x1 + 5.4, y1 + 11, "l")
    drawString(f"periods",          4, x1 + 6,   y1 + 6.5, "r")
    drawString(str(number_periods), 4, x1 + 5.4, y1 + 6.5, "l")
    # drawString(f"events",           4, x1 + 6,   y1 + 2, "r")
    # drawString(str(number_events),  4, x1 + 5.4, y1 + 2, "l")
    c.setFont("Aptos", 4)
    # c.drawString(x1, y1 + 2, f"Timeline {version} - created {str(datetime.datetime.now())[0:16]} ")
    c.drawString(x1 + 6,        y1 + 2, "events")
    c.drawRightString(x1 + 5.4, y1 + 2, str(number_events))

def render_to_file():
    renderPDF.draw(d, c, border_lr, border_tb)
    c.showPage()
    c.save()
    print(f"File exported: {filename}")

if __name__ == "__main__":
    import_data(text)
    create_horizontal_axis(c)
    create_adam_moses(c)
    create_kings(c)
    create_periods(c)
    create_timestamp(c)
    render_to_file()


# inspiration bin

# canvas.setFillColorCMYK(c, m, y, k) 
# canvas.setStrikeColorCMYK(c, m, y, k) 
# canvas.setFillColorRGB(r, g, b) 
# c.setFillColor(colors.grey)


# Drawing
# d = Drawing(400, 200)
# d.add(Rect(50, 50, 300, 100, fillColor=colors.yellow))
# d.add(String(150,100, "Hello World Brüder việc", fontSize=18, fontName="Aptos", fillColor=colors.red))
# special_characters = "Special characters with German Brüder việc với sứ đồ Phao-lô để."
# d.add(String(180,86, special_characters, fillColor=colors.blue, fontName="Aptos"))