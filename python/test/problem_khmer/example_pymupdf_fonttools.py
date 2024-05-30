import pymupdf  # no more fitz
from fontTools import subset
from fontTools.ttLib import TTFont
pdf_file_name   = "example_pymupdf_fontools.pdf"
pdf_document = pymupdf.open()      # Create a new PDF
page = pdf_document.new_page()        # Add a page
page = pdf_document[0]
page.insert_font(fontname="khmer", fontfile='../../fonts/NotoKhmer.ttf')
page.insert_text((72, 93),  f"King         - ស្តេច", fontname="khmer", fontsize=32)
page.insert_text((72, 129), f"Prophet   - ហោរា", fontname="khmer", fontsize=32)
pdf_document.save(pdf_file_name, garbage=4, deflate=True)
pdf_document.close()
