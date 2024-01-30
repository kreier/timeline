# hello_reportlab.py
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 1
from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('Aptos', '../aptos.ttf',subfontIndex=0,asciiReadable=0))

my_canvas = canvas.Canvas("test-reportlab.pdf")
my_canvas.setFont('Aptos', 16)

my_canvas.drawString(100, 750, "Welcome to Reportlab!")
my_canvas.drawString(100, 730, "How about Japanese? これは日本語のテキストです。".encode('utf8'))
my_canvas.drawString(100, 710, "How about Chinese? 这是一篇中文文本。")
my_canvas.drawString(100, 690, "How about Korean? 한국어로 된 글입니다.")
my_canvas.drawString(100, 670, "How about Taiwanese? 這是台灣文字。")
my_canvas.save()
