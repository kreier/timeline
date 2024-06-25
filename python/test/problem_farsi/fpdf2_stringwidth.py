from fpdf import FPDF
fontname = ["NotoArabic.ttf", "Amiri-Regular.ttf"]
# strings:     judges  prophets
teststrings = ["قضات", "پیامبران"]

def right_align(teststrings, more_text):
    pdf.set_draw_color(180)
    pdf.set_line_width(0.3)
    for string in teststrings:
        if more_text:
            pdf.cell(text="Hello world!")               # this throws string_width off!
        # pdf.set_text_shaping(use_shaping_engine=True, script="arab", language="far")
        pdf.set_font('font', size=24)
        pdf.set_x(120 - pdf.get_string_width(string))
        print(f"{pdf.get_string_width(string):.2f} {string}    ", end="")
        pdf.rect(pdf.get_x(), pdf.get_y() + 2.2, pdf.get_string_width(string), 11, style="D")
        pdf.cell(h=13, text=string + " ")
        pdf.ln()
    print(" ")

for typeface in fontname:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.c_margin = 0
    pdf.add_font("font", style="", fname="../../fonts/" + typeface)
    print(typeface)
    right_align(teststrings, False)
    pdf.set_text_shaping(use_shaping_engine=True, script="arab", language="far")
    right_align(teststrings, False)
    right_align(teststrings, True)
    pdf.output("fpdf2_stringwidth" + typeface + ".pdf")
