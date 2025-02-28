# import arabic_reshaper
# from bidi.algorithm import get_display
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfbase.ttfonts import TTFont
# fontfile = "../../fonts/NotoArabic.ttf"
# teststring = "أصبحت ويكيبيديا الآن متاحة بـ 342 لغة." # "Wikipedia is now available in 342 languages."

# c = canvas.Canvas("wikipedia_reportlab.pdf", pagesize=A4)
# pdfmetrics.registerFont(TTFont('testfont', fontfile))
# c.setFont("testfont", 24)
# c.drawString(28.5, 782.4, teststring)
# ar = arabic_reshaper.reshape(teststring)
# ar = get_display(ar)
# c.drawString(28.5, 733.5, ar)
# c.showPage()
# c.save()

# from https://groups.google.com/g/reportlab-users/c/np95WmcQh-I

from pyfribidi2 import log2vis, ON as DIR_ON, LTR as DIR_LTR, RTL as DIR_RTL

def _formatText(self, text):
    "Generates PDF text output operator(s)"
    if log2vis and self.direction in ('LTR','RTL'):
        # Use pyfribidi to write the text in the correct visual order.
        text = log2vis(text, directionsMap.get(self.direction.upper(),DIR_ON),clean=True)
