import freetype
import uharfbuzz as hb
import unicodedata

# Normalize the string to NFC (though a̱ stays decomposed)
text = unicodedata.normalize("NFC", "Ba̱smath")

# Load a font that supports combining marks (Gentium Plus, Noto Sans, DejaVu Sans, etc.)
# face = freetype.Face("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")
face = freetype.Face("../../fonts/noto.ttf")  # Adjust path as necessary
face.set_char_size(32*64)

# Create HarfBuzz font
hb_font = hb.Font.from_freetype(face)

# Create buffer and add text
buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()

# Shape
hb.shape(hb_font, buf)

# Inspect glyphs
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    gid = info.codepoint
    cluster = info.cluster
    x_advance = pos.x_advance / 64.0
    y_advance = pos.y_advance / 64.0
    x_offset = pos.x_offset / 64.0
    y_offset = pos.y_offset / 64.0
    print(f"gid={gid}, cluster={cluster}, adv=({x_advance},{y_advance}), offset=({x_offset},{y_offset})")