# use arabic script with reportlab

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

# fontname = ["NotoArabic.ttf", "Amiri-Regular.ttf", "IBMPlexSansArabic-Regular.ttf"]
fontname = ["NotoArabic.ttf"]

# strings:     prophets    kings     periods   events    Abraham     book
teststrings = ["الأنبياء", "الملوك", "فترات", "الأحداث", "إبْرَاهِيم", "كتاب"]

def render_strings(teststrings):
    global text_x, text_y
    fontsize = 24
    text_y -= fontsize + 6
    c.setFont("testfont", fontsize)
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.setLineWidth(0.3*mm)
    for string in teststrings:
        c.rect(text_x, text_y - 12, stringWidth(string, "testfont", fontsize), fontsize + 12, fill=0)
        c.drawString(text_x, text_y, string)
        text_x += stringWidth(string, "testfont", fontsize) + 6
    text_x = 28
    text_y -= 12

def info(text):
    global text_y
    text_y -= 12
    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, text)

for typeface in fontname:
    pdfmetrics.registerFont(TTFont('testfont', "../../fonts/" + typeface))
    filename = "reportlab_stringwidth." + typeface + ".pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    text_x = 28           # ca 10 mm from left
    text_y = 297*mm - 27
    info("Rendering without shape engine:")
    render_strings(teststrings)
    info("Now activating the shape engine and try this again:")
    render_strings(teststrings)
    render_strings([''.join(teststrings)])
    render_strings(["عمَّد يسوع في خريف سنة ٢٩ بم"])
    fontsize = 24
    for string in teststrings:
        text_y -= fontsize + 18
        text_x = 110*mm - stringWidth(string, "testfont", fontsize)
        c.rect(text_x, text_y - 12, stringWidth(string, "testfont", fontsize), fontsize + 12, fill=0)
        c.drawString(text_x, text_y, string)

    c.showPage()
    c.save()
    # print(f"File exported: {filename}")
