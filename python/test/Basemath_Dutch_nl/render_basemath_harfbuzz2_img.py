import uharfbuzz as hb
import unicodedata
from PIL import Image, ImageDraw
import freetype

# Normalize text
text = unicodedata.normalize("NFC", "Ba̱smath")

# Load font binary for HarfBuzz
with open("../../fonts/noto.ttf", "rb") as f:
    fontdata = f.read()

# HarfBuzz shaping
face = hb.Face(fontdata)
font = hb.Font(face)
buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()
hb.shape(font, buf)

infos = buf.glyph_infos
positions = buf.glyph_positions

# FreeType face for rasterization
ft_face = freetype.Face("../../fonts/noto.ttf")
ft_face.set_char_size(48*64)  # 48pt

# Create a blank image
img = Image.new("L", (400, 100), color=255)  # grayscale, white background
draw = ImageDraw.Draw(img)

# Render glyphs

# scale = ft_face.size.metrics.y_scale / 65536  # vertical scale factor

x, y = 20, 60  # baseline start

for info, pos in zip(infos, positions):
    gid = info.codepoint
    ft_face.load_glyph(gid, freetype.FT_LOAD_RENDER)
    bitmap = ft_face.glyph.bitmap
    top = ft_face.glyph.bitmap_top
    left = ft_face.glyph.bitmap_left

    # Convert FreeType bitmap to Pillow image
    glyph_img = Image.frombytes(
        "L",
        (bitmap.width, bitmap.rows),
        bytes(bitmap.buffer)   # <-- convert here
    )



    # Paste glyph into main image
    # img.paste(glyph_img, (x + left, y - top), glyph_img)
    img.paste(glyph_img, (int(x + left + pos.x_offset/64.0),
                      int(y - top + pos.y_offset/64.0)), glyph_img)

    # Advance pen position using HarfBuzz values (scaled)
    x += pos.x_advance / 64.0
    y += pos.y_advance / 64.0

    # # Advance pen position
    # x += pos.x_advance // 64
    # y += pos.y_advance // 64

# Save or show
img.show()
img.save("output.png")