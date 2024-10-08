# example rendering Sinhala
from fpdf import FPDF
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.add_font("noto", style="", fname="../../fonts/NotoSinhala.ttf")
pdf.set_font('noto', size=32)
pdf.cell(text="Conference - සමුළුව", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=12)
pdf.cell(h = 20,text="Now using __text_shaping__ with **uharfbuzz**:", markdown=True, new_x="LMARGIN", new_y="NEXT")
pdf.set_font("noto", size=32)
pdf.set_text_shaping(use_shaping_engine=True, script="khmr", language="khm")
pdf.cell(text="Conference - සමුළුව", new_x="LMARGIN", new_y="NEXT")
pdf.output("example_fpdf.pdf")
