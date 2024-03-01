# minimal.py hello world!
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF, renderPM
from reportlab.platypus import SimpleDocTemplate
from svglib.svglib import svg2rlg
# renderPDF.drawToFile(drawing, "image_daniel.pdf")

c = canvas.Canvas("image_svg.pdf")
c.drawString(100, 750, "Hello world!")
drawing = svg2rlg("daniel2.svg")
desired_height = 500
factor = desired_height / drawing.height
print(f"The width of your drawing is: {drawing.width} and the height is {drawing.height}.")
sx = sy = factor
drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
drawing.scale(sx, sy)
print(f"The width of your drawing is: {drawing.width} and the height is {drawing.height}.")
renderPDF.draw(drawing, c, 0, 40)
c.save()
