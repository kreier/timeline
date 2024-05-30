# import pymupdf  # no more fitz
# from fontTools import subset
# from fontTools.ttLib import TTFont

# pdf_file_name   = "example_pymupdf_fontools.pdf"
# matrix = [["Khmer", "King Prophet", "ស្តេច ហោរា"],
#           ["Sinhala", "Conference", "සමුළුව"]]

# pdf_document = pymupdf.open()      # Create a new PDF
# page = pdf_document.new_page()        # Add a page
# page = pdf_document[0]

# for i in range(len(matrix)):
#     page.insert_font(fontname=matrix[i][0], fontfile='../../fonts/Noto' + matrix[i][0] + '.ttf')
#     page.insert_text((72, 93+90*i), f"Language {matrix[i][0]}:", fontname=matrix[i][0], fontsize=32)
#     page.insert_text((72, 129+90*i), f"Word '{matrix[i][1]}' - {matrix[i][2]}", fontname=matrix[i][0], fontsize=32)

# pdf_document.save(pdf_file_name, garbage=4, deflate=True)
# pdf_document.close()

import pymupdf  # no more fitz
from fontTools import subset
from fontTools.ttLib import TTFont
pdf_file_name   = "example_pymupdf_fonttools.pdf"
pdf_document = pymupdf.open()         # Create a new PDF
page = pdf_document.new_page()        # Add a page
page = pdf_document[0]
page.insert_font(fontname="sinhala", fontfile='../../fonts/NotoSinhala.ttf')
page.insert_text((72, 93),  f"Conference - සමුළුව", fontname="sinhala", fontsize=32)
pdf_document.save(pdf_file_name, garbage=4, deflate=True)
pdf_document.close()
