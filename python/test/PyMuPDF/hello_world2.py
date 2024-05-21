import pymupdf  # PyMuPDF
from fontTools import subset
from fontTools.ttLib import TTFont

# Create a new PDF
pdf_document    = pymupdf.open()
khmer_font_path = "../../Fonts/NotoKhmer.ttf"
pdf_file_name   = "hello_world2.pdf"

# Define the Unicode range for Khmer glyphs
khmer_unicode_range = range(0x1780, 0x1800)

# Convert the Unicode range to a string of characters
khmer_characters = ''.join(chr(code_point) for code_point in khmer_unicode_range)

options = subset.Options()
# options.set(layoutFeatures=['liga', 'kern'])  
# options.set(text='Hello World!')
# Set the text option to the Khmer characters
# options.set(text=khmer_characters)

font = subset.load_font(khmer_font_path, options)
subsetter = subset.Subsetter(options)
subsetter.populate(text=khmer_characters)
# subsetter.populate(unicodes=["U+1780", "U+1800"])  # replace with the unicode values you need
subsetter.subset(font)

# Add a page
page = pdf_document.new_page()
page = pdf_document[0]  # load the page you want to insert the font into
page.insert_font(fontname="F0", fontfile=khmer_font_path)

page.insert_text((72,72), "Hello world ស្ស", fontname="F0", fontsize=14)

pdf_document.save(pdf_file_name, garbage=4, deflate=True)
pdf_document.close()

print(f"PDF {pdf_file_name} created successfully!")
