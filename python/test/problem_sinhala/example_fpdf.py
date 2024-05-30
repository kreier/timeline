# example rendering Khmer
from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.add_font("noto", style="", fname="../../fonts/NotoKhmer.ttf")
pdf.set_font('noto', size=30)
pdf.cell(text="King        - ស្តេច")
pdf.ln()
pdf.cell(text="Prophet - ហោរា")
pdf.output("example_fpdf.pdf")
