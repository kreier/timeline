# example.py 
from reportlab.pdfgen import canvas
my_canvas = canvas.Canvas("example.pdf")
text = ["Russian and Vietnamese works: Мафуса́л и Trận Đại Hồng Thủy",
"U+02B9 : MODIFIER LETTER PRIME does not work: Me·thuʹse·lah ",
"Japanese does not work: これは日本語のテキストです。",
"Neither does Chinese, Korean or Taiwanese:", 
"这是一篇中文文本。| 한국어로 된 글입니다.|這是台灣文字。",
"The hack from /demos/test_multibyte_jpn works: 本語"]
msg = u'\u6771\u4EAC : Unicode font'.encode('utf8')
text.append(msg)

# simple drawing works only for latin characters
for i in range(7):
    my_canvas.drawString(50, 780 - 16 * i, text[i])

# with an imported font some of the UTF-8 features work
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Aptos', '../aptos.ttf'))
my_canvas.setFont("Aptos", 14)
for i in range(7):
    my_canvas.drawString(50, 660 - 16 * i, text[i])

# now using the msmincho.ttc font
pdfmetrics.registerFont(TTFont('MS Mincho','msmincho.ttc'))
my_canvas.setFont('MS Mincho', 14)
for i in range(7):
    my_canvas.drawString(50, 540 - 16 * i, text[i])

# with an imported font some of the UTF-8 features work - Chinese
pdfmetrics.registerFont(TTFont('Noto1', 'NotoSansSC-Medium.ttf'))
my_canvas.setFont("Noto1", 14)
for i in range(7):
    my_canvas.drawString(50, 420 - 16 * i, text[i])

# with an imported font some of the UTF-8 features work -  Korean
pdfmetrics.registerFont(TTFont('Noto2', 'NotoSansKR-Medium.ttf'))
my_canvas.setFont("Noto2", 14)
for i in range(7):
    my_canvas.drawString(50, 300 - 16 * i, text[i])

# with an imported font some of the UTF-8 features work - Japanese
pdfmetrics.registerFont(TTFont('Noto', 'NotoSansJP-Medium.ttf'))
my_canvas.setFont("Noto", 14)
for i in range(7):
    my_canvas.drawString(50, 180 - 16 * i, text[i])

my_canvas.save()
