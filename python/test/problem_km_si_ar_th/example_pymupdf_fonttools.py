import pymupdf  # no more fitz
from fontTools import subset
from fontTools.ttLib import TTFont

pdf_file_name   = "example_pymupdf_fontools.pdf"
matrix = [["Khmer", "King Prophet", "ស្តេច ហោរា"],
          ["Sinhala", "Conference", "සමුළුව"]]

pdf_document = pymupdf.open()      # Create a new PDF
page = pdf_document.new_page()        # Add a page
page = pdf_document[0]

for i in range(len(matrix)):
    page.insert_font(fontname=matrix[i][0], fontfile='../../fonts/Noto' + matrix[i][0] + '.ttf')
    page.insert_text((72, 72+90*i), f"Language {matrix[i][0]}:", fontname=matrix[i][0], fontsize=32)
    page.insert_text((72, 108+90*i), f"Word '{matrix[i][1]}' - {matrix[i][2]}", fontname=matrix[i][0], fontsize=32)

pdf_document.save(pdf_file_name, garbage=4, deflate=True)
pdf_document.close()

'''
khmer_unicode_range = range(0x1780, 0x1800)
khmer_characters = ''.join(chr(code_point) for code_point in khmer_unicode_range)
options = subset.Options()
# options.set(layoutFeatures=['liga', 'kern'])  
# options.set(text='Hello World!')
# options.set(text=khmer_characters)

font = subset.load_font(khmer_font_path, options)
subsetter = subset.Subsetter(options)
subsetter.populate(text=khmer_characters)
# subsetter.populate(unicodes=["U+1780", "U+1800"])  # replace with the unicode values you need
subsetter.subset(font)
'''
