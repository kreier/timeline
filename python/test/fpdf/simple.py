from fpdf import FPDF

pdf = FPDF(unit="pt", format="A4")
pdf.set_margin(0)
pdf.add_page()
pdf.set_font("Helvetica", size=12)
for i in range(68):
    pdf.set_xy(0, i*12)
    pdf.cell(text="Hello, World!")
pdf.cell(text="one more line", new_x="LMARGIN", new_y="NEXT")
pdf.cell(text="one more line", new_x="LMARGIN", new_y="NEXT")
pdf.cell(text="one more line", new_x="LMARGIN", new_y="NEXT")
pdf.cell(text="one more line", new_x="LMARGIN", new_y="NEXT")
pdf.output("simple.pdf")

print("PDF created successfully!")
