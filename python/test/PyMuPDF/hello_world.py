import pymupdf  # PyMuPDF

# Create a new PDF
pdf_document = pymupdf.open()

# Add a page
page = pdf_document.new_page()

# Set text
text = "Hello, World!  ស្ស"

# Define the position and insert text
page.insert_text((72, 72), text, fontsize=12)

# Save the PDF
pdf_document.save("hello_world.pdf")
pdf_document.close()

print("PDF created successfully!")
