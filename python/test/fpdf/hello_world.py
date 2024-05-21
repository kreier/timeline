from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size=12)

# Add a cell
pdf.cell(200, 10, txt="Hello, World!", ln=True, align='C')

# Save the PDF with name .pdf
pdf.output("hello_world.pdf")

print("PDF created successfully!")
