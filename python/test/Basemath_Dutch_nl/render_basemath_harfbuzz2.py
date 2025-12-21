import uharfbuzz as hb
import unicodedata

# Normalize the string
text = unicodedata.normalize("NFC", "Ba̱smath")

# Load font binary
with open("../../fonts/noto.ttf", "rb") as f:
    fontdata = f.read()

# Create face and font
face = hb.Face(fontdata)
font = hb.Font(face)

# Create buffer and add text
buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()

# Shape
hb.shape(font, buf)

# Inspect glyphs
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    print(f"gid={info.codepoint}, cluster={info.cluster}, "
          f"adv=({pos.x_advance},{pos.y_advance}), "
          f"offset=({pos.x_offset},{pos.y_offset})")