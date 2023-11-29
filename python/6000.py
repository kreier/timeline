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
from reportlab.pdfbase.pdfmetrics import stringWidth
import pandas as pd
import datetime
import os

# Check execution location, exit if not in /timeline/python
if os.getcwd()[-6:] != "python":
    print("This script must be executed inside the python folder.")
    exit()

pdfmetrics.registerFont(TTFont('Aptos', 'aptos.ttf'))
pdfmetrics.registerFont(TTFont('Aptos-bold', 'aptos-bold.ttf'))

# Some general settings
version  = "3.6"
language = "en"
color_scheme = "normal"
page_width  = 4*293*mm   # 4x A4 landscape
page_height = 204*mm     #    A4 landscape - 2x border_tb
border_lr   = 2*mm
border_tb   = 7*mm
pdf_author  = "https://github.com/kreier/timeline"
vertical_lines  = False

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

def x_position(date_float):
    global x1
    return x1 + (4075 + date_float) * dots_year

def y_position(row_y):
    global y2
    return y2 - 1 - row_y * 12  # vertically centered 10 point script in 12 pt line

def drawString(text, fontsize, x_string, y_string, position):
    c.setFont("Aptos", fontsize)
    if len(text) == 0: # don't draw empty strings
        return
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
    elif position == "cb":
        c.setFont("Aptos", fontsize)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_string, y_string, text)

# initiate variables
def initiate_counters():
    global counter_persons, counter_judges, counter_prophets, counter_kings, counter_periods, counter_events
    counter_persons  = 0
    counter_judges   = 0
    counter_prophets = 0
    counter_kings    = 0
    counter_periods  = 0
    counter_events   = 0

# Import strings for the respective language for names and comments
def import_dictionary():
    global dict
    print(f"Import dictionary for names and descriptions, language: {language}")
    file_dictionary = "../db/dictionary_" + language + ".tsv"
    key_dict = pd.read_csv(file_dictionary, encoding='utf8', sep = '\t')
    for index, row in key_dict.iterrows():
        dict.update({f"{row.key}" : f"{row.text}"})

# Import colors for all keys
def import_colors(c_scheme):
    global color, color_scheme
    color_scheme = c_scheme
    print(f"Import color scheme: {color_scheme}")
    file_colors = "../db/colors_" + color_scheme + ".csv"
    key_colors = pd.read_csv(file_colors, encoding='utf8')
    for index, row in key_colors.iterrows():
        color.update({f"{row.key}" : (row.R, row.G, row.B)})

def create_canvas():
    global c, filename
    # Create the canvas
    filename = "../timeline/timeline_v" + version + "_"+ language + ".pdf"
    c = canvas.Canvas(filename, pagesize=(page_width,page_height))
    c.setAuthor(pdf_author)
    c.setTitle(dict['pdf_title'])
    c.setSubject(dict['pdf_subject'])

def create_drawing_area():
    global drawing_height, drawing_width, d, x1, y1, x2, y2
    drawing_width  = page_width - 2 * border_lr
    drawing_height = page_height - 2 * border_tb
    d = Drawing(drawing_width, drawing_height)
    x1 = border_lr
    y1 = border_tb
    x2 = x1 + drawing_width
    y2 = y1 + drawing_height

    # The drawing should span from 4075 BCE to 2075 CE, so we have to calculate
    # the length of one year in dots from drawing_with for this 6150 years
    global dots_year
    dots_year = drawing_width / 6150

def create_horizontal_axis():
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

    c.drawString(x1, y1 - 16, dict["BCE"])
    c.drawString(x1, y2 + 8 , dict["BCE"])
    c.drawRightString(x2, y1 - 16, dict["CE"])
    c.drawRightString(x2, y2 + 8,  dict["CE"])

def create_adam_moses():
    # unique pattern for people from Adam to Moses, and eventline for deluge
    global counter_persons
    global counter_events

    # Blue line for the deluge in 2370 BCE
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 1)
    date_deluge = x_position(-2370)
    c.line(date_deluge, y1, date_deluge, y2)
    drawString(f"{dict['Deluge']} 2370 {dict['BCE']}", 12, date_deluge + 2, y2 - 16, "r")
    counter_events += 1

    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data Adam to Moses")
    persons = pd.read_csv("../db/adam-moses.csv", encoding='utf8')
    c.setFont("Aptos", 12)
    for index, row in persons.iterrows():
        born = -year(row.born)
        died = -year(row.died)
        person = dict[f"{row.key}"]
        details_r = f"{born} {dict['to']} {died} {dict['BCE']} - {born - died} {dict['years']}"
        x_box = x_position(row.born)
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
            drawString(f"{father_born - born} {dict['years']}", 9, x_box - 3, y_box + 11, "l")
        father_born = born
        counter_persons += 1

def create_reference_events():
    # Deluge in 2370 BCE is special and included in the Adam_Moses part
    global counter_events

    print("Import data of reference events")
    events = pd.read_csv("../db/events.csv", encoding='utf8')
    for index, row in events.iterrows():
        x_txt  = x_position(row.date) + 2
        c.setLineWidth(row.width)
        c.setStrokeColorRGB(0.3, 0.0, 0.0)
        c.line(x_position(row.date), y_position(row.y_start), x_position(row.date), y_position(row.y_end))
        if row.position == "l":
            x_txt -= 4
        drawString(dict[row.key], 10, x_txt, y_position(row.y_text), row.position)
        counter_events += 1

def create_judges():
    global counter_judges
    print("Import data of judges")
    judges = pd.read_csv("../db/judges.csv", encoding='utf8')
    for index, row in judges.iterrows():
        start = row.start
        end   = row.end
        x_box = x_position(start)
        y_box = y_position(row.row_y)
        x_boxwidth = (end -  start) * dots_year
        c.setLineWidth(0.2)
        c.setStrokeColorRGB(0, 0, 0)
        co = color['judges']
        c.setFillColorRGB(co[0], co[1], co[2])
        c.rect(x_box, y_box + 10, x_boxwidth, 2, fill = 1)

        # indicate years of oppression prior to peacetime of the judge
        oppression = row.oppression
        x_oppression = x_box - oppression * dots_year
        x_opp_width  = oppression * dots_year
        co = color['oppression']
        c.setFillColorRGB(co[0], co[1], co[2])
        c.rect(x_oppression, y_box + 10, x_opp_width, 2, fill = 1)

        judge = dict[row.key]
        drawString(judge, 10, x_box + x_boxwidth * 0.5 , y_box, "cb")
        counter_judges += 1

def create_kings():
    global counter_kings
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data of kings")
    kings = pd.read_csv("../db/kings.csv", encoding='utf8')
    c.setFont("Aptos", 10)
    c.setLineWidth(0.3)
    for index, row in kings.iterrows():
        start = row.start
        end   = row.end
        if row.born < 0:
            born = row.born
            detail_born = ", " + dict["became_king"] + f" {int(start-born)}"
        else:
            born = start
            detail_born = ""
        detail = dict[f"{row.key}"] + " "
        time_reigned = "("
        if row.years > 0:
            time_reigned += f"{row.years} "
            if row.years > 1:
                time_reigned += f"{dict['years']}"
            else:
                time_reigned += f"{dict['year']}"
        if row.months > 0:
            time_reigned += f"{row.months} "
            if row.months > 1:
                time_reigned += f"{dict['months']}"
            else:
                time_reigned += f"{dict['month']}"
        if row.days > 0:
            if row.months > 0:
                time_reigned += " "
            time_reigned += f"{row.days} {dict['days']}"

        detail += f"{-year(start)}-{-year(end)} {time_reigned})" + detail_born
        if index < 23:
            detail_l = ""
            detail_r = detail
        else:
            detail_l = detail
            detail_r = ""
        x_box  = x_position(start) 
        x_born = x_position(born)
        y_box  = y_position(row.row_y)
        x_boxwidth = (end -  start) * dots_year
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.line(x_born, y_box + 3, x_box, y_box + 3)
        c.line(x_born, y_box -2, x_born, y_box + 8)
        co = color[row.key]
        c.setFillColorRGB(co[0], co[1], co[2])
        c.rect(x_box, y_box - 3, x_boxwidth, 12, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail_r, 10, x_box + x_boxwidth + 2, y_box, "r")
        drawString(detail_l, 10, x_box - 2, y_box, "l")
        counter_kings += 1

def timebar(x, y, width, R, G, B):
    c.setLineWidth(0.0)
    c.setStrokeColorRGB(1, 1, 1)
    c.setFillColorRGB(R, G, B)
    c.rect(x, y, width, 4, fill = 1, stroke = 0)        
    # let's overdraw left and right side with some shades, 75% 50% and 25%
    factor = [0.75, 0.50, 0.25]
    for i in range(3):
        c.setFillColorRGB(1 - factor[i] * (1 - R), 1 - factor[i] * (1 - G), 1 - factor[i] * (1 - B))
        c.rect(x + 2 - i,         y, 1, 4, fill = 1, stroke = 0)
        c.rect(x + width - 3 + i, y, 1, 4, fill = 1, stroke = 0)

def create_prophets():
    global counter_prophets
    print("Import data of prophets")
    prophets = pd.read_csv("../db/prophets.csv", encoding='utf8')
    for index, row in prophets.iterrows():
        start = row.start
        end   = row.end
        x_box = x_position(start)
        y_box = y_position(row.row_y)
        x_boxwidth = (end -  start) * dots_year
        co = color['prophets']
        timebar(x_box, y_box + 10, x_boxwidth, co[0], co[1], co[2])
        prophet = dict[row.key]
        c.setFont("Aptos", 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_box , y_box, prophet)
        counter_prophets += 1

def create_books():
    global counter_persons
    print("Import data of books")
    books = pd.read_csv("../db/books.csv", encoding='utf8')
    for index, row in books.iterrows():
        start = row.start
        end   = row.end
        x_box = x_position(start)
        y_box = y_position(row.row_y)
        x_boxwidth = (end -  start) * dots_year
        co = color['books']
        timebar(x_box, y_box + 10, x_boxwidth, co[0], co[1], co[2])
        book = dict[row.key]
        c.setFont("Aptos", 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_box , y_box, book)
        counter_persons += 1

def create_caesars():
    global counter_kings
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    print("Import data of caesars")
    caesars = pd.read_csv("../db/caesars.csv", encoding='utf8')
    c.setFont("Aptos", 10)
    c.setLineWidth(0.3)
    for index, row in caesars.iterrows():
        born  = row.born
        start = row.start
        end   = row.end
        detail = dict[row.key] + " "
        if start < 0:
            detail += f"{int(-start+1)} {dict['BCE']} - "
        else:
            detail += f"{int(start)}-"
        if end < 0:
            detail += f" {int(-end+1)} {dict['BCE']}"
        else:
            detail += f"{int(end)} {dict['CE']}"
        x_box  = x_position(start)
        x_born = x_position(born)
        y_box  = y_position(row.row_y)
        x_boxwidth = (end -  start) * dots_year
        co = color['caesars']
        c.setFillColorRGB(co[0], co[1], co[2])

        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box - 3, x_boxwidth, 12, fill = 1)
        c.line(x_born, y_box + 3, x_box, y_box + 3)
        c.line(x_born, y_box - 2, x_born, y_box + 8)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail, 10, x_box + x_boxwidth + 2, y_box, "r")
        counter_kings += 1

def create_periods():
    global counter_periods
    # Import the perios with start and end as pandas dataframe
    print("Import data of periods")
    periods = pd.read_csv("../db/periods.csv", encoding='utf8')
    c.setFont("Aptos", 10)
    c.setLineWidth(0.3)
    for index, row in periods.iterrows():
        detail_c = detail = ""
        start = row.start
        end   = row.end
        key   = row.key
        x_box = x_position(start)
        y_box = y_position(row.row_y)
        x_boxwidth = (end - start) * dots_year
        co = color[f"{row.key}"]
        c.setFillColorRGB(co[0], co[1], co[2])
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box - 3, x_boxwidth, 12, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        if len(row.text_center) > 1:
            detail_c = dict[row.text_center]
            drawString(detail_c, 10, x_box + x_boxwidth * 0.5, y_box, "c")
        detail = dict[key]
        if row.location_description == "l":
            drawString(detail, 10, x_box - 2, y_box, "l")
        else:
            drawString(detail, 10, x_box + x_boxwidth + 2, y_box, "r")
        counter_periods += 1


def create_timestamp():
    timestamp_details = ["persons", "judges", "prophets", "kings", "periods", "events"]
    for index, detail in enumerate(timestamp_details):
        drawString(f"{dict[detail]}", 4, x1 + 6,   y1 + 29.0 - 4.5 * index, "r")
        counter_detail = str(eval("counter_" + detail))
        drawString(counter_detail,    4, x1 + 5.4, y1 + 29.0 - 4.5 * index, "l")
    c.setFont("Aptos", 4)
    c.drawString(x1, y1 + 2, f"Timeline {version} - created {str(datetime.datetime.now())[0:16]}")

def render_to_file():
    renderPDF.draw(d, c, border_lr, border_tb)
    c.showPage()
    c.save()
    print(f"File exported: {filename}")

def create_timeline(lang):
    global language
    language = lang
    initiate_counters()
    import_dictionary()
    import_colors("normal")
    create_canvas()
    create_drawing_area()
    create_horizontal_axis()
    create_adam_moses()
    create_reference_events()
    create_judges()
    create_kings()
    create_prophets()
    create_books()
    create_periods()
    create_caesars()
    create_timestamp()
    render_to_file()

if __name__ == "__main__":
    create_timeline("en")
    create_timeline("de")
    # create_timeline("vn")
