# minimal_khmer.py hello world!
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('noto_khmer', '../fonts/NotoKhmer.ttf'))
my_canvas = canvas.Canvas("minimal_khmer.pdf")
my_canvas.setFont('noto_khmer', 36)        # one inch would be 72 points
my_canvas.drawString(56.7, 785.3-36, "ស្ស") # 2cm = 56.7 pt left and top
my_canvas.save()
