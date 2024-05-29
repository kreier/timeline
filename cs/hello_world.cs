using iText.Kernel.Pdf;
using iText.Layout;
using iText.Layout.Element;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        string filename = "hello_world.pdf";

        using (var writer = new PdfWriter(filename))
        using (var pdfDoc = new PdfDocument(writer))
        using (var document = new Document(pdfDoc))
        {
            document.Add(new Paragraph("Hello World!"));
        }

        Console.WriteLine($"PDF created successfully: {filename}");
    }
}
