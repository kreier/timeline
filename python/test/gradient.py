# example.py 
from reportlab.pdfgen import canvas
red = (1, 0, 0)
green = (0, 1, 0)
my_canvas = canvas.Canvas("gradient.pdf")
my_canvas.drawString(30, 800, "Add a box with a color gradient")
p = my_canvas.beginPath()
p.rect(30, 650, 100, 100, fill=1)
# my_canvas.rect(30, 650, 100, 100, stroke=1, fill=1)
my_canvas.linearGradient(30,500,130,600,(red, green), extend=False)

my_canvas.save()
