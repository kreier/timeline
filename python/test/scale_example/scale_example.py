from fpdf import FPDF

SCALE = 10

pdf = FPDF(unit="mm", format=(13080, 2970))
pdf.add_page()

def sx(x):
    return x / SCALE

def sy(y):
    return y / SCALE

# draw a line with high internal precision
pdf.line(sx(0), sy(0), sx(13080), sy(2970))

pdf.set_xy(sx(1000), sy(1000))
pdf.set_font("Helvetica", size=12)
pdf.cell(0, 10, "High precision text")

pdf.output("high_zoom.pdf")
