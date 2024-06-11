from fpdf import FPDF
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.c_margin = 0
# pdf.add_font("noto", style="", fname="../../fonts/NotoKhmer.ttf")
pdf.add_font("noto", style="", fname="../../fonts/Khmer-Regular.ttf")
# strings:    years,  alone,    1st year, sword,  fork, objects
teststrings = ["ឆ្នាំ", "ម្នាក់ ឯង", "ឆ្នាំទី១", "ដង្កាវ", "ង្គ្រា", "វត្ថុ"]

def render_strings(teststrings):
    pdf.set_font('noto', size=24)
    pdf.set_draw_color(160)
    pdf.set_line_width(0.3)
    for string in teststrings:
        pdf.rect(pdf.get_x(), pdf.get_y()+2, pdf.get_string_width(string), 13, style="D")
        pdf.cell(h=17, text=string + " ")
    pdf.ln()

def info(text):
    pdf.set_font("Helvetica", size=12)
    pdf.cell(text=text)
    pdf.ln()

info("Rendering without shape engine:")
render_strings(teststrings)

info("Now activating the shape engine and try this again:")
pdf.set_text_shaping(use_shaping_engine=True, script="khmr", language="khm")
render_strings(teststrings)

render_strings([''.join(teststrings)])     # These two lines are the same, just for comparison
# pdf.cell(h=17, text=''.join(teststrings))  # and having a box around the rendered string
pdf.output("fpdf2_stringwidth.pdf")
