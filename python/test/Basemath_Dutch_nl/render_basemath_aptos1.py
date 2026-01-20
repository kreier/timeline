from PIL import Image, ImageDraw, ImageFont

# Text to render
text = "Ba̱smath"

# Load the font (adjust size as needed)
# font_path = "../../fonts/aptos.ttf"
# font_path = "../../fonts/noto.ttf"
font_path = "../../fonts/Aptos-Display.ttf"
font_size = 72
font = ImageFont.truetype(font_path, font_size)

# Create a blank image with white background
# Size is estimated based on text length
img = Image.new("RGB", (400, 200), color="white")

# Draw text
draw = ImageDraw.Draw(img)
draw.text((50, 50), text, font=font, fill="black")

# Save to PNG
img.save("output.png")
print("Saved output.png")
