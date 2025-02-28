from fpdf import FPDF
fontfile = "../../fonts/NotoArabic.ttf"
teststring = "أصبحت ويكيبيديا الآن متاحة بـ 342 لغة." # "Wikipedia is now available in 342 languages."

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.c_margin = 0
pdf.add_font("noto", style="", fname=fontfile)
pdf.set_font('noto', size=24)
pdf.cell(h=17, text=teststring)
pdf.ln()
pdf.set_text_shaping(use_shaping_engine=True, script="arab", language="ara")
pdf.cell(h=17, text=teststring)
pdf.output("wikipedia_fpdf2.pdf")
