from PIL import Image, ImageDraw, ImageFont
import freetype
import uharfbuzz as hb

# Test string
text = "Ba̱smath, Te̱rah and Me·thuʹse·lah"
font_path = "C:/Windows/Fonts/consola.ttf"
size = 72

# --- Without HarfBuzz (Pillow only) ---
font = ImageFont.truetype(font_path, size)
img_left = Image.new("RGB", (800, 200), "white")
draw_left = ImageDraw.Draw(img_left)
draw_left.text((10, 80), text, font=font, fill="black")

# --- With HarfBuzz shaping ---
# Load font with FreeType
face = freetype.Face(font_path)
face.set_char_size(size * 64)

# Load font binary for HarfBuzz
with open(font_path, "rb") as f:
    fontdata = f.read()

hb_face = hb.Face(fontdata)
hb_font = hb.Font(hb_face)

buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()
hb.shape(hb_font, buf)

infos = buf.glyph_infos
positions = buf.glyph_positions

img_right = Image.new("RGB", (800, 200), "white")

x, y = 50, 120
for info, pos in zip(infos, positions):
    gid = info.codepoint
    face.load_glyph(gid, freetype.FT_LOAD_RENDER)
    bitmap = face.glyph.bitmap
    top, left = face.glyph.bitmap_top, face.glyph.bitmap_left

    if bitmap.width > 0 and bitmap.rows > 0:
        glyph_img = Image.frombytes("L", (bitmap.width, bitmap.rows), bytes(bitmap.buffer))
        img_right.paste(
            Image.merge("RGB", (glyph_img, glyph_img, glyph_img)),
            (x + left + pos.x_offset // 64, y - top - pos.y_offset // 64),
            glyph_img
        )

    # Advance by HarfBuzz's shaped values (scaled to pixels)
    x += pos.x_advance // 32
    y += pos.y_advance // 32

# --- Combine both images side by side ---
width = img_left.width + img_right.width
height = max(img_left.height, img_right.height)
combined = Image.new("RGB", (width, height), "white")

combined.paste(img_left, (0, 0))
combined.paste(img_right, (img_left.width, 0))

# Add labels
draw_combined = ImageDraw.Draw(combined)
draw_combined.text((10, 10), "Without HarfBuzz", font=ImageFont.truetype(font_path, 24), fill="red")
draw_combined.text((img_left.width + 10, 10), "With HarfBuzz", font=ImageFont.truetype(font_path, 24), fill="green")

# Save and show
combined.save("comparison.png")
combined.show()
