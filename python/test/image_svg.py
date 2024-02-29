# minimal.py hello world!
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF, renderPM
from reportlab.platypus import SimpleDocTemplate
from svglib.svglib import svg2rlg
# renderPDF.drawToFile(drawing, "image_daniel.pdf")

c = canvas.Canvas("image_svg.pdf")
c.drawString(100, 750, "Hello world!")
drawing = svg2rlg("daniel2.svg")
factor = 0.5
sx = sy = factor
drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
drawing.scale(sx, sy)
renderPDF.draw(drawing, c, 0, 40)
c.save()
