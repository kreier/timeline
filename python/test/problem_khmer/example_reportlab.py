# example rendering in Khmer
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Khmer", '../../fonts/NotoKhmer.ttf'))
my_canvas = canvas.Canvas("example_reportlab.pdf")
my_canvas.setFont("Khmer", 32)
my_canvas.drawString(72, 749, "King         - ស្តេច")
my_canvas.drawString(72, 713, "Prophet  - ហោរា") 
my_canvas.save()
