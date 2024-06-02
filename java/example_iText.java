import com.itextpdf.kernel.pdf.*;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Paragraph;
import java.io.*;
import com.itextpdf.kernel.font.PdfFont;
import com.itextpdf.kernel.font.PdfFontFactory;
import com.itextpdf.io.font.PdfEncodings;

public class HelloWorld {
  public static final String DEST = "/myfiles/example_iText.pdf";
  public static final String FONT_KHMER = "/uploads/NotoKhmer.ttf";
  public static final String FONT_SINHALA = "/uploads/NotoSinhala.ttf";
  public static final String KHMER = "ស្តេច ហោរា";
  public static final String SINHALA = "සමුළුව";
  
  public static void main(String args[]) throws IOException {
    PdfDocument pdf = new PdfDocument(new PdfWriter(DEST));
    Document document = new Document(pdf);
    document.setFontSize(30).add(new Paragraph("Language Khmer:"));
    PdfFont fontKhmer = PdfFontFactory.createFont(FONT_KHMER, PdfEncodings.IDENTITY_H);
    document.add(new Paragraph().setFont(fontKhmer).setFontSize(30).add("Word 'King Prophet'  ").add(KHMER));
    
    document.setFontSize(30).add(new Paragraph("\nLanguage Sinhala"));
    PdfFont fontSinhala = PdfFontFactory.createFont(FONT_SINHALA, PdfEncodings.IDENTITY_H);
    document.add(new Paragraph().setFont(fontSinhala).setFontSize(30).add("Word 'Conference'  ").add(SINHALA));
    document.close();
  }
}
