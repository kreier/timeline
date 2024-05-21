# example.py 
from reportlab.pdfgen import canvas
my_canvas = canvas.Canvas("example.pdf")
text = ["Russian and Vietnamese works: Мафуса́л и Trận Đại Hồng Thủy",
"U+02B9 : MODIFIER LETTER PRIME does not work: Me·thuʹse·lah ",
"Japanese does not work: これは日本語のテキストです。",
"Neither does Chinese, Korean or Taiwanese:",
"这是一篇中文文本。| 한국어로 된 글입니다.|這是台灣文字。",
"The hack from /demos/test_multibyte_jpn works: 本語"]
# msg = u'\u6771\u4EAC : Unicode font'.encode('utf8')
# text.append(msg)

# simple drawing works only for latin characters
for i in range(len(text)):
    my_canvas.drawString(30, 800 - 16 * i, text[i])

# with an imported font some of the UTF-8 features work
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
fonts = ['msmincho.ttc',
         '../fonts/aptos.ttf', 
         '../fonts/NotoSimplifiedChinese.ttf', 
         '../fonts/NotoKorean.ttf',
         '../fonts/NotoJapanese.ttf']
fontsize = [14, 14, 12, 12, 12]
for k in range(len(fonts)):
    pdfmetrics.registerFont(TTFont(f"font{k}", fonts[k]))
    my_canvas.setFont(f"font{k}", fontsize[k])
    my_canvas.drawString(30, 685 - 130 * k, f"Font: {fonts[k]}")
    for i in range(len(text)):
        my_canvas.drawString(30, 670 - 16 * i - 130 * k, text[i])

my_canvas.save()
