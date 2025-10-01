import sys
import qrcode
from PIL import Image

def generate_qr_code(language_code):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # L 7%, M 15%, Q 25%, H 30%
        box_size=8,
        border=1,
    )
    url = f"https://timeline24.github.io/timeline_{language_code}.pdf"
    qr.add_data(url)
    qr.make(fit=True)

    # Generate image
    # img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img = qr.make_image(fill_color="black", back_color="white")
    
    output_file = f"qr-{language_code}.png"
    img.save(output_file)
    print(f"QR code saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_qr.py language-code")
    else:
        generate_qr_code(sys.argv[1])
