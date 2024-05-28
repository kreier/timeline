# example_Khmer.py - try Khmer
from reportlab.pdfgen import canvas
my_canvas = canvas.Canvas("example_Khmer.pdf")
my_canvas.setAuthor("Khmer test")
my_canvas.setTitle("Test rendering Khmer glyphs")
my_canvas.setSubject("support Unicode v3.0 and utf-8 in reportlab")
text = ["Simple examples in Russian, Vietnamese, Japanese, Chinese, Korean, Taiwanese and Khmer:",
"Мафуса́л и, Trận Đại Hồng, これは日本語, 这是一篇中, 한국어로, 這是台灣文, កាំ ",
"U+02B9 : MODIFIER LETTER PRIME does not work: Me·thuʹse·lah ",
"Khmer syllable 'កាំ' (kâm), longer មនុស្ស (kings)", 
"Problems: ស្ស (2) ចៅក្ (2) ហោ (1) ស្តេ (2) ព្រឹត្តិ (4) ណ៍ (1) ត្ថុ (2) ត្ថុ (2)", 
"fresh: ស្រស់ and syllable ssa: ស្ស"]

# simple drawing works only for latin characters - 800 from the bottom
for i in range(len(text)):
    my_canvas.drawString(30, 800 - 16 * i, text[i])

# with an imported font some of the UTF-8 features work
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
fonts = ['../fonts/aptos.ttf', 
         '../fonts/NotoKhmer.ttf']
fontsize = [13, 12]
for k in range(len(fonts)): # print the example text in the different fonts from 685 downwards
    pdfmetrics.registerFont(TTFont(f"font{k}", fonts[k]))
    my_canvas.setFont(f"font{k}", fontsize[k])
    my_canvas.drawString(30, 685 - 130 * k, f"Font: {fonts[k]}")
    for i in range(len(text)):
        my_canvas.drawString(30, 670 - 16 * i - 130 * k, text[i])

my_canvas.save()

def print_unicode_values(s):
    for char in s:
        print(f'The unicode value of {char} is {ord(char)}. In Hex: {hex(ord(char))} or {bytearray(char, 'utf-8')}')

teststring = "ស្រស់" # fresh
print(f"\nFirst teststring: {teststring}")
print_unicode_values(teststring)
ba = bytearray(teststring, 'utf-8')
for byte in ba:
    print(hex(byte), end=' ')

teststring = "ស្ស"
print(f"\nSecond teststring: {teststring}")
print_unicode_values(teststring)
ba = bytearray(teststring, 'utf-8')
for byte in ba:
    print(hex(byte), end=' ')

