# Create a pdf document that is a timeline for the last 6000 years
# We are using fpdf2 from verion 4.7 on https://github.com/py-pdf/fpdf2
# Documentation found on https://py-pdf.github.io/fpdf2/Tutorial.html

from fpdf import FPDF
import pandas as pd
import googletrans # it works again with v4.0.2 since 2024-11-20 that should fix many problems
import datetime, sys, os

# Some general settings - implied area from 4075 BCE to 2075 CE
version  = 5.8
language = "en"
language_str = "English"
color_scheme = "normal"
mm           = 2.834645669                # document is in pt, 46 rows with 12pt height, text 10pt
border_lr    = 10*mm                      # space left/right usually 10, for roll holders 60
border_tb    = 7*mm                       # space for the years top and bottom
page_width   = 4*297*mm + 2 * border_lr   # 4x A4 landscape
page_height  = 210*mm                     #    A4 landscape height
render_type  = "digital"
pdf_author   = "https://github.com/kreier/timeline"
fontsize_regular = 10
fontsize_AMoses  = 16
y_offset         = 0
vertical_lines   = False
left_to_right    = True   # False for Arabic, Hebrew, Persian and other RTL writing systems
direction        = "r"
direction_rl     = "l"
direction_factor = 1
replace_numerals = False  # for Khmer, Arabic, 
daniel2_image    = ""
edition_2025     = False
# logging.getLogger("fpdf.svg").propagate = False # suppress warnings for unsupported svg features

# Check execution location, exit if not in /timeline/python
if os.getcwd()[-6:] != "python":
    print("This script must be executed inside the python folder.")
    exit()

def year(date_float):             # convert the float dates to year, month and day
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

def x_position(date_float):      # area is 6150 years wide from 4075 BCE to 2075 CE
    global x1, left_to_right
    if left_to_right:
        return x1 + (4075 + date_float) * dots_year
    else:
        return x1 + (2075 - date_float) * dots_year

def y_position(row_y):           # with update 2024/03/12 to height 204 -> 210mm we now have 46 lines
    global y1
    return y1 + row_y * 12       # vertically centered 10 point script in 12 pt line, 1pt above/below

def drawString(text, fontsize, x_string, y_string, position, white_background):
    global pdf
    if len(text) == 0:           # don't draw empty strings
        return
    pdf.set_font_size(fontsize)  # set fontcolor and fonttype outside this function
    pdf.set_fill_color(255)
    pdf.set_draw_color(255)
    pdf.set_line_width(0.8)
    xtra = 0                     # used for labels under images
    if fontsize < 6:
        xtra = 0
    pdf.set_text_shaping(use_shaping_engine=True) # explicit to trigger switch to arabic
    white_width = pdf.get_string_width(text) # depends on font, fontsize
    if position == "r":                                                   # r - draw to the right
        if white_background:
            pdf.rect(x_string, y_string, white_width, fontsize, style="FD") # with "F" fill and "D" draw and "DF" or "FD"
        pdf.set_xy(x_string, y_string)
        pdf.cell(text=text)
    elif position == "l":                                                 # l - draw to the left
        if white_background:
            pdf.rect(x_string - white_width, y_string, white_width, fontsize, style="FD")
        pdf.set_xy(x_string - white_width, y_string)
        pdf.cell(text=text, align="R")
    elif position == "c":                                                # c - centered, no BG
        pdf.set_xy(x_string - white_width / 2, y_string)
        pdf.cell(text=text)

def number_to_string(number, language):
    # list_languages_special_numerals = ["ar", "fa", "si", "km"]
    global replace_numerals
    if replace_numerals:
        languages_special_numerals = {'ar': 'arabic_numerals',
                                    'fa': 'farsi_numerals',
                                    'si': 'sinhala_numerals',
                                    'km': 'khmer_numerals'}
        arabic_numerals = {
            '0': '٠',  '1': '١',  '2': '٢',  '3': '٣',  '4': '٤',
            '5': '٥',  '6': '٦',  '7': '٧',  '8': '٨',  '9': '٩'}
        farsi_numerals = {
            '0': '۰',  '1': '۱',  '2': '۲',  '3': '۳',  '4': '۴',
            '5': '۵',  '6': '۶',  '7': '۷',  '8': '۸',  '9': '۹'}
        sinhala_numerals = {
            '0': '෦',  '1': '෧',  '2': '෨',  '3': '෩',  '4': '෪',
            '5': '෫',  '6': '෬',  '7': '෭',  '8': '෮',  '9': '෯'}
        khmer_numerals = {
            '0': '០',  '1': '១',  '2': '២',  '3': '៣',  '4': '៤',
            '5': '៥',  '6': '៦',  '7': '៧',  '8': '៨',  '9': '៩'}
        if language in languages_special_numerals:
            new_numerals = locals()[languages_special_numerals[language]]
            return ''.join(new_numerals[digit] for digit in str(number))
        else:
            return str(number)
    else:
        return str(number)

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

def import_dictionary():           # Import strings for the respective language for names and comments
    global dict, version
    dict = {}
    # first import the reference dictionary in english
    reference = "../db/dictionary_reference.csv"
    key_dict = pd.read_csv(reference, encoding='utf8')
    key_dict = key_dict.fillna(" ")
    for index, row in key_dict.iterrows():
        dict.update({f"{row.key}" : f"{row.text}"})
    # now overwrite with the translated text values
    file_dictionary = "../db/dictionary_" + language + ".csv"
    key_dict = pd.read_csv(file_dictionary, encoding='utf8')
    key_dict = key_dict.fillna(" ")
    for index, row in key_dict.iterrows():
        dict.update({f"{row.key}" : f"{row.text}"})
    print(f"Imported dictionary: {len(key_dict)} keywords")
    version = float(dict["version"])
    print(f"Version {version}")

def import_colors(c_scheme):       # Import colors for all keys
    global color, color_scheme
    color_scheme = c_scheme
    color = {}
    print(f"Import color scheme: {color_scheme}")
    file_colors = "../db/colors_" + color_scheme + ".csv"
    key_colors = pd.read_csv(file_colors, encoding='utf8')
    for index, row in key_colors.iterrows():
        color.update({f"{row.key}" : (row.R, row.G, row.B)})

def create_canvas(edition):
    global pdf, filename, render_type, language_str, x1, y1, x2, y2, page_width, border_lr
    global left_to_right, direction, direction_rl, direction_factor, y_offset, replace_numerals
    global font_regular, font_bold, fontsize_regular, fontsize_AMoses
    print(f"Start creating the edition: {edition}")
    if edition == "print":
        render_type  = "print"
        border_lr    = 60*mm
        page_width   = 4*297*mm + 2 * border_lr
        filename = "../timeline/timeline_v" + str(version) + "_"+ language + "_print.pdf"
    else:
        filename = "../timeline/timeline_v" + str(version) + "_"+ language + ".pdf"
    pdf = FPDF(unit="pt", format=(page_width, page_height))       # no orientation ="landscape" since it only swaps width and height
    pdf.set_margin(0)
    pdf.c_margin = 0
    pdf.add_font("Aptos", style="", fname="fonts/aptos.ttf")
    pdf.set_font("Aptos", "", fontsize_regular)
    pdf.set_text_color(0)
    pdf.add_font("Aptos-bold", style="", fname="fonts/aptos-bold.ttf")
    pdf.add_font("NotoCuneiform", style="", fname="fonts/NotoCuneiform.ttf") # Akkadian    
    pdf.add_page(format=(page_width, page_height))
    pdf.set_author(pdf_author)
    pdf.set_title(dict['pdf_title'])
    pdf.set_subject(dict['pdf_subject'])
    drawing_width  = page_width - 2 * border_lr
    drawing_height = page_height - 2 * border_tb
    x1 = border_lr                                  # left for fpdf2 and reportlab
    y1 = border_tb                                  # in fpdf2 this is top, on reportlab that is bottom
    x2 = x1 + drawing_width
    y2 = y1 + drawing_height

    # The drawing should span from 4075 BCE to 2075 CE, so we have to calculate
    # the length of one year in dots from drawing_with for this 6150 years
    global dots_year
    dots_year = drawing_width / 6150

    # Draw small lines into the corners for the print edition, since print shops import only the
    # content area and exclude the white space from the desired print area
    if edition == "print":
        pdf.set_line_width(0.1)
        pdf.set_draw_color(r=0, g=0, b=0)
        cornerpoints = [[0.1, 0.1, 1, 1], [page_width - 0.2, 0.1, -1, 1], [0.1, page_height - 0.2, 1, -1], [page_width - 0.2, page_height - 0.2, -1, -1]]
        for [x, y, dx, dy] in cornerpoints:
            pdf.line(x, y, x + 10*dx, y)
            pdf.line(x, y, x, y + 10*dy)

    # import features of the supported language into dataframe supported_language
    df = pd.read_csv("../db/supported_languages.csv", encoding='utf8')
    df = df.fillna(" ")
    row_index = df[df['key'] == language].index   # creates array of matching entries with language string
    language_str = df.at[row_index[0], 'language_str'] # language is used for the shape engine

    # set RTL or LTR
    se_direction = "ltr"
    if df.at[row_index[0], 'direction'] == "RTL":
        left_to_right = False
        se_direction = "rtl"
        direction = "l"
        direction_rl = "r"
        direction_factor = -1

    # Import the script/glyph for this language
    if df.at[row_index[0], 'fontname'] == " ":
        font_regular = "Aptos"
        font_bold    = "Aptos-bold"
    else:
        glyphs = df.at[row_index[0], 'fontname']
        fontname = glyphs
        fontfile = "fonts/" + glyphs + ".ttf"
        fontname_bold = glyphs + "-bold"
        fontfile_bold = "fonts/" + glyphs + "-bold.ttf"
        pdf.add_font(fontname, style="", fname=fontfile)
        if os.path.exists(fontfile_bold):
            pdf.add_font(fontname_bold, style="", fname=fontfile_bold)
        else:
            pdf.add_font(fontname_bold, style="", fname=fontfile)
        font_regular = fontname
        font_bold    = fontname_bold
    if df.at[row_index[0], 'shaping_engine']:                  # set the font shaper
        pdf.set_text_shaping(use_shaping_engine=True, 
                                direction=se_direction, 
                                script=df.at[row_index[0], 'script'], 
                                language=df.at[row_index[0], 'language'])
    fontsize_regular = df.at[row_index[0], 'fontsize']
    fontsize_AMoses  = df.at[row_index[0], 'fontsize_AM']
    y_offset         = df.at[row_index[0], 'y_offset']
    if df.at[row_index[0], 'replace_numerals']:
        replace_numerals = True

def create_horizontal_axis():
    global language, left_to_right
    pdf.set_line_width(0.8)
    pdf.set_draw_color(r=0, g=0, b=0)
    pdf.line(x1, y1, x1 + page_width - 2 * border_lr, y1)    # axis on top and bottom of the drawing area
    pdf.line(x1, y2, x1 + page_width - 2 * border_lr, y2)
    pdf.set_font(font_regular, "", 11)                       # tickmarks and years for 61 centuries
    for i in range(61):
        tick_x = x_position(-4075) + (75 + 100 * i) * dots_year * direction_factor
        pdf.set_draw_color(0)
        pdf.line(tick_x, y1, tick_x, y1 - 2*mm)              # main tickmark
        pdf.line(tick_x, y2, tick_x, y2 + 2*mm)
        for l in range (-40, 0, 10):                         # smaller ticks left and right
            tick_s = tick_x + l * dots_year
            pdf.line(tick_s, y1, tick_s, y1 - 1*mm)
            pdf.line(tick_s, y2, tick_s, y2 + 1*mm)
        for r in range (10, 60, 10):
            tick_s = tick_x + r * dots_year
            pdf.line(tick_s, y1, tick_s, y1 - 1*mm)
            pdf.line(tick_s, y2, tick_s, y2 + 1*mm)       
        # label the year - old year = str(abs((100 * i) - 4000))
        year = number_to_string(abs((100 * i) - 4000), language)
        print_year = True
        if i == 39:                                              # the year 100 BCE
            if pdf.get_string_width(dict["BCE"]) > 60:
                print_year = False
        if i == 41:                                              # the year 100 CE
            if pdf.get_string_width(dict["CE"]) > 60:
                print_year = False
        if i == 40:                                              # there is no year zero
            print_year = False
            pdf.line(tick_x, y1, tick_x, y1 - 6*mm)
            pdf.line(tick_x, y2, tick_x, y2 + 6*mm)
            drawString(dict["CE"], 11,  tick_x + 2 * direction_factor, y1 - 17, direction, False)
            drawString(dict["CE"], 11,  tick_x + 2 * direction_factor, y2 +  7, direction, False)
            drawString(dict["BCE"], 11, tick_x - 2 * direction_factor, y1 - 17, direction_rl, False)
            drawString(dict["BCE"], 11, tick_x - 2 * direction_factor, y2 +  7, direction_rl, False)
        if print_year:
            drawString(year, 11, tick_x, y1 - 17, "c", False)
            drawString(year, 11, tick_x, y2 +  7, "c", False)
        if vertical_lines:                                       # vertical lines for centuries
            pdf.set_line_width(0.1)
            pdf.line(tick_x, y1, tick_x, y2)
            if i > 28 and i < 35:                                # from 1100 to 600 BCE also every 50 years
                 pdf.line(tick_x + 50 * dots_year, y1, tick_x + 50 * dots_year, y2)
    drawString(dict["CE"],  11, x_position(2075)  - 20 * direction_factor, y1 - 17, direction, False)
    drawString(dict["CE"],  11, x_position(2075)  - 20 * direction_factor, y2 +  7, direction, False)
    drawString(dict["BCE"], 11, x_position(-4075) + 20 * direction_factor, y1 - 17, direction_rl, False)
    drawString(dict["BCE"], 11, x_position(-4075) + 20 * direction_factor, y2 +  7, direction_rl, False)

def create_adam_moses():
    # unique pattern for people from Adam to Moses, and eventline for deluge
    global counter_people, counter_events, language, fontsize_regular, fontsize_AMoses
    global left_to_right, y_offset, direction, direction_factor

    # Blue line for the deluge in 2370 BCE
    pdf.set_line_width(1.0)
    pdf.set_draw_color(r=0, g=0, b=255)
    date_deluge = x_position(-2370)
    pdf.line(date_deluge, y1, date_deluge, y2)
    x_offset = 2 * direction_factor
    drawString(f"{dict['Deluge']} {number_to_string(2370, language)} {dict['BCE']}", 12, date_deluge + x_offset, y1 + 6, direction, True)
    counter_events += 1

    # one special for Job
    co = color['books']
    job_y = 40.83           # see books.csv for the text and second timebar at 41.9
    pdf.set_fill_color(r=191 + 64 * co[0], g=191 + 64 * co[1], b=191 + 64 * co[2])
    # c.setFillColorRGB(0.75 + 0.25 * co[0], 0.75 + 0.25 * co[1], 0.75 + 0.25 * co[2])
    x_start = x_position(-1675)
    y_start = y_position(job_y)
    x_width = x_position(1675) - x_position(1485)
    pdf.rect(x_start, y_start, x_width, 2, style="F")

    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    people = pd.read_csv("../db/adam-moses.csv", encoding='utf8')
    print("Imported data Adam to Moses:", len(people))
    for index, row in people.iterrows():
        born = -year(row.born)
        died = -year(row.died)
        person = dict[f"{row.key}"]
        details_r = f"{number_to_string(born, language)} {dict['to']} {number_to_string(died, language)} {dict['BCE']} - {number_to_string(born - died, language)} {dict['years_age']}"
        if language == "ilo":
            details_r = f"{born} {dict['to']} {died} {dict['BCE']} - {dict['years_age']} {born - died}"
        x_box = x_position(row.born)
        y_box = y1 + index * 20.5 + 2   # line height was 21 until 2024
        if index > 18:   # after Terah
            y_box += 12.5
        if index == 23:  # Moses
            y_box += 12
        x_boxwidth = x_position(born) - x_position(died)
        x_text = x_box + x_boxwidth * 0.5
        co = color[f"{row.key}"]
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.set_line_width(0.3)
        pdf.set_draw_color(0)
        pdf.rect(x_box, y_box, x_boxwidth, 19, style="FD") # Boxes are 19 pt high, 21 pt seperated from one another - 20.5 since 5.1
        y_box += y_offset
        pdf.set_text_color(255)
        pdf.set_font(font_bold, "", fontsize_AMoses)
        drawString(person, fontsize_AMoses, x_text, y_box + 2, "c", False)
        pdf.set_text_color(0)
        pdf.set_font(font_regular, "", 12)
        drawString(details_r, 12, x_box + x_boxwidth + 2 * direction_factor, y_box + 3.5, direction, True)
        if index > 0 and index < 23:
            father_age_when_son_born = f"{number_to_string(father_born - born, language)} {dict['years_age']}"
            pdf.set_font_size(9)
            if language == "ilo":
                father_age_when_son_born = f"{dict['years_age']} {father_born - born}"
            drawString(father_age_when_son_born, 9, x_box - 3 * direction_factor, y_box + 1, direction_rl, True)
        father_born = born
        counter_people += 1

def draw_event(text, date, ys, ye, yt, wl, pos):
    global fontsize_regular, pdf
    if not left_to_right:
        if pos == "l":
            pos = "r"
        else:
            pos = "l"
    x_line = x_position(date)
    x_txt  = x_line + 4
    y_txt  = y_position(yt) - 9
    x_add  = 2
    if pos == "l":
        x_txt = x_line - 4
        x_add = -x_add
    pdf.set_text_color(0)
    pdf.set_font(font_regular, "", fontsize_regular)
    drawString(dict[text], fontsize_regular, x_txt, y_txt, pos, True)
    pdf.set_line_width(wl)
    pdf.set_draw_color(20, 20, 30)
    pdf.set_fill_color(0)
    pdf.line(x_line, y_position(ys) - 1, x_line, y_position(ye) - 1)
    points = ((x_line, y_txt + 3), (x_line + x_add, y_txt + 5), (x_line, y_txt + 7))
    pdf.polygon(points, style="DF")

def create_reference_events():
    # Deluge in 2370 BCE is special and included in the Adam_Moses part
    global counter_events
    file_events = "../db/events.csv"
    if edition_2025:
        file_events = "../db/events25.csv"
    events = pd.read_csv(file_events, encoding='utf8')
    print("Imported data of reference events:", len(events))
    for index, row in events.iterrows():
        draw_event(row.key, row.date, row.y_start, row.y_end, row.y_text, row.width, row.position)
        counter_events += 1

def create_events_objects():
    global counter_objects
    items = pd.read_csv("../db/events_objects.csv", encoding='utf8')
    for index, row in items.iterrows():
        draw_event(row.key, row.date, row.y_start, row.y_end, row.y_text, row.width, row.position)
        counter_objects += 1

def create_judges():
    global counter_judges, fontsize_regular
    judges = pd.read_csv("../db/judges.csv", encoding='utf8')
    print("Imported data of judges:", len(judges))
    for index, row in judges.iterrows():
        start = row.start
        end   = row.end
        x_box = x_position(start)
        y_box = y_position(row.row_y) - 13
        x_boxwidth = x_position(end) - x_position(start)
        pdf.set_line_width(0.2)
        pdf.set_draw_color(0)
        co = color['judges']
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.rect(x_box, y_box, x_boxwidth, 2, style="FD")           # peaceful period afterwards
        oppression   = row.oppression
        x_oppression = x_position(start - oppression)
        x_opp_width  = x_box - x_oppression
        co = color['oppression']
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.rect(x_oppression, y_box, x_opp_width, 2, style="FD")   # years of opression before
        judge = dict[row.key]
        drawString(judge, fontsize_regular, x_box + x_boxwidth * 0.5 , y_box + 4, "c", True)
        counter_judges += 1

def create_kings():
    global counter_kings, fontsize_regular, left_to_right, direction, direction_factor
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    kings = pd.read_csv("../db/kings.csv", encoding='utf8')
    print("Imported data of kings:", len(kings))
    pdf.set_font(font_regular, size=10)
    pdf.set_line_width(0.3)
    for index, row in kings.iterrows():
        start = row.start
        end   = row.end
        if row.born < 0:
            born = row.born
            detail_born = ", " + dict["became_king"] + f" {number_to_string(int(start-born), language)} " + dict["age_kings"]
        else:
            born = start
            detail_born = ""
        detail = dict[f"{row.key}"] + " "
        time_reigned = "("
        if row.years > 0:
            time_reigned += f"{number_to_string(row.years, language)} "
            if row.years > 1:
                time_reigned += f"{dict['years']}"
            else:
                time_reigned += f"{dict['year']}"
        if row.months > 0:
            time_reigned += f"{number_to_string(row.months, language)} "
            if row.months > 1:
                time_reigned += f"{dict['months']}"
            else:
                time_reigned += f"{dict['month']}"
        if row.days > 0:
            if row.months > 0:
                time_reigned += " "
            time_reigned += f"{number_to_string(row.days, language)} {dict['days']}"

        detail += f"{number_to_string(-year(start), language)}-{number_to_string(-year(end), language)} {time_reigned})" + detail_born
        x_box  = x_position(start) 
        x_born = x_position(born)
        y_box  = y_position(row.row_y) - 10
        x_boxwidth = x_position(end) - x_position(start)        
        # horizontal T-graph for time before coming king
        pdf.set_line_width(0.3)
        pdf.set_draw_color(0)
        pdf.line(x_born, y_box + 6, x_box,  y_box + 6)            # offset with fpdf2 is -3, was +3 with reportlab
        pdf.line(x_born, y_box + 1, x_born, y_box + 11)           # -3-5 = -8 and -3+5 = +2
        # box to indicate time of reign
        co = color[row.key]
        pdf.set_fill_color(255*co[0], 255*co[1], 255*co[2])
        pdf.rect(x_box, y_box, x_boxwidth, 12, style="FD")       # offset y_box was -3 - now its zero
        y_box += 1
        if index < 23:
            drawString(detail, fontsize_regular, x_box + x_boxwidth + 2 * direction_factor, y_box, direction, True)
        else:
            drawString(detail, fontsize_regular, x_box - 2 * direction_factor, y_box, direction_rl, True)        
        counter_kings += 1

def faded_color(red, green, blue, percent):
    return [1 - percent * (1 - red), 1 - percent * (1 - green), 1 - percent * (1 - blue)]

def timebar(x, y, width, R, G, B, exact):
    pdf.set_fill_color(R*255, G*255, B*255)
    if width < 0:
        x += width
        width = -width
    pdf.rect(x, y, width, 4, style="F")
    if exact:
        return
    fade_steps = 35
    for i in range(fade_steps):
        co = faded_color(R, G, B, (i+1)/fade_steps)
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.rect(x + 3 * i/fade_steps - 0.1,   y, 1, 4, style="F")
        pdf.rect(x + width - 3 * i/fade_steps, y, 1, 4, style="F")

def text_with_timebar(text, row, year_start, year_end, R, G, B, exact):
    global fontsize_regular, direction
    x_box = x_position(year_start)
    y_box = y_position(row) - 9
    x_boxwidth = x_position(year_end) - x_position(year_start)    
    timebar(x_box, y_box - 6, x_boxwidth, R, G, B, exact)
    drawString(text, fontsize_regular, x_box, y_box, direction, True)

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
    cunei = ["gilgamesh", "ur3", "hammurabi"]
    co = color['objects']
    for index, row in objects.iterrows():
        if row.key in cunei:
            x_boxwidth = x_position(row.end) - x_position(row.start)
            timebar(x_position(row.start), y_position(row.row_y) - 15, x_boxwidth, co[0], co[1], co[2], False)
            pdf.set_font("NotoCuneiform", "", 9)
            pdf.set_fill_color(0)
            shift = pdf.get_string_width(dict[row.key])
            if left_to_right:
                shift = 0
            pdf.set_xy(x_position(row.start) - shift , y_position(row.row_y) - 8)
            pdf.cell(text=dict[row.key])
            pdf.set_font(font_regular, "", fontsize_regular)
        else:
            text_with_timebar(dict[row.key], row.row_y, row.start, row.end, co[0], co[1], co[2], False)
            counter_objects += 1

def create_periods():
    global counter_periods, fontsize_regular, render_type
    # Import the perios with start and end as pandas dataframe
    periods = pd.read_csv("../db/periods.csv", encoding='utf8')
    print("Imported data of periods:", len(periods))
    pdf.set_font(font_regular, "", 10)
    for index, row in periods.iterrows():
        detail_c = detail = ""
        start = row.start
        end   = row.end
        key   = row.key
        x_box = x_position(start)
        y_box = y_position(row.row_y) - 9
        special_language = {"ilo", "kne"}                 # move maya postclassic one lower
        if language in special_language and key == "maya_postclassic":
            y_box = y_position(row.row_y + 1) - 9
        if edition_2025 and row.key == "millenium":       # change for edition_2025
            y_box = y_position(row.row_y - 14) - 9
        # x_boxwidth = (end - start) * dots_year
        x_boxwidth = x_position(end) - x_position(start)
        if row.key == "millenium" and render_type == "print":
            x_boxwidth = x_position(end + 230) - x_position(start) 
        co = color[f"{row.key}"]
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.set_line_width(0.3)
        pdf.set_draw_color(0)
        if row.end_fade > row.end or row.start_fade < row.start:
            pdf.set_line_width(0.0)
            pdf.set_draw_color(1)
        shift = direction_factor
        stil = "F"
        if row.border:
            stil = "DF"
        pdf.rect(x_box, y_box - 1, x_boxwidth, 12, style=stil)
        if row.end_fade > row.end:                                              # fade end
            fade_width = x_position(row.end_fade) - x_position(row.end)
            x_boxwidth += fade_width
            fade_steps = 50
            for i in range(fade_steps):
                cl = faded_color(co[0], co[1], co[2], (i+1)/fade_steps)
                pdf.set_fill_color(cl[0]*255, cl[1]*255, cl[2]*255)
                pdf.rect(x_box + x_boxwidth - fade_width * (i+1)/fade_steps - 0.2 * shift, y_box - 1, fade_width / 45, 12, style="F")
        if row.start_fade < row.start:                                          # fade start
            fade_width = x_position(row.start) - x_position(row.start_fade)
            x_boxwidth += fade_width
            x_box = x_position(row.start_fade)
            fade_steps = 50
            for i in range(fade_steps):
                cl = faded_color(co[0], co[1], co[2], (i+1)/fade_steps)
                pdf.set_fill_color(cl[0]*255, cl[1]*255, cl[2]*255)
                pdf.rect(x_box + fade_width * i/fade_steps + 0.2 * shift, y_box - 1, fade_width / 45, 12, style="F")
        if len(row.text_center) > 1:
            detail_c = dict[row.text_center]
            textsize = fontsize_regular
            pdf.set_font(font_bold, "", textsize)
            pdf.set_text_color(255)
            while pdf.get_string_width(detail_c) > abs(x_boxwidth) and textsize > 4:
                textsize -= 1
                pdf.set_font(font_bold, "", textsize)
                print(textsize, " ", detail_c)
            drawString(detail_c, textsize, x_box + x_boxwidth * 0.5, y_box, "c", True)
        detail = dict[key]
        # y_box -= 8
        pdf.set_text_color(0)
        pdf.set_font(font_regular, "", fontsize_regular)
        if row.location_description == "l":
            drawString(detail, fontsize_regular, x_box - 2 * direction_factor, y_box , direction_rl, True)
        else:
            drawString(detail, fontsize_regular, x_box + x_boxwidth + 2*direction_factor, y_box, direction, True)
        counter_periods += 1

def create_caesars():
    global counter_kings, fontsize_regular
    # Import the persons with date of birth and death (estimated on October 1st) as pandas dataframe
    caesars = pd.read_csv("../db/caesars.csv", encoding='utf8')
    print("Imported data of caesars:", len(caesars))
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
        y_box  = y_position(row.row_y) - 10
        # x_boxwidth = (end -  start) * dots_year
        x_boxwidth = x_position(end) - x_position(start)                
        pdf.set_draw_color(0)
        pdf.set_line_width(0.3)
        pdf.line(x_born, y_box + 6, x_box,  y_box + 6)           # offset with fpdf2 is -3, was +3 with reportlab
        pdf.line(x_born, y_box + 1, x_born, y_box + 11)          # -3-5 = -8 and -3+5 = +2
        co = color['caesars']
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.rect(x_box, y_box, x_boxwidth, 12, style="FD")       # offset y_box was -3 - now its zero
        y_box += 1
        drawString(detail, fontsize_regular, x_box + x_boxwidth + 2 * direction_factor, y_box, direction, False)
        counter_kings += 1

def tribulation_graphics(row):
    global direction_factor
    reference_y = y_position(row)
    pdf.set_line_width(0)
    co = color["tribulation1"]
    pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
    pdf.rect(x_position(2030), reference_y, x_position(2035)-x_position(2030), 10, style="F") # box 2030-2035
    pdf.rect(x_position(2053), reference_y, x_position(2060)-x_position(2053), 10, style="F") # box 2053-2060
    for falter in range(3):
        xf = x_position(2035 + 6 * falter)
        yf = reference_y - 1.64
        d=direction_factor
        co = color["tribulation2"]
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        points = ((xf, yf+1.64), (xf + 1.64*d, yf+0), (xf + 1.64*d, yf+10), (xf, yf+11.64))
        pdf.polygon(points, style="F")
        co = color["tribulation3"]
        pdf.set_fill_color(co[0]*255, co[1]*255, co[2]*255)
        points = ((xf+3.30*d, yf+1.64), (xf + 1.64*d, yf+0), (xf + 1.64*d, yf+10), (xf+3.30*d, yf+11.64))
        pdf.polygon(points, style="F")

def create_tribulation():
    # draw the band above last days (24.1) and king of the south anglo-america (36)
    global fontsize_regular, direction_rl
    tribulation_lines = [23.25]     # this was 22.35 and 34.65 until 5.2 in 2025-02-05
    if edition_2025:
        tribulation_lines = [21.25]
    for row in tribulation_lines:
        pdf.set_text_color(0)
        pdf.set_font(font_regular, "", fontsize_regular)
        drawString(dict["tribulation"], fontsize_regular, x_position(2027), y_position(row), direction_rl, True)
        tribulation_graphics(row)

def create_terah_familytree():
    global counter_terahfam, direction_factor
    shift_x = 30 * direction_factor
    file_lines  = "../db/terah-lines.csv"
    file_family = "../db/terah-family.csv"
    if version > 4.8:
        file_lines  = "../db/terah-lines2.csv"
        file_family = "../db/terah-family2.csv"
    if version > 5.4:
        file_lines  = "../db/terah-lines3.csv"
        file_family = "../db/terah-family3.csv"
    lines = pd.read_csv(file_lines, encoding='utf8')        # lines in black and green
    shift_lines = -0.33
    for index, row in lines.iterrows():
        pdf.set_line_width(0.3)
        pdf.set_draw_color(0)
        if row.type == "married":
            pdf.set_line_width(1.0)
            pdf.set_draw_color(13, 155, 13)
        x_1 = x_position(-row.start) + shift_x
        y_1 = y_position(row.start_row + shift_lines)
        x_2 = x_position(-row.end) + shift_x
        y_2 = y_position(row.end_row + shift_lines)
        pdf.line(x_1, y_1, x_2, y_2)
    terah = pd.read_csv(file_family, encoding='utf8')      # text in blue and red on white boxes
    print(f"Imported family tree of Terah: {len(terah)} text fields")
    red  = color["terah_red"]
    blue = color["terah_blue"]
    for index, row in terah.iterrows():
        pdf.set_font(font_regular, "", 10)
        text_width = pdf.get_string_width(dict[row.key])
        x = x_position(-row.left) + shift_x
        y = y_position(row.row) - 9
        pdf.set_line_width(2.0)
        pdf.set_fill_color(255)
        pdf.set_draw_color(255)
        pdf.rect(x - 0.5 * text_width - 1, y, text_width + 2, 10, style = "FD")
        pdf.set_text_color(blue[0]*255, blue[1]*255, blue[2]*255)
        if row.color == "red":
            pdf.set_text_color(red[0]*255, red[1]*255, red[2]*255)
        drawString(dict[row.key], 10, x, y, "c", False)
        if version > 4.8:
            if row.sup > 0:
                pdf.char_vpos = "SUP"
                pdf.write(text=str(row.sup))
                pdf.char_vpos = "LINE"
    footnotes = pd.read_csv("../db/terah-footnotes.csv", encoding='utf8')
    pdf.set_text_color(0, 0, 0)
    for index, row in footnotes.iterrows():
        drawString(dict[row.key], 10, x_position(row.year), y_position(row.row), "r", False)
    counter_terahfam = 88

def include_pictures():
    global font_regular, direction, pdf
    pictures = pd.read_csv("../db/pictures.csv", encoding='utf8')
    print("Imported list of pictures:", len(pictures))
    pdf.set_font("Aptos", "", 5.9)
    pdf.set_text_color(0)
    for index, row in pictures.iterrows():
        location = "../images/" + row.key
        local_x = x_position(row.x)
        if row.year != "0":
            drawString(str(row.year), 5.9, local_x, y_position(row.y), direction, True)        
        if not left_to_right:
            local_x -= row.width*mm
        pdf.image(location, local_x, y_position(row.y) - row.height*mm - 0.4, row.width*mm, row.height*mm)

def include_pictures_svg():
    global font_regular, direction, pdf
    pictures_svg = pd.read_csv("../db/pictures_svg.csv", encoding='utf8')
    print("Imported list of SVG pictures:", len(pictures_svg))
    pdf.set_font("Aptos", "", 5.9)
    pdf.set_text_color(0)
    for index, row in pictures_svg.iterrows():
        location = "../images/" + row.key + ".svg"
        local_x = x_position(row.x)
        local_y = y_position(row.y)
        if row.key == "world_population":
            local_x += int(dict["daniel2_shift"])
            if version > 4.8:
                local_x = x_position(-4090)
                local_y = y_position(45.3)
        if row.fpdf2:    # only include the SVG images compatible with fpdf2, as indicated in csv
            if not edition_2025 or (edition_2025 and row.edition25):
                if row.year != 0:
                    drawString(str(row.year), 5.9, local_x, local_y - 1, direction, True)
                if not left_to_right:
                    local_x -= row.width
                pdf.image(location, local_x, local_y - row.height - 1.2, row.width, row.height)

    # text for world population graphic
    population_x = x_position(-3677) + int(dict["daniel2_shift"])
    population_y = 19
    if version > 4.8:
        population_x = x_position(-4075)
        population_y = 33
    pdf.set_text_color(25, 25, 160)
    pdf.set_font_size(4)
    drawString("source: https://www.worldometers.info/world-population/#table-historical", 4, population_x, y_position(population_y + 1), direction, False)
    population_color = color["world_population"]
    pdf.set_font(font_regular, "", 10)
    pdf.set_text_color(population_color[0]*255, population_color[1]*255, population_color[2]*255)
    drawString(dict["world_population"], 10, population_x, y_position(population_y) , direction, False)

def create_daniel2():                   # reference image has dimensions 748 x 240
    global font_regular, font_bold
    left_x = -4026
    shift_upward = 30*mm    
    if version > 4.8:
        left_x = -4075
        shift_upward = 70*mm
    d2_height = 96*mm
    d2_width  = d2_height / 748 * 240
    kingdoms = ["Babylon", "Medopersia", "Greece", "Rome", "Angloamerica"]
    kingdom_x = [0, 0, 0, 0, 0]
    years = ["607BCE", "", "539BCE", "537BCE", "", "331BCE", "", "63BCE", "70CE", "1914CE", "", ""] 
    yearlines = [2, 3, 2, 2, 3]
    current_yearline = 0
    image_shift = int(dict["daniel2_shift"])
    if daniel2_image == "_fiverr1":
        kingdom_x = [0, 0, 0, 0, -15]
    if daniel2_image == "_fiverr2":
        kingdom_x = [10, 0, 0, 0, -10]
    for index, kingdom in enumerate(kingdoms):
        pdf.set_line_width(0.4)
        co = color["daniel2"]
        pdf.set_draw_color(co[0]*255, co[1]*255, co[2]*255)
        y_line = y2 - shift_upward - d2_height * (0.91 - index * 0.212)
        pdf.line(x_position(left_x+226) + image_shift + kingdom_x[index], y_line, x_position(left_x), y_line)
        pdf.set_text_color(co[0]*255, co[1]*255, co[2]*255)
        pdf.set_font(font_bold, "", 12)
        drawString(dict[kingdom + "_c"], 12, x_position(left_x), y_line + 2, direction, False)
        pdf.set_text_color(50)
        pdf.set_font(font_regular, "", 8)
        drawString(dict[kingdom], 8, x_position(left_x), y_line + 15.4, direction, False)
        if years[current_yearline] != "":
            current_yearstring = dict[years[current_yearline]]
        pdf.set_font(font_regular, "", 6)
        indentation = pdf.get_string_width(current_yearstring) + 3
        for yearline in range(yearlines[index]):
            yearstring = " "
            if years[current_yearline] != "":
                yearstring = dict[years[current_yearline]]
            drawString(yearstring, 6, x_position(left_x), y_line + 25.2 + 8 * yearline, direction, False)
            line_daniel2 = "daniel2_" + str(current_yearline+1)
            drawString(dict[line_daniel2], 6, x_position(left_x) + indentation*direction_factor, y_line + 25.2 + 8 * yearline, direction, False)
            current_yearline += 1
    file_d2 = "../images/daniel2" + daniel2_image
    # if daniel2_nwt:
    #     file_d2 += "_nwt"
    d2_x = x_position(left_x+176) + image_shift * direction_factor
    if not left_to_right:
        file_d2 += "_rtl"
        d2_x -= d2_width
    pdf.image(file_d2 + ".svg", x = d2_x, y = y2 - shift_upward - d2_height, w = d2_width , h = d2_height)

def create_timestamp():
    qr_x = -4026
    qr_y = 6.1
    if version < 4.8:
        timestamp_details = ["people", "judges", "prophets", "kings", "periods", "events", "objects", "terahfam"]
        for index, detail in enumerate(timestamp_details):
            drawString(f"{dict[detail]}", 4, x_position(-4075) + 6 * direction_factor, y2 - 42 + 4.5 * index, direction, False)
        for index, detail in enumerate(timestamp_details):
            counter_detail = str(eval("counter_" + detail))
            counter_detail = number_to_string(counter_detail, language)
            drawString(counter_detail, 4, x_position(-4075) + 5.4 * direction_factor, y2 - 42 + 4.5 * index, direction_rl, False)
    else:
        qr_x = -4075
        qr_y = 3.8
    pdf.set_font("Aptos", "", 4)
    pdf.set_text_color(50)
    pdf.set_text_shaping(use_shaping_engine=True, language="eng")
    info_width = pdf.get_string_width(f"Timeline {version} – created {str(datetime.datetime.now())[0:16]} – {pdf_author} – license: MIT – some images are CC BY-SA")
    if left_to_right:
        info_width = 0
    pdf.set_xy(x_position(-4075) - info_width, y2 - 6)
    pdf.cell(text=f"Timeline {version} – created {str(datetime.datetime.now())[0:16]} – ")
    pdf.set_text_color(25, 25, 150)
    pdf.cell(text=f"{pdf_author}", link="https://kreier.github.io/timeline/")
    pdf.set_text_color(50)
    pdf.cell(text=" – license: MIT – some ")
    pdf.set_text_color(25, 25, 150)
    pdf.cell(text="images", link="https://github.com/kreier/timeline/blob/main/images/images_source.csv")
    pdf.set_text_color(50)
    pdf.cell(text=" are ")
    pdf.set_text_color(25, 25, 150)
    pdf.cell(text="CC BY-SA", link="https://creativecommons.org/licenses/by-sa/4.0/")

    qr_file = "../images/qr-" + language + ".png"
    if edition_2025:
        qr_file = "../images/qr-" + language + "25.png"
    qr_size = 15*mm
    if os.path.exists(qr_file):
        if left_to_right:
            pdf.image(qr_file, x_position(qr_x), y_position(qr_y), qr_size, qr_size)
        else:
            pdf.image(qr_file, x_position(qr_x) - qr_size, y_position(qr_y), qr_size, qr_size)
        pdf.set_font_size(4.5)
        pdf.set_text_color(30)
        timestamp = str(datetime.datetime.now())
        dateindex = timestamp[2:4] + timestamp[5:7] + timestamp[8:10]
        rotation_angle = -90
        rotation_y = y_position(qr_y + 0.1)
        if left_to_right:
            rotation_angle = 90
            rotation_y += qr_size * 0.94
        with pdf.rotation(angle=rotation_angle, x=x_position(qr_x), y=rotation_y):
            pdf.set_xy(x_position(qr_x), y_position(qr_y + 0.2) + qr_size * (1.47 + 0.47 * direction_factor))
            pdf.cell(text="timeline " + language)
            pdf.set_xy(x_position(qr_x), y_position(qr_y + 0.58) + qr_size * (1.47 + 0.47 * direction_factor))
            pdf.cell(text=dateindex)

def render_to_file():
    global pdf, filename
    pdf.output(filename)
    print(f"File exported: {filename}")

def create_timeline(lang, edition):
    global language
    language = lang
    initiate_counters()
    import_dictionary()
    import_colors("normal")
    create_canvas(edition)
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
    create_tribulation()
    create_terah_familytree()
    include_pictures()
    include_pictures_svg()
    create_daniel2()
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
    number_characters = 0                   # you can translate up to 500,000 characters per month for free
    for index, row in dict.iterrows():      # with 3 columns 'key' 'text' and 'english'
        english_text = row.english
        number_characters += len(english_text)
        if not english_text == " ":  # it only applies to row 9 where in english is an empty string (unline Vietnamese or Russian)
            dict.at[index, 'text'] = translator.translate(english_text, src='en', dest=language).text
            print('.', end='')
        if (index + 1) % 40 == 0:
            print(f" {index}")
    print(dict)
    print("Exporting ...")
    dict.to_csv(filename, index=False)
    print(f"You translated {number_characters} characters.")

def is_supported(language):
    global language_str
    # import list of supported languages into dataframe supported_language
    df = pd.read_csv("../db/supported_languages.csv", encoding='utf8')
    df = df.fillna(" ")
    row_index = df[df['key'] == language].index   # creates array of matching entries with language string
    if len(row_index) == 0:
        print(f"Your selected language '{language}' is not yet supported by this timeline project.\n")
        print(f"Let's check if the language code exists in Google Translate: ", end = "")
        isValid = checkForValidLanguageCode(language)
        if isValid:
            print(f"Found {language_str}.")
            print(f"Now creating a new dictionary in this language with Google Translate.")
            create_dictionary(language)
            return True
        else:
            print(f"Nope.\nIt looks like '{language}' is not a valid language code in ISO 639 or it is not supported by Google Translate.")
            return False
    else:
        language_str = df.at[row_index[0], 'language_str'] # language is used for the shape engine
        print(f"Your selected language {language} is supported: {language_str}")
        return True

if __name__ == "__main__":
    print(f"Timeline v{version}") # parameters are language, image Daniel 2 and 2025 edition
    if len(sys.argv) < 2:
        print("You did not provide a language as argument. Put it as a parameter after fpdf2_6000.py")
        exit()
    language = sys.argv[1]
    if len(sys.argv) > 2:
        daniel2_image = sys.argv[2]
    if len(sys.argv) > 3:
        if sys.argv[3] == "2025":
            edition_2025 = True
    if is_supported(language):
        create_timeline(language, "digital")
        create_timeline(language, "print")
