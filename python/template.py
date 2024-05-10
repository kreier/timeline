# Create a timeline pdf document, template reference size is A4 297x219 mm
# We are using reportlab https://pypi.org/project/reportlab/
# Documentation found on https://docs.reportlab.com/reportlab/userguide/ch1_intro/
# Userguide https://www.reportlab.com/docs/reportlab-userguide.pdf 

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import pandas as pd
import sys
import os

# Some general settings
page_width     = 297*mm     #    A4 landscape
page_height    = 210*mm     #    A4 landscape height
border_lr      = 10*mm                      # space left/right for roll holders
border_tb      = 7*mm                       # space for the years top and bottom
year_start     = 1850
year_end       = 2035
years_step_maj = 10
drawing_width  = page_width - 2 * border_lr
drawing_height = page_height - 2 * border_tb
dots_year      = drawing_width / (year_end - year_start)
output_file    = "../timeline/gb.pdf"
pdf_title      = "Timeline template"
pdf_subject    = "Visualize time"
pdf_author     = "https://github.com/kreier/timeline"
version        = 4.5
language = "en"
language_str = "English"
color_scheme = "normal"
fontsize_regular = 10
vertical_lines  = False

dict  = {}
color = {}

# Check execution location, exit if not in /timeline/python
if os.getcwd()[-6:] != "python":
    print("This script must be executed inside the python folder.")
    exit()

pdfmetrics.registerFont(TTFont('Aptos', 'fonts/aptos.ttf'))
pdfmetrics.registerFont(TTFont('Aptos-bold', 'fonts/aptos-bold.ttf'))

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
    global x1, year_start
    return x1 + (date_float - year_start) * dots_year

def y_position(row_y): # with update 2024/03/12 to height 204 -> 210mm we now have 46 lines
    global y2
    return y2 + 1 - row_y * 12  # vertically centered 10 point script in 12 pt line

def drawString(text, fontsize, x_string, y_string, position):
    c.setFont("Aptos", fontsize)
    if len(text) == 0: # don't draw empty strings
        return
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1)
    xtra = 0
    if fontsize < 6:
        xtra = 1
    white_width = stringWidth(text, "Aptos", fontsize)
    if position == "r":
        c.setFillColorRGB(1, 1, 1)
        c.rect(x_string, y_string - 2 + xtra, white_width, fontsize, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_string, y_string, text)
    elif position == "l":
        c.setFillColorRGB(1, 1, 1)
        c.rect(x_string - white_width, y_string - 2 + xtra, white_width, fontsize, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        c.drawRightString(x_string, y_string, text)
    elif position == "c":
        c.setFont("Aptos-bold", fontsize)
        c.setFillColorRGB(1, 1, 1)
        if fontsize == 10:
            c.drawCentredString(x_string, y_string, text)
        else: # probably persian (farsi) or arabic
            c.drawCentredString(x_string, y_string + 1, text)
    elif position == "cb":
        c.setFont("Aptos", fontsize)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_string, y_string, text)


def create_canvas():
    global c, output_file
    # Create the canvas
    c = canvas.Canvas(output_file, pagesize=(page_width,page_height))
    c.setAuthor(pdf_author)
    c.setTitle(pdf_title)
    c.setSubject(pdf_subject)

def create_drawing_area():
    global drawing_height, drawing_width, d, x1, y1, x2, y2
    d = Drawing(drawing_width, drawing_height)
    # d = Drawing(page_width, page_height)
    x1 = border_lr
    y1 = border_tb
    x2 = x1 + drawing_width
    y2 = y1 + drawing_height


def create_horizontal_axis():
    # axis around drawing area
    c.setLineWidth(0.8)
    c.setStrokeColorCMYK(1.00, 1.00, 0, 0.50) 
    c.line(x1, y1, x1 + drawing_width, y1)
    c.line(x1, y2, x1 + drawing_width, y2)

    # tickmarks and years for 61 centuries
    c.setFont("Aptos", 11)
    # bce_width = stringWidth(dict["BCE"], font_regular, 11)
    # print(f"The BCE string is {bce_width} points wide.")
    year_tick_start = int((year_start + years_step_maj)/years_step_maj + 0.9) * years_step_maj
    year_tick_stop  = int((year_end - years_step_maj)/years_step_maj) * years_step_maj
    major_steps = int((year_tick_stop - year_tick_start)/years_step_maj) + 1
    for i in range(major_steps):
        # main tickmark
        year = year_tick_start + years_step_maj * i
        tick_x = x1 + (year - year_start) * dots_year
        c.setLineWidth(1.0)
        c.line(tick_x, y1, tick_x, y1 - 2*mm)
        c.line(tick_x, y2, tick_x, y2 + 2*mm)

        # smaler ticks left and right - four left
        step_minor = int(years_step_maj / 10)
        for l in range (-4 * step_minor, 0, step_minor):
            tick_s = tick_x + l * dots_year
            c.line(tick_s, y1, tick_s, y1 - 1*mm)
            c.line(tick_s, y2, tick_s, y2 + 1*mm)
        for r in range (step_minor, step_minor * 6, step_minor):
            tick_s = tick_x + r * dots_year
            c.line(tick_s, y1, tick_s, y1 - 1*mm)
            c.line(tick_s, y2, tick_s, y2 + 1*mm)

        # label the year
        # offset_x = stringWidth(year, font_regular, 11) * 0.5
        print_year = True

        if i == 39:                                              # the year 100 BCE
            if stringWidth("BCE", "Aptos", 11) > 60:
                print_year = False
        if i == 41:                                              # the year 100 CE
            if stringWidth("CE", "Aptos", 11) > 60:
                print_year = False
        if year == "0":                                          # there is no year zero
            print_year = False
            tick_x = x1 + (4075) * dots_year
            c.setLineWidth(1.0)
            c.line(tick_x, y1, tick_x, y1 - 6*mm)
            c.line(tick_x, y2, tick_x, y2 + 6*mm)
            c.drawString(tick_x + 2, y1 - 16, "CE")
            c.drawString(tick_x + 2, y2 +  8, "CE")
            c.drawRightString(tick_x - 2, y1 - 16, "BCE")
            c.drawRightString(tick_x - 2, y2 +  8, "BCE")
        
        if print_year:
            c.drawCentredString(tick_x, y1 - 16, str(year))           # bottom
            c.drawCentredString(tick_x, y2 + 8,  str(year))           # top

        # line for 1914 and 1971
        c.setLineWidth(0.1)
        c.line(x_position(1914), y1, x_position(1914), y2)
        c.line(x_position(1971), y1, x_position(1971), y2)

        # vertical lines for centuries
        if vertical_lines:
            c.setLineWidth(0.1)
            c.line(tick_x, y1, tick_x, y2)

            # from 1100 to 600 BCE also every 50 years
            if i > 28 and i < 35:
                c.line(tick_x + 50 * dots_year, y1, tick_x + 50 * dots_year, y2)

    # c.drawRightString(x1 + 20, y1 - 16, "BCE")
    # c.drawRightString(x1 + 20, y2 + 8 , "BCE")
    # c.drawString(x2 - 20, y1 - 16, "CE")
    # c.drawString(x2 - 20, y2 + 8,  "CE")

def draw_event(text, date, ys, ye, yt, wl, pos):
    global fontsize_regular
    x_line = x_position(date)
    x_txt  = x_line + 4
    y_txt  = y_position(yt)
    x_add  = 2
    if pos == "l":
        x_txt = x_line - 4
        x_add = -x_add
    lc = [0.15, 0.15, 0.2]
    c.setLineWidth(wl)
    c.setStrokeColorRGB(lc[0], lc[1], lc[2])
    c.line(x_line, y_position(ys), x_line, y_position(ye))
    drawString(text, fontsize_regular, x_txt, y_txt, pos)
    points = [x_line, y_txt + 1, x_line + x_add, y_txt + 3, x_line, y_txt + 5]
    d.add(Polygon(points, fillColor=(lc[0], lc[1], lc[2]), strokeColor=(lc[0], lc[1], lc[2]), strokeWidth = 0.1))


def faded_color(red, green, blue, percent):
    return [1 - percent * (1 - red), 1 - percent * (1 - green), 1 - percent * (1 - blue)]

def create_gb():
    # Import the perios with start and end as pandas dataframe
    gb = pd.read_csv("../db/gb.csv", encoding='utf8')
    print("Imported data of governing body:", len(gb))
    c.setFont("Aptos", 10)
    c.setLineWidth(0.3)
    co = [0.6, 0.1, 0.4]
    for index, row in gb.iterrows():
        detail_c = detail = ""
        start = row.start
        end   = row.end
        key   = row.key
        x_box = x_position(start)
        y_box = y_position(row.row_y)
        x_boxwidth = (end - start) * dots_year
        if index > 6:
            co = [0.2, 0.6, 0.7]
        c.setFillColorRGB(co[0], co[1], co[2])
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x_box, y_box - 3, x_boxwidth, 12, fill = 1)
        if index > 6:
            c.setLineWidth(1)
            c.setStrokeColorRGB(1, 0, 0)
            c.line(x_position(row.member), y_box - 3, x_position(row.member), y_box + 9)
        if row.end_fade > row.end:
            fade_width = (row.end_fade - row.end) * dots_year
            x_boxwidth += fade_width
            fade_steps = 50
            for i in range(fade_steps):
                cl = faded_color(co[0], co[1], co[2], (i+1)/fade_steps)
                c.setFillColorRGB(cl[0], cl[1], cl[2])
                c.rect(x_box + x_boxwidth - fade_width * i/fade_steps - 0.8, y_box - 3, 1, 12, fill = 1, stroke = 0)
        if row.start_fade < row.start:
            fade_width = (row.start - row.start_fade) * dots_year + 1
            x_boxwidth += fade_width
            x_box = x_position(row.start_fade)
            fade_steps = 50
            for i in range(fade_steps):
                cl = faded_color(co[0], co[1], co[2], (i+1)/fade_steps)
                c.setFillColorRGB(cl[0], cl[1], cl[2])
                c.rect(x_box + fade_width * i/fade_steps, y_box - 3, fade_width/48, 12, fill = 1, stroke = 0)

        c.setFillColorRGB(0, 0, 0)
        # if len(row.text_center) > 0:
        detail_c = row.key
        textsize = fontsize_regular
        while stringWidth(detail_c, "Aptos-bold", textsize, 'utf8') > x_boxwidth and textsize > 4:
            textsize -= 1
            print(textsize, " ", detail_c)
        drawString(detail_c, textsize, x_box + x_boxwidth * 0.5, y_box, "c")
        # detail = key
        # if row.location_description == "l":
        #     drawString(detail, fontsize_regular, x_box - 2, y_box, "l")
        # else:
        #     drawString(detail, fontsize_regular, x_box + x_boxwidth + 2, y_box, "r")

def render_to_file():
    renderPDF.draw(d, c, 0, 0)   # locations in c are already relative, and d is positioned inside relatively
    c.showPage()
    c.save()
    print(f"File exported: {output_file}")

def create_timeline():
    global version
    create_canvas()
    create_drawing_area()
    create_horizontal_axis()
    create_gb()
    render_to_file()


if __name__ == "__main__":
    print(f"Timeline template v{version}")
    # if len(sys.argv) < 2:
    #     print("You did not provide a language as argument. Put it as a parameter after template.py")
    #     exit()
    # language = sys.argv[1]
    create_timeline()
