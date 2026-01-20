from PIL import Image, ImageDraw, ImageFont

# Text to render
main_text = "Ba̱smath, Te̱rah and Me·thuʹse·lah"

# Font sizes
main_font_size = 72
header_font_size = main_font_size // 2

# Load fonts
aptos_font = ImageFont.truetype("../../fonts/aptos.ttf", main_font_size)
aptos_header_font = ImageFont.truetype("../../fonts/aptos.ttf", header_font_size)

noto_font = ImageFont.truetype("../../fonts/NotoSans.ttf", main_font_size)
noto_header_font = ImageFont.truetype("../../fonts/NotoSans.ttf", header_font_size)

segoe_font = ImageFont.truetype("../../fonts/segoeuithis.ttf", main_font_size)
segoe_header_font = ImageFont.truetype("../../fonts/segoeuithis.ttf", header_font_size)

# PowerShell default font (Consolas)
consolas_font = ImageFont.truetype("consola.ttf", main_font_size)   # system font
consolas_header_font = ImageFont.truetype("consola.ttf", header_font_size)

# Prepare headers
aptos_header = f"Font used: {aptos_font.getname()[0]}"
noto_header = f"Font used: {noto_font.getname()[0]}"
segoe_header = f"Font used: {segoe_font.getname()[0]}"
consolas_header = f"Font used: {consolas_font.getname()[0]}"

# Measure sizes
temp_img = Image.new("RGB", (1, 1))
draw = ImageDraw.Draw(temp_img)

def measure_section(header_text, header_font, main_text, main_font):
    header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    main_bbox = draw.textbbox((0, 0), main_text, font=main_font)
    width = max(header_bbox[2]-header_bbox[0], main_bbox[2]-main_bbox[0])
    height = (header_bbox[3]-header_bbox[1]) + (main_bbox[3]-main_bbox[1]) + 40
    header_h = header_bbox[3] - header_bbox[1]
    return width, height, header_h

aptos_w, aptos_h, aptos_header_h = measure_section(aptos_header, aptos_header_font, main_text, aptos_font)
noto_w, noto_h, noto_header_h = measure_section(noto_header, noto_header_font, main_text, noto_font)
segoe_w, segoe_h, segoe_header_h = measure_section(segoe_header, segoe_header_font, main_text, segoe_font)
consolas_w, consolas_h, consolas_header_h = measure_section(consolas_header, consolas_header_font, main_text, consolas_font)

# Final image size
width = max(aptos_w, noto_w, segoe_w, consolas_w) + 20
height = aptos_h + noto_h + segoe_h + consolas_h + 120  # spacing between sections

# Create final image
img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

# Draw Aptos section
y = 10
draw.text((10, y), aptos_header, font=aptos_header_font, fill="black")
draw.text((10, y + aptos_header_h + 20), main_text, font=aptos_font, fill="black")

# Draw NotoSans section
y += aptos_h + 30
draw.text((10, y), noto_header, font=noto_header_font, fill="black")
draw.text((10, y + noto_header_h + 20), main_text, font=noto_font, fill="black")

# Draw Segoe UI This section
y += noto_h + 30
draw.text((10, y), segoe_header, font=segoe_header_font, fill="black")
draw.text((10, y + segoe_header_h + 20), main_text, font=segoe_font, fill="black")

# Draw Consolas section
y += segoe_h + 30
draw.text((10, y), consolas_header, font=consolas_header_font, fill="black")
draw.text((10, y + consolas_header_h + 20), main_text, font=consolas_font, fill="black")

# Save and open
img.save("output.png")
img.show()
