import unicodedata
import uharfbuzz as hb
import freetype
from PIL import Image

# --------- Config ----------
FONT_PATH = "../../fonts/noto.ttf"
TEXT = unicodedata.normalize("NFC", "Ba̱smath")
FONT_PIXEL_SIZE = 64       # vertical pixel size for rendering
MARGIN = 20                # padding around the text
OUTPUT = "output.png"
# ---------------------------

# 1) Shape with HarfBuzz (using raw font data)
with open(FONT_PATH, "rb") as f:
    fontdata = f.read()

hb_face = hb.Face(fontdata)
hb_font = hb.Font(hb_face)

buf = hb.Buffer()
buf.add_str(TEXT)
buf.guess_segment_properties()
hb.shape(hb_font, buf)

infos = buf.glyph_infos
positions = buf.glyph_positions

upem = hb_face.upem  # units per em
scale = FONT_PIXEL_SIZE / upem

# 2) Prepare FreeType face for rasterization
ft_face = freetype.Face(FONT_PATH)
ft_face.set_pixel_sizes(0, FONT_PIXEL_SIZE)  # set height to FONT_PIXEL_SIZE pixels

# Metrics (ascender/descender are in 26.6 units -> divide by 64)
ascent = ft_face.size.ascender / 64.0
descent = -ft_face.size.descender / 64.0
baseline_y = MARGIN + ascent

# Estimate image width from total advance (in 26.6 units -> divide by 64)
total_advance_x = sum(pos.x_advance for pos in positions) / 64.0
img_width = int(total_advance_x) + 2 * MARGIN
img_height = int(ascent + descent) + 2 * MARGIN

# 3) Create canvas (grayscale “L”: 255 = white background)
img = Image.new("L", (max(img_width, 1), max(img_height, 1)), color=255)

# 4) Render each glyph respecting HarfBuzz advances and offsets
x, y = MARGIN, baseline_y  # pen position at baseline
for info, pos in zip(infos, positions):
    gid = info.codepoint

    # Render glyph bitmap
    ft_face.load_glyph(gid, freetype.FT_LOAD_RENDER)
    slot = ft_face.glyph
    bitmap = slot.bitmap
    top = slot.bitmap_top
    left = slot.bitmap_left

    if bitmap.width > 0 and bitmap.rows > 0:
        # Convert FreeType bitmap buffer to bytes for Pillow
        glyph_img = Image.frombytes("L", (bitmap.width, bitmap.rows), bytes(bitmap.buffer))

        # Apply HarfBuzz offsets (26.6 fixed-point -> divide by 64.0)
        x_offset = pos.x_offset / 64.0
        y_offset = pos.y_offset / 64.0

        # Paste glyph at computed position
        paste_x = int(x + left + x_offset)
        paste_y = int(y - top + y_offset)
        img.paste(glyph_img, (paste_x, paste_y), glyph_img)

    # Advance pen (respect kerning and mark attachment)
    x += pos.x_advance / 64.0
    y += pos.y_advance / 64.0

# 5) Save or display
img.save(OUTPUT)
img.show()

print(f"Saved rendered image to {OUTPUT}")
