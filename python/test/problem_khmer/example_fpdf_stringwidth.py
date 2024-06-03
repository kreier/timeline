# example rendering Khmer
from fpdf import FPDF
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.c_margin = 0
pdf.add_font("noto", style="", fname="../../fonts/NotoKhmer.ttf")
# teststring = ["ពុម្ពអក្សរស្មុគស្មាញ", "គឺជាលក្ខណៈ", "នៃភាសាខ្មែរ។"]
# teststring = ["អំរី (​ម្នាក់​ឯង​)", "យេរ៉ូបោម", "យ៉ូសៀស"]
teststring = ["ស៊ីមរី (៧ ថ្ងៃ)", "អេឡា (២ ឆ្នាំ)", "អំរី ( ម្នាក់ ឯង )  (៨ ឆ្នាំ)"]
pdf.set_font("noto", size=12)
pdf.cell(text="The following text consists of three cells. We determine the width before and after rendering.")
pdf.ln()

pdf.set_font('noto', size=24)
teststringlength = []
teststringlength_measured = []
for i in range(len(teststring)):
    teststringlength.append(pdf.get_string_width(teststring[i]))
    start = pdf.get_x()
    pdf.cell(h=17, text=teststring[i])
    end = pdf.get_x()
    pdf.cell(h=17, text="—")
    teststringlength_measured.append(end - start)
pdf.ln()
pdf.set_font("noto", size=12)
for i in range(len(teststringlength)):
    pdf.cell(text=f"Before: {teststringlength[i]}  -  after: {teststringlength_measured[i]}")
    pdf.ln()
pdf.ln()

pdf.cell(text="Now activating the shape engine and try this again:")
pdf.ln()
pdf.set_text_shaping(use_shaping_engine=True, script="khmr", language="khm")

pdf.set_font('noto', size=24)
teststringlength = []
teststringlength_measured = []
for i in range(len(teststring)):
    teststringlength.append(pdf.get_string_width(teststring[i]))
    start = pdf.get_x()
    pdf.cell(h=17, text=teststring[i])
    end = pdf.get_x()
    pdf.cell(h=17, text="—")
    teststringlength_measured.append(end - start)
pdf.ln()
pdf.set_font("noto", size=12)
for i in range(len(teststringlength)):
    pdf.cell(text=f"Before: {teststringlength[i]}  -  after: {teststringlength_measured[i]}")
    pdf.ln()
pdf.ln()

pdf.c_margin = 1
pdf.set_font('noto', size=24)
for i in range(len(teststring)):
    pdf.cell(text=teststring[i])
    pdf.cell(text="—")
pdf.ln()
pdf.cell(h=17, text=teststring[0]+"—"+teststring[1]+"—"+teststring[2]+"—")

pdf.output("example_fpdf2_strignwidth.pdf")
