# Create a pdf document that is a timeline for the last 6000 years
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
from svglib.svglib import svg2rlg
import pandas as pd
import googletrans
import datetime
import sys
import os

# Some general settings
version  = 4.5
language = "en"
language_str = "English"
color_scheme = "normal"
border_lr    = 10*mm                      # space left/right for roll holders
border_tb    = 7*mm                       # space for the years top and bottom
page_width   = 4*297*mm + 2 * border_lr   # 4x A4 landscape
page_height  = 210*mm                     #    A4 landscape height
pdf_author   = "https://github.com/kreier/timeline"
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
CJKAST = ["Japanese", "Korean", "SimplifiedChinese", "Arabic", "Sinhala", "Thai", "Georgian"]
for glyphs in CJKAST:
    fontname = "Noto" + glyphs
    fontfile = "fonts/Noto" + glyphs + ".ttf"
    fontname_bold = "Noto" + glyphs + "-bold"
    fontfile_bold = "fonts/Noto" + glyphs + "-bold.ttf"
    pdfmetrics.registerFont(TTFont(fontname, fontfile))
    pdfmetrics.registerFont(TTFont(fontname_bold, fontfile_bold))
pdfmetrics.registerFont(TTFont('NotoCuneiform', 'fonts/NotoCuneiform.ttf')) # Akkadian

supported = {"ar": "Arabic (العربية)",
             "de": "German (Deutsch)",
             "en": "English", 
             "es": "Spanish (Español)", 
             "fi": "Finnish (Suomi)", 
             "fr": "French (Français)",
             "ig": "Igbo (Ásụ̀sụ́ Ìgbò)",
             "ilo": "Iloko (Illocano)",
             "ja": "Japanese (日本語)",
             "ko": "Korean (한국인)",
             "no": "Norwegian (norsk)",
             "ru": "Russian (Русский)",
             "zh": "Chinese (Simplified) [中文简体(普通话)]",
             "si": "Sinhala (සිංහල)",
             "th": "Thai (ภาษาไทย)",
             "vi": "Vietnamese (Tiếng Việt)"}

def create_dictionary(target_language):
    global dict, language
    filename = "../db/dictionary_" + target_language + ".csv"
    if os.path.isfile(filename):
        print(f"A dictionary file {filename} already exists. Delete it if you want to create a new Google translated file.")
        return    
    reference = pd.DataFrame() # will contain the english dictionary with 'key' and 'text' column, plus 'alternative' and 'notes' (not used)
    reference = pd.read_csv("../db/dictionary_reference.csv")
    print(f"Imported reference english dictionary, found {len(reference)} entries.")
    print(reference)
    dict = reference[['key', 'text', 'notes']].copy()  # create a new dictionary, copy columns key and text
    dict['english'] = reference['text'].copy()         # add a column 'english' and fill with 'text' from english dictionary
    print("\nTranslating ...")
    translator = googletrans.Translator()
    number_characters = 0                  # you can translate up to 500,000 characters per month for free
    for index, row in dict.iterrows(): # with 3 columns 'key' 'text' and 'english'
        english_text = row.english
        number_characters += len(english_text)
        if not english_text == " ": # it only applies to row 9 where in english is an empty string (unline Vietnamese or Russian)
            dict.at[index, 'text'] = translator.translate(english_text, src='en', dest=language).text
            print('.', end='')
            # print(f'English: {english_text}, Translated: {dict_translated[index]}')
        if (index + 1) % 40 == 0:
            print(f" {index}")
    print(dict)
    print("Exporting ...")
    dict.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")

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

def y_position(row_y): # with update 2024/03/12 to height 204 -> 210mm we now have 46 lines
    global y2
    return y2 + 1 - row_y * 12  # vertically centered 10 point script in 12 pt line

def drawString(text, fontsize, x_string, y_string, position):
    c.setFont(font_regular, fontsize)
    if len(text) == 0: # don't draw empty strings
        return
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1)
    xtra = 0
    if fontsize < 4:
        xtra = 1
    white_width = stringWidth(text, font_regular, fontsize)
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
        c.setFont(font_bold, fontsize)
        c.setFillColorRGB(1, 1, 1)
        if fontsize == 10:
            c.drawCentredString(x_string, y_string, text)
        else: # probably persian (farsi) or arabic
            c.drawCentredString(x_string, y_string + 1, text)
    elif position == "cb":
        c.setFont(font_regular, fontsize)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_string, y_string, text)

# initiate variables
def initiate_counters():
    global counter_people, counter_judges, counter_prophets, counter_kings, counter_periods, counter_events, counter_objects, counter_terahfam
    counter_people   = 0
    counter_judges   = 0
    counter_prophets = 0
    counter_kings    = 0
    counter_periods  = 0
    counter_events   = 0
    counter_objects  = 0
    counter_terahfam = 0

# Import strings for the respective language for names and comments
def import_dictionary():
    global dict, font_regular, font_bold, version, fontsize_regular
    dict = {}
    # first import the reference dictionary in english
    reference = "../db/dictionary_reference.csv"
    key_dict = pd.read_csv(reference, encoding='utf8')
    for index, row in key_dict.iterrows():
        dict.update({f"{row.key}" : f"{row.text}"})
    # now overwrite with the translated text values
    file_dictionary = "../db/dictionary_" + language + ".csv"
    key_dict = pd.read_csv(file_dictionary, encoding='utf8')
    for index, row in key_dict.iterrows():
        dict.update({f"{row.key}" : f"{row.text}"})
    font_regular = "Aptos"
    font_bold = "Aptos-bold"
    special_fonts = {"jp" : "Japanese",
                     "ja" : "Japanese",
                     "kr" : "Korean",
                     "ko" : "Korean",
                     "sc" : "SimplifiedChinese",
                     "zh" : "SimplifiedChinese",
                     "zh-cn" : "SimplifiedChinese",
                     "zh-tw" : "SimplifiedChinese",
                     "ar" : "Arabic",
                     "fa" : "Arabic",
                     "si" : "Sinhala",
                     "th" : "Thai", 
                     "ka" : "Georgian"}
    if language in special_fonts:
        language_fontname = special_fonts[language]
        font_regular = "Noto" + language_fontname
        font_bold    = "Noto" + language_fontname + "-bold"
        if language == "si":
            fontsize_regular = 9
        if language == "ar" or language == "fa":
            fontsize_regular = 8
    # special_languages = ["jp", "kr", "sc", "ar", "si", "thai"]
    # for special_language in special_languages:
    #     if language == special_language:
    #         abbreviation = language.upper()
    #         font_regular = "Noto" + abbreviation
    #         font_bold    = "Noto" + abbreviation + "-bold"
    print(f"Imported dictionary: {len(key_dict)} keywords")
    version = float(dict["version"])
    print(f"Version {version}")

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
    filename = "../timeline/timeline_v" + str(version) + "_"+ language + ".pdf"
    c = canvas.Canvas(filename, pagesize=(page_width,page_height))
    c.setAuthor(pdf_author)
    c.setTitle(dict['pdf_title'])
    c.setSubject(dict['pdf_subject'])

def create_drawing_area():
    global drawing_height, drawing_width, d, x1, y1, x2, y2
    drawing_width  = page_width - 2 * border_lr
    drawing_height = page_height - 2 * border_tb
    d = Drawing(drawing_width, drawing_height)
    # d = Drawing(page_width, page_height)
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
    c.setFont(font_regular, 11)
    # bce_width = stringWidth(dict["BCE"], font_regular, 11)
    # print(f"The BCE string is {bce_width} points wide.")
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
        # offset_x = stringWidth(year, font_regular, 11) * 0.5
        print_year = True
        ''' a remnant from the fix in v4.0 before making the page wider by 20 mm left/right
        if i == 0:                                               # the year 4000 BCE
            if stringWidth(dict["BCE"], font_regular, 11) > 30:
                print_year = False
        if i == 60:                                              # the year 2000 CE
            if stringWidth(dict["CE"], font_regular, 11) > 30:
                print_year = False
        '''
        if i == 39:                                              # the year 100 BCE
            if stringWidth(dict["BCE"], font_regular, 11) > 60:
                print_year = False
        if i == 41:                                              # the year 100 CE
            if stringWidth(dict["CE"], font_regular, 11) > 60:
                print_year = False
        if year == "0":                                          # there is no year zero
            print_year = False
            tick_x = x1 + (4075) * dots_year
            c.setLineWidth(1.0)
            c.line(tick_x, y1, tick_x, y1 - 6*mm)
            c.line(tick_x, y2, tick_x, y2 + 6*mm)
            c.drawString(tick_x + 2, y1 - 16, dict["CE"])
            c.drawString(tick_x + 2, y2 +  8, dict["CE"])
            c.drawRightString(tick_x - 2, y1 - 16, dict["BCE"])
            c.drawRightString(tick_x - 2, y2 +  8, dict["BCE"])
        
        if print_year:
            c.drawCentredString(tick_x, y1 - 16, year)           # bottom
            c.drawCentredString(tick_x, y2 + 8,  year)           # top

        # vertical lines for centuries
        if vertical_lines:
            c.setLineWidth(0.1)
            c.line(tick_x, y1, tick_x, y2)

            # from 1100 to 600 BCE also every 50 years
            if i > 28 and i < 35:
                c.line(tick_x + 50 * dots_year, y1, tick_x + 50 * dots_year, y2)

    c.drawRightString(x1 + 20, y1 - 16, dict["BCE"])
    c.drawRightString(x1 + 20, y2 + 8 , dict["BCE"])
    c.drawString(x2 - 20, y1 - 16, dict["CE"])
    c.drawString(x2 - 20, y2 + 8,  dict["CE"])

def create_adam_moses():
    # unique pattern for people from Adam to Moses, and eventline for deluge
    global counter_people
    global counter_events

    # Blue line for the deluge in 2370 BCE
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 1)
    date_deluge = x_position(-2370)
    c.line(date_deluge, y1, date_deluge, y2)
    drawString(f"{dict['Deluge']} 2370 {dict['BCE']}", 12, date_deluge + 2, y2 - 16, "r")
    counter_events += 1

    # one special for Job
    co = color['books']
    job_y = 41  # see books.csv for the text and second timebar at 41.9
    c.setFillColorRGB(0.75 + 0.25 * co[0], 0.75 + 0.25 * co[1], 0.75 + 0.25 * co[2])
    x_start = x_position(-1675)
    y_start = y_position(job_y)
    x_width = (1675 - 1485) * dots_year
    c.rect(x_start, y_start, x_width, 2, fill = 1, stroke = 0)

    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    people = pd.read_csv("../db/adam-moses.csv", encoding='utf8')
    print("Imported data Adam to Moses:", len(people))
    c.setFont(font_regular, 12)
    for index, row in people.iterrows():
        born = -year(row.born)
        died = -year(row.died)
        person = dict[f"{row.key}"]
        details_r = f"{born} {dict['to']} {died} {dict['BCE']} - {born - died} {dict['years_age']}"
        if language == "ilo":
            details_r = f"{born} {dict['to']} {died} {dict['BCE']} - {dict['years_age']} {born - died}"
        x_box = x_position(row.born)
        y_box = y2 - index*21 - 21
        if index == 23:  # Moises
            y_box -= 12
        x_boxwidth = (born - died) * dots_year
        x_text = x_box + x_boxwidth * 0.5
        co = color[f"{row.key}"]
        c.setFillColorRGB(co[0], co[1], co[2])
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.3)
        c.rect(x_box, y_box, x_boxwidth, 19, fill = 1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont(font_bold, 15)
        if language == "ar" or language == "fa":
            c.setFont(font_bold, 13)
            y_box += 2
        if language == "si":
            c.setFont(font_bold, 13)
            y_box += 1
        c.drawCentredString(x_text, y_box + 5, person)
        drawString(details_r, 12, x_box + x_boxwidth + 2, y_box + 6, "r")
        if index > 0 and index < 23:
            father_age_when_son_born = f"{father_born - born} {dict['years_age']}"
            if language == "ilo":
                father_age_when_son_born = f"{dict['years_age']} {father_born - born}"
            drawString(father_age_when_son_born, 9, x_box - 3, y_box + 11, "l")
        father_born = born
        counter_people += 1

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
    drawString(dict[text], fontsize_regular, x_txt, y_txt, pos)
    points = [x_line, y_txt + 1, x_line + x_add, y_txt + 3, x_line, y_txt + 5]
    d.add(Polygon(points, fillColor=(lc[0], lc[1], lc[2]), strokeColor=(lc[0], lc[1], lc[2]), strokeWidth = 0.1))

def create_events_objects():
    global counter_objects
    items = pd.read_csv("../db/events_objects.csv", encoding='utf8')
    for index, row in items.iterrows():
        draw_event(row.key, row.date, row.y_start, row.y_end, row.y_text, row.width, row.position)
        counter_objects += 1

def create_reference_events():
    # Deluge in 2370 BCE is special and included in the Adam_Moses part
    global counter_events
    events = pd.read_csv("../db/events.csv", encoding='utf8')
    print("Imported data of reference events:", len(events))
    for index, row in events.iterrows():
        draw_event(row.key, row.date, row.y_start, row.y_end, row.y_text, row.width, row.position)
        counter_events += 1

def create_judges():
    global counter_judges, fontsize_regular
    judges = pd.read_csv("../db/judges.csv", encoding='utf8')
    print("Imported data of judges:", len(judges))
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
        drawString(judge, fontsize_regular, x_box + x_boxwidth * 0.5 , y_box, "cb")
        counter_judges += 1

def create_kings():
    global counter_kings, fontsize_regular
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    kings = pd.read_csv("../db/kings.csv", encoding='utf8')
    print("Imported data of kings:", len(kings))
    c.setFont(font_regular, 10)
    c.setLineWidth(0.3)
    for index, row in kings.iterrows():
        start = row.start
        end   = row.end
        if row.born < 0:
            born = row.born
            detail_born = ", " + dict["became_king"] + f" {int(start-born)} " + dict["age_kings"]
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
        # horizontal T-graph for time before coming king
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        c.line(x_born, y_box + 3, x_box, y_box + 3)
        c.line(x_born, y_box -2, x_born, y_box + 8)
        # box to indicate time of reign
        co = color[row.key]
        c.setFillColorRGB(co[0], co[1], co[2])
        c.rect(x_box, y_box - 3, x_boxwidth, 12, fill = 1)
        c.setFillColorRGB(0, 0, 0)
        drawString(detail_r, fontsize_regular, x_box + x_boxwidth + 2, y_box, "r")
        drawString(detail_l, fontsize_regular, x_box - 2, y_box, "l")
        counter_kings += 1

def faded_color(red, green, blue, percent):
    return [1 - percent * (1 - red), 1 - percent * (1 - green), 1 - percent * (1 - blue)]

def timebar(x, y, width, R, G, B, exact):
    c.setLineWidth(0.0)
    c.setStrokeColorRGB(1, 1, 1)
    c.setFillColorRGB(R, G, B)
    c.rect(x, y, width, 4, fill = 1, stroke = 0)
    if exact:
        return
    fade_steps = 35
    for i in range(fade_steps):
        co = faded_color(R, G, B, (i+1)/fade_steps)
        c.setFillColorRGB(co[0], co[1], co[2])
        c.rect(x + 3 * i/fade_steps - 0.1,   y, 1, 4, fill = 1, stroke = 0)
        c.rect(x + width - 3 * i/fade_steps, y, 1, 4, fill = 1, stroke = 0)

def text_with_timebar(text, row, year_start, year_end, R, G, B, exact):
    global fontsize_regular
    x_box = x_position(year_start)
    y_box = y_position(row)
    x_boxwidth = (year_end -  year_start) * dots_year
    timebar(x_box, y_box + 10, x_boxwidth, R, G, B, exact)
    c.setFont(font_regular, 10)
    c.setFillColorRGB(0, 0, 0)
    drawString(text, fontsize_regular, x_box, y_box, "r")
    # c.drawString(x_box , y_box, text)

def create_prophets():
    global counter_prophets
    prophets = pd.read_csv("../db/prophets.csv", encoding='utf8')
    print("Imported data of prophets:", len(prophets))
    co = color['prophets']
    for index, row in prophets.iterrows():
        text_with_timebar(dict[row.key], row.row_y, row.start, row.end, co[0], co[1], co[2], False)
        counter_prophets += 1

def create_books():
    global counter_people
    books = pd.read_csv("../db/books.csv", encoding='utf8')
    print("Imported data of books:", len(books))
    co = color['books']
    for index, row in books.iterrows():
        text_with_timebar(dict[row.key], row.row_y, row.start, row.end, co[0], co[1], co[2], False)
        counter_people += 1

def create_people():
    global counter_people
    people = pd.read_csv("../db/people.csv", encoding='utf8')
    print("Imported data of people:", len(people))
    co = color['people']
    for index, row in people.iterrows():
        exact = False
        if row.exact == "y":
            exact = True      
        text_with_timebar(dict[row.key], row.row_y, row.start, row.end, co[0], co[1], co[2], exact)
        counter_people += 1

def create_objects():
    global counter_objects
    objects = pd.read_csv("../db/objects.csv", encoding='utf8')
    print("Imported data of objects or items:", len(objects))
    co = color['objects']
    for index, row in objects.iterrows():
        if row.key == "gilgamesh":
            x_boxwidth = (row.end -  row.start) * dots_year
            timebar(x_position(row.start), y_position(row.row_y) + 10, x_boxwidth, co[0], co[1], co[2], False)
            c.setFont("NotoCuneiform", 10)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x_position(row.start) , y_position(row.row_y), dict["gilgamesh"])
        else:
            text_with_timebar(dict[row.key], row.row_y, row.start, row.end, co[0], co[1], co[2], False)
            counter_objects += 1

def create_caesars():
    global counter_kings, fontsize_regular
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    caesars = pd.read_csv("../db/caesars.csv", encoding='utf8')
    print("Imported data of caesars:", len(caesars))
    c.setFont(font_regular, 10)
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
        drawString(detail, fontsize_regular, x_box + x_boxwidth + 2, y_box, "r")
        counter_kings += 1

def create_periods():
    global counter_periods, fontsize_regular
    # Import the perios with start and end as pandas dataframe
    periods = pd.read_csv("../db/periods.csv", encoding='utf8')
    print("Imported data of periods:", len(periods))
    c.setFont(font_regular, 10)
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
                c.rect(x_box + fade_width * i/fade_steps, y_box - 3, 1, 12, fill = 1, stroke = 0)

        c.setFillColorRGB(0, 0, 0)
        if len(row.text_center) > 1:
            detail_c = dict[row.text_center]
            textsize = fontsize_regular
            while stringWidth(detail_c, font_bold, textsize, 'utf8') > x_boxwidth and textsize > 4:
                textsize -= 1
                print(textsize, " ", detail_c)
            drawString(detail_c, textsize, x_box + x_boxwidth * 0.5, y_box, "c")
        detail = dict[key]
        if row.location_description == "l":
            drawString(detail, fontsize_regular, x_box - 2, y_box, "l")
        else:
            drawString(detail, fontsize_regular, x_box + x_boxwidth + 2, y_box, "r")
        counter_periods += 1

def create_terah_familytree():
    global counter_terahfam
    lines = pd.read_csv("../db/terah-lines.csv", encoding='utf8')
    c.setFont(font_regular, 10)
    for index, row in lines.iterrows():
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0, 0, 0)
        if row.type == "married":
            c.setLineWidth(1.0)
            c.setStrokeColorRGB(0.05, 0.61, 0.05)
        x_1 = x_position(-row.start)
        y_1 = y_position(row.start_row - 0.25)
        x_2 = x_position(-row.end)
        y_2 = y_position(row.end_row - 0.25)
        c.line(x_1, y_1, x_2, y_2)
    terah = pd.read_csv("../db/terah-family.csv", encoding='utf8')
    print(f"Imported family tree of Terah: {len(terah)} text fields")
    c.setStrokeColorRGB(1, 1, 1)
    red  = color["terah_red"]
    blue = color["terah_blue"]
    for index, row in terah.iterrows():
        text_width = stringWidth(dict[row.key], font_regular, 10)
        x = x_position(-row.left)
        y = y_position(row.row)
        c.setLineWidth(2.0)
        c.setFillColorRGB(1, 1, 1)
        c.rect(x - 0.5 * text_width - 1, y - 2, text_width + 2, 10, fill = 1)
        c.setFillColorRGB(blue[0], blue[1], blue[2])
        if row.color == "red":
            c.setFillColorRGB(red[0], red[1], red[2])
        c.drawCentredString(x, y, dict[row.key])
    counter_terahfam = 80

def include_pictures():
    pictures = pd.read_csv("../db/pictures.csv", encoding='utf8')
    print("Imported list of pictures:", len(pictures))
    for index, row in pictures.iterrows():
        if row.year != "0":
            drawString(str(row.year), 3, x_position(row.x), y_position(row.y) - 2.4, "r")
        location = "../images/" + row.key
        c.drawImage(location, x_position(row.x), y_position(row.y), width=row.width*mm, height=row.height*mm)

def include_pictures_svg():
    pictures_svg = pd.read_csv("../db/pictures_svg.csv", encoding='utf8')
    print("Imported list of SVG pictures:", len(pictures_svg))
    for index, row in pictures_svg.iterrows():
        if row.year != 0:
            drawString(str(row.year), 3, x_position(row.x), y_position(row.y) - 2.4, "r")
        location = "../images/" + row.key + ".svg"
        drawing = svg2rlg(location)
        factor = row.height / drawing.height
        sx = sy = factor
        drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
        drawing.scale(sx, sy)
        renderPDF.draw(drawing, c, x_position(row.x), y_position(row.y))

def create_daniel2():
    desired_height = 96*mm
    shift_upward   = 30*mm    
    kingdoms = ["Babylon", "Medopersia", "Greece", "Rome", "Angloamerica"]
    years = ["607", "", "539", "537", "", "331", "", "63", "70", "1914-1918", "", ""] 
    yearlines = [2, 3, 2, 2, 3]
    current_yearline = 0
    image_shift = int(dict["daniel2_shift"])
    for index, kingdom in enumerate(kingdoms):
        # print(index, ". ", kingdom, " - ", dict[kingdom + "_c"], " - ", dict[kingdom] )
        co = color["daniel2"]
        c.setLineWidth(0.4)
        c.setStrokeColorRGB(co[0], co[1], co[2])
        y_line = y1 + shift_upward + desired_height * (0.91 - index * 0.212)
        c.line(x_position(-3800) + image_shift,y_line, x_position(-4026), y_line)
        c.setFont(font_bold, 12)
        c.setFillColorRGB(co[0], co[1], co[2])
        c.drawString(x_position(-4026), y_line - 12, dict[kingdom + "_c"])
        c.setFont(font_regular, 8)
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.drawString(x_position(-4026), y_line - 22, dict[kingdom])
        current_yearstring = years[current_yearline] + dict["BCE"]
        if index == 4:
            current_yearstring = years[current_yearline] + " " + dict["CE"]
        indentation = stringWidth(current_yearstring, font_regular, 6) + 2
        for yearline in range(yearlines[index]):
            yearstring = ""
            if years[current_yearline] != "":
                yearstring = years[current_yearline] + " " + dict["BCE"]
                if current_yearline > 7:
                    yearstring = years[current_yearline] + " " + dict["CE"]
            c.setFont(font_regular, 6)
            c.drawString(x_position(-4026), y_line - 30 - 8 * yearline, yearstring)
            line_daniel2 = "daniel2_" + str(current_yearline+1)
            c.drawString(x_position(-4026) + indentation, y_line - 30 - 8 * yearline, dict[line_daniel2])
            current_yearline += 1
    drawing = svg2rlg("../images/daniel2.svg")
    factor = desired_height / drawing.height
    sx = sy = factor
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    renderPDF.draw(drawing, c, x_position(-3850) + image_shift, y1 + shift_upward)        

def create_timestamp():
    timestamp_details = ["people", "judges", "prophets", "kings", "periods", "events", "objects", "terahfam"]
    for index, detail in enumerate(timestamp_details):
        drawString(f"{dict[detail]}", 4, x1 + 6,   y1 + 38 - 4.5 * index, "r")
        counter_detail = str(eval("counter_" + detail))
        drawString(counter_detail,    4, x1 + 5.4, y1 + 38 - 4.5 * index, "l")
    c.setFont(font_regular, 4)
    c.drawString(x1, y1 + 2, f"Timeline {version} – created {str(datetime.datetime.now())[0:16]} – {pdf_author} – some images are CC BY-SA")
    if language in supported:
        qr_file = "../images/qr-" + language + ".png"
        c.drawImage(qr_file, x_position(-4026), y_position(9), width=12*mm, height=12*mm)
        c.setFontSize(4.5)
        c.rotate(90)
        timestamp = str(datetime.datetime.now())
        dateindex = timestamp[2:4] + timestamp[5:7] + timestamp[8:10]
        c.drawString(y_position(8.9), -x_position(-3955), "timeline " + language)
        c.drawString(y_position(8.9), -x_position(-3948), dateindex)
        c.rotate(-90)
        # drawString( "timeline " + language, 5, x_position(-4020), y_position(9.5), "r")

def render_to_file():
    # renderPDF.draw(d, c, border_lr, border_tb)
    renderPDF.draw(d, c, 0, 0)
    c.showPage()
    c.save()
    print(f"File exported: {filename}")

def create_timeline(lang):
    global language, version, language_str
    language = lang
    initiate_counters()
    import_dictionary()
    # import_colors("random")
    import_colors("normal")
    create_canvas()
    create_drawing_area()
    create_horizontal_axis()
    create_adam_moses()
    create_reference_events()
    create_events_objects()
    create_judges()
    create_kings()
    create_prophets()
    create_books()
    create_people()
    create_objects()
    create_periods()
    create_caesars()
    if version >= 4.2:
        create_daniel2()
    if version >= 4.3:
        create_terah_familytree()
    include_pictures()
    include_pictures_svg()
    create_timestamp()
    render_to_file()

def checkForValidLanguageCode(langCode):
    data=googletrans.LANGCODES
    for key, value in data.items():
        if value == langCode:
            global language_str
            language_str=key
            return True
    return False

def is_supported(language):
    global language_str
    if language in supported:
        language_str = supported[language]
        print(f"Your selected language {language} is supported: {language_str}")
        return True
    else:
        print(f"Your selected language '{language}' is not directly supported by this timeline project.")
        print(f"Let's check if the language code exists in Google Translate: ", end = "")
        isValid = checkForValidLanguageCode(language)
        if isValid:
            print(f"Found {language_str}.")
            print(f"Now creating a new dictionary in this language with Google Translate.")
            create_dictionary(language)
            return True
        else:
            print(f"Nope.\nIt looks like '{language}' is not a valid language code or it is not supported by Google Translate.")
            return False

if __name__ == "__main__":
    print(f"Timeline v{version}")
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after 6000.py")
        exit()
    language = sys.argv[1]
    if is_supported(language):
        create_timeline(language)
