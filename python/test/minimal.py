# minimal.py hello world!
from reportlab.pdfgen import canvas
my_canvas = canvas.Canvas("minimal.pdf")
my_canvas.drawString(100, 750, "Hello world!")
my_canvas.save()
