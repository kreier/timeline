from fpdf import FPDF
fontname = ["NotoKhmer.ttf", "Khmer-Regular.ttf", "Moul-Regular.ttf", "Battambang-Regular.ttf", 
            "Preahvihear-Regular.ttf", "Siemreap-Regular.ttf",
            "NotoSansKhmer-Regular.ttf", "NotoSansKhmer-Regular.otf", "NotoSansKhmerUI-Regular.ttf", 
            "NotoSansKhmerUI-Regular.otf", "NotoSansKhmerUI-Regular1.ttf", "NotoSansKhmerUI-Regular1.otf",
            "NotoSansKhmer-RegularDev.ttf", "NotoSerifKhmer-Regular.ttf"]
# strings:    years,  alone,    1st year, sword,  fork
teststrings = ["ឆ្នាំ", "ម្នាក់ ឯង", "ឆ្នាំទី១", "ដង្កាវ", "ង្គ្រា"]

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

for typeface in fontname:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.c_margin = 0
    pdf.add_font("noto", style="", fname="../../fonts/" + typeface)
    info("Rendering without shape engine:")
    render_strings(teststrings)
    info("Now activating the shape engine and try this again:")
    pdf.set_text_shaping(use_shaping_engine=True, script="khmr", language="khm")
    render_strings(teststrings)
    render_strings([''.join(teststrings)])     
    pdf.output("fpdf2_stringwidth" + typeface + ".pdf")
