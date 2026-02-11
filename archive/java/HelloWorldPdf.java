import com.itextpdf.kernel.pdf.*;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Paragraph;
import java.io.*;

public class HelloWorldPdf {
    // public static final String DEST = "hello_world.pdf";
    public static final String DEST = "/myfiles/hello.pdf";
    
    public static void main(String[] args) {
        String filename = "hello_world.pdf";

        try {
            PdfDocument pdf = new PdfDocument(new PdfWriter(DEST));
            Document document = new Document(pdf);
            // document.open();
            document.add(new Paragraph("Hello World! in my timeline project."));
            document.close();
            System.out.println("PDF created successfully: " + filename);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

// import com.itextpdf.kernel.pdf.*;
// import com.itextpdf.layout.Document;
// import com.itextpdf.layout.element.Paragraph;
// import java.io.*;

// public class HelloWorld {
//   public static final String DEST = "/myfiles/hello.pdf";
  
//   public static void main(String args[]) throws IOException {
//     PdfDocument pdf = new PdfDocument(new PdfWriter(DEST));
//     Document document = new Document(pdf);
//     String line = "Hello! Welcome to iTextPdf";
//     document.add(new Paragraph(line));
//     document.close();

//     System.out.println("Awesome PDF just got created.");
//   }
// }