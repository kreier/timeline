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
version  = "3.2"
language = "en"
filename = "../timeline/timeline_v" + version + ".pdf"
color_scheme = "normal"
# filename = "../timeline/timeline_v" + version + "_"+ language + ".pdf"
page_width  = 4*297*mm   # 4x A4 landscape
page_height = 210*mm     #    A4 landscape
border_lr   = 10*mm
border_tb   = 10*mm
pdf_author  = "Matthias Kreier"
pdf_title   = "6000 years human history visualized"
pdf_subject = "Timeline of humankind"
vertical_lines  = False
number_persons  = 0
number_judges   = 0
number_prophets = 0
number_kings    = 0
number_periods  = 0
number_events   = 0

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
dict  = {}
color = {}

# convert the float dates to year, month and day
def year(date_float):
    year = int(date_float)
    if year < 0:
        year -= 1
    return year

def month(date_float):
    month = int((date_float - int(date_float))*12)
    if date_float < 0:
        month = 13 + month
    return month

def day(date_float):
    month = (date_float - int(date_float))*12
    if date_float < 0:
        month = 13 + month
    day = int((month - int(month))*30) + 1
    return day

def y_value(row_y):
    global y2
    return y2 - 4 - row_y * 12

# Import strings for the respective language for names and comments
def import_dictionary():
    print(f"Import dictionary for names and descritions, language: {language}")
    file_dictionary = "../db/dictionary_" + language + ".tsv"
    key_dict = pd.read_csv(file_dictionary, encoding='utf8', sep = '\t')
    for index, row in key_dict.iterrows():
        dict.update({f"{row.key}" : f"{row.text}"})

# Import colors for all keys
def import_colors():
    global color
    print(f"Import color scheme: {color_scheme}")
    file_colors = "../db/colors_" + color_scheme + ".csv"
    key_colors = pd.read_csv(file_colors, encoding='utf8')
    for index, row in key_colors.iterrows():
        color.update({f"{row.key}" : (row.R, row.G, row.B)})

def drawString(text, fontsize, x_string, y_string, position):
    c.setFont("Aptos", fontsize)
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1)
    white_width = stringWidth(text, "Aptos", fontsize)
    if position == "r":
        c.rect(x_string, y_string - 2, white_width, fontsize, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_string, y_string, text)
    elif position == "l":
        c.rect(x_string - white_width, y_string - 2, white_width, fontsize, fill = 1)
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
        if vertical_lines:
            c.setLineWidth(0.1)
            c.line(tick_x, y1, tick_x, y2)

            # from 1100 to 600 BCE also every 50 years
            if i > 28 and i < 35:
                c.line(tick_x + 50 * dots_year, y1, tick_x + 50 * dots_year, y2)

    c.drawString(x1, y1 - 16, "BCE")
    c.drawString(x1, y2 + 8 , "BCE")
    c.drawRightString(x2, y1 - 16, "CE")
    c.drawRightString(x2, y2 + 8, "CE")

def create_reference_events(s):
    global number_events
    # Blue line for the deluge in 2370 BCE
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 1)
    date_deluge = x1 + (4075 - 2370) * dots_year
    c.line(date_deluge, y1, date_deluge, y2)
    drawString("Deluge 2370 BCE", 12, date_deluge + 2, y2 - 16, "r")

    # Red line for the division fo the kingdom 997 BCE
    c.setStrokeColorRGB(0.8, 0, 0)
    date_division_kingdom = x1 + (4075 - 997) * dots_year
    c.line(date_division_kingdom, y_value(2), date_division_kingdom, y_value(24))
    drawString("Division of the kingdom Israel 997 BCE", 10, date_division_kingdom - 2, y_value(5.5) + 3, "l")

    # Red line for the date of the exodus Nisan 14th, 1513 BCE
    c.setStrokeColorRGB(0.8, 0, 0)
    date_exodus = x1 + (4075 - 1513) * dots_year
    c.line(date_exodus, y_value(-0.4), date_exodus, y_value(6))

    # Red line for the end of the time of the nations October 1914 CE
    c.setStrokeColorRGB(0.8, 0, 0)
    date_1914 = x1 + (4075 + 1914) * dots_year
    c.line(date_1914, y_value(-0.4), date_1914, y_value(25))
    drawString("End of the time of the nations, Gods kingdom starts to rule in heaven 1914 CE", 10, date_1914 - 2, y_value(23.5), "l")

    # destruction Jerusalem 607 BCE
    drawString("Destruction of Jerusalem 607 BCE by Babylon", 10, x1 + (4075 - 607) * dots_year, y_value(26), "r")

    # destruction Samaria 740 BCE
    drawString("Destruction of Samaria 740 BCE by Assyria", 10, x1 + (4075 - 740) * dots_year + 2, y_value(44) + 3, "r")

    number_events += 6


def create_adam_moses(c):
    global number_persons
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data Adam to Moses")
    persons = pd.read_csv("../db/adam-moses.csv", encoding='utf8')
    c.setFont("Aptos", 12)
    for index, row in persons.iterrows():
        born = -year(row.born)
        died = -year(row.died)
        # person = f"{row.person}"
        person = dict[f"{row.key}"]
        details_r = f"{born} to {died} BCE - {born - died} years"
        x_box = x1 + (4075 + row.born) * dots_year
        y_box = y2 - index*21 - 21
        x_boxwidth = (born - died) * dots_year
        x_text = x_box + x_boxwidth * 0.5
        co = color[f"{row.key}"]
        c.setFillColorRGB(co[0], co[1], co[2])
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.3)
        c.rect(x_box, y_box, x_boxwidth, 19, fill = 1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Aptos-bold", 15)
        c.drawCentredString(x_text, y_box + 5, person)
        drawString(details_r, 12, x_box + x_boxwidth + 2, y_box + 6, "r")
        if index > 0 and index < 23:
            drawString(f"{father_born - born} years", 9, x_box - 3, y_box + 11, "l")
        father_born = born
        number_persons += 1

def create_judges(c):
    global number_judges
    print("Import data for judges")
    number_judges += 1

def create_kings(c):
    global number_kings
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data of kings")
    kings = pd.read_csv("../db/kings.csv", encoding='utf8')
    c.setFont("Aptos", 10)
    c.setLineWidth(0.3)
    for index, row in kings.iterrows():
        # if row.born:
        #     born  = int(row.born[0:4])
        start = row.start
        end   = row.end
        row_y = row.row_y
        # detail = f"{row.king} "
        detail = dict[f"{row.key}"] + " "
        time_reigned = "("
        if row.years > 0:
            time_reigned += f"{row.years} year"
            if row.years > 1:
                time_reigned += "s"
        if row.months > 0:
            time_reigned += f"{row.months} month"
            if row.months > 1:
                time_reigned += "s"
        if row.days > 0:
            if row.months > 0:
                time_reigned + " "
            time_reigned += f"{row.days} days"

        detail += f"{-year(start)}-{-year(end)} {time_reigned})"
        if index < 20:
            detail_l = ""
            detail_r = detail
        else:
            detail_l = detail
            detail_r = ""
        x_box = x1 + (4075 + start) * dots_year
        y_box = y2 - row_y*12 - 16
        x_boxwidth = (end -  start) * dots_year
        # c.setFillColorRGB(row.R, row.G, row.B)
        # c.setFillColorRGB(1,0,.3)
        co = color[f"{row.key}"]
        c.setFillColorRGB(co[0], co[1], co[2])

        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box, x_boxwidth, 12, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail_r, 10, x_box + x_boxwidth + 2, y_box + 3, "r")
        drawString(detail_l, 10, x_box - 2, y_box + 3, "l")
        number_kings += 1

def create_prophets(c):
    global number_prophets
    print("Import data of prophets")
    number_prophets += 3

def create_periods(c):
    global number_periods
    # Import the perios with start and end as pandas dataframe
    print("Import data of periods")
    periods = pd.read_csv("../db/periods.csv", encoding='utf8')
    c.setFont("Aptos", 10)
    c.setLineWidth(0.3)
    for index, row in periods.iterrows():
        start = row.start
        end   = row.end
        if len(row.text) > 0:
            detail_c = f"{row.text}"
        if len(row.text_l) > 0:
            detail_l = f"{row.text_l}"
        if len(row.text_r) > 0:
            detail_r = f"{row.text_r}"
        x_box = x1 + (4075 + start) * dots_year
        y_box = y_value(row.row_y)
        x_boxwidth = (end - start) * dots_year
        c.setFillColorRGB(row.R, row.G, row.B)
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box, x_boxwidth, 12, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail_c, 10, x_box + x_boxwidth * 0.5, y_box + 3, "c")
        drawString(detail_r, 10, x_box + x_boxwidth + 2, y_box + 3, "r")
        drawString(detail_l, 10, x_box - 2, y_box + 3, "l")
        number_periods += 1





def create_timestamp(c):
    drawString(f"persons",           4, x1 + 6,   y1 + 29.0, "r")
    drawString(str(number_persons),  4, x1 + 5.4, y1 + 29.0, "l")
    drawString(f"judges",            4, x1 + 6,   y1 + 24.5, "r")
    drawString(str(number_judges),   4, x1 + 5.4, y1 + 24.5, "l")
    drawString(f"prophets",          4, x1 + 6,   y1 + 20.0, "r")
    drawString(str(number_prophets), 4, x1 + 5.4, y1 + 20.0, "l")
    drawString(f"kings",             4, x1 + 6,   y1 + 15.5, "r")
    drawString(str(number_kings),    4, x1 + 5.4, y1 + 15.5, "l")
    drawString(f"periods",           4, x1 + 6,   y1 + 11.0, "r")
    drawString(str(number_periods),  4, x1 + 5.4, y1 + 11.0, "l")
    drawString(f"events",            4, x1 + 6,   y1 +  6.5, "r")
    drawString(str(number_events),   4, x1 + 5.4, y1 +  6.5, "l")
    c.setFont("Aptos", 4)
    c.drawString(x1, y1 + 2, f"Timeline {version} - created {str(datetime.datetime.now())[0:16]}")

def render_to_file():
    renderPDF.draw(d, c, border_lr, border_tb)
    c.showPage()
    c.save()
    print(f"File exported: {filename}")

if __name__ == "__main__":
    import_dictionary()
    import_colors()
    create_horizontal_axis(c)
    create_reference_events(c)
    create_adam_moses(c)
    create_judges(c)
    create_kings(c)
    create_prophets(c)
    create_periods(c)
    create_timestamp(c)
    render_to_file()
