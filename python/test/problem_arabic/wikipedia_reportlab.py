import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
fontfile = "../../fonts/NotoArabic.ttf"
teststring = "أصبحت ويكيبيديا الآن متاحة بـ 342 لغة." # "Wikipedia is now available in 342 languages."

c = canvas.Canvas("wikipedia_reportlab.pdf", pagesize=A4)
pdfmetrics.registerFont(TTFont('testfont', fontfile))
c.setFont("testfont", 24)
c.drawString(28.5, 782.4, teststring)
ar = arabic_reshaper.reshape(teststring)
ar = get_display(ar)
c.drawString(28.5, 733.5, ar)
c.showPage()
c.save()
