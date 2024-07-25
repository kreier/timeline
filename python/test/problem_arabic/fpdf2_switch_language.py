from fpdf import FPDF
fontname = ["NotoArabic.ttf"]
# fontname = ["NotoArabic.ttf", "Amiri-Regular.ttf", "IBMPlexSansArabic-Regular.ttf"]
# strings:     prophets    kings     periods   events    Abraham     book
teststrings = ["الملوك", "الملوك", "test", "الملوك", "الملوك", "الملوك", "test", "الملوك", "test"]

def render_strings(teststrings):
    pdf.set_font('noto', size=24)
    pdf.set_draw_color(160)
    pdf.set_line_width(0.3)
    for string in teststrings:
        pdf.set_text_shaping(use_shaping_engine=True, script="arab", language="ara")
        pdf.set_x(110 - pdf.get_string_width(string))
        pdf.rect(pdf.get_x(), pdf.get_y()+2, pdf.get_string_width(string), 13, style="D")
        pdf.cell(h=17, text=string)
        pdf.ln()
    pdf.ln()

for typeface in fontname:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.c_margin = 0
    pdf.add_font("noto", style="", fname="../../fonts/" + typeface)
    pdf.set_text_shaping(use_shaping_engine=True, script="arab", language="ara")
    render_strings(teststrings)
    pdf.output("fpdf2_switch_language" + typeface + ".pdf")
