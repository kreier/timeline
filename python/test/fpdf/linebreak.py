from fpdf import FPDF

pdf = FPDF(unit="pt", format="A4")
pdf.set_margin(0)
pdf.add_page()
pdf.set_font("Helvetica", size=12)
pdf.set_xy(20, 20)
pdf.multi_cell(95, text="This is just a test to see if the linebreak automatically kicks in.", new_y="NEXT", align="L", new_x="LMARGIN")
pdf.cell(text="one more line", new_x="LMARGIN", new_y="NEXT")
pdf.output("linebreak.pdf")

print("PDF created successfully!")
