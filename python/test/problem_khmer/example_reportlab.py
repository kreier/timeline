# example rendering in some languages
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
matrix = [["Khmer", "King Prophet", "ស្តេច ហោរា"],
          ["Sinhala", "Conference", "සමුළුව"]]
my_canvas = canvas.Canvas("example_reportlab.pdf")
for i in range(len(matrix)):
    pdfmetrics.registerFont(TTFont(matrix[i][0], '../../fonts/Noto' + matrix[i][0] + '.ttf'))
    my_canvas.setFont(matrix[i][0], 32)
    my_canvas.drawString(72, 749-90*i, f"Language {matrix[i][0]}:")
    my_canvas.drawString(72, 713-90*i, f"Word '{matrix[i][1]}' - {matrix[i][2]}") 
my_canvas.save()
