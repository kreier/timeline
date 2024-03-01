# example.py 
from reportlab.pdfgen import canvas
red   = (1, 0, 0)
green = (0, 1, 0)
blue  = (0, 0, 1)
my_canvas = canvas.Canvas("gradient.pdf")
my_canvas.drawString(30, 800, "Add a box with a color gradient")
p = my_canvas.beginPath()
p.rect(30, 650, 100, 100)
my_canvas.clipPath(p, stroke=0, fill=1)
my_canvas.linearGradient(30,650,130,750,(red, green), extend=False)

all = my_canvas.beginPath()
all.rect(0, 0, 300, 800)
my_canvas.clipPath(all, stroke=1)

my_canvas.setFillColor(blue)
my_canvas.rect(30, 500, 100, 100, stroke=1, fill=1)

my_canvas.drawImage('./daniel2.jpg', 250, 400, width=50, height=200, mask=None)

my_canvas.save()
