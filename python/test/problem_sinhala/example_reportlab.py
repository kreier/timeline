# example rendering in Sinhala
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Sinhala", '../../fonts/NotoSinhala.ttf'))
my_canvas = canvas.Canvas("example_reportlab.pdf")
my_canvas.setFont("Sinhala", 32)
my_canvas.drawString(72, 749, "Conference - සමුළුව")
my_canvas.save()
