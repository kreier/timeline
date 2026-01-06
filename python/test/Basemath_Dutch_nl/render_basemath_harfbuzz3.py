import freetype
import harfbuzz as hb
import unicodedata

text = unicodedata.normalize("NFC", "Ba̱smath")

face = freetype.Face("../../fonts/noto.ttf")
face.set_char_size(32*64)

hb_font = hb.ft_font_create(face)

buf = hb.Buffer()
buf.add_str(text)
buf.guess_segment_properties()

hb.shape(hb_font, buf)

for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    print(info.codepoint, pos.x_advance, pos.y_advance)