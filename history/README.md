# History of timeline projects

With my retirement starting on June 10th, 2023 I started this repository to create a as graphic document to better align events in the flow of time and visualize connections between people and events. These are:

- Timeline 4026 BCE - 2050 CE to be stretched over four A4 landscape papers
- Timeline 1000 BCE - 607 BCE, the kings in the two-tribe nation of Judah and the 10-tribe nation of Israel

| Version | Date          | Persons | Periods | Events | Languages | Keywords | Colors | Images |
|:-------:|---------------|:-------:|:-------:|:------:|:---------:|:--------:|:------:|:------:|
|   1.0   | February 2009 |    63   |    8    |   20   |     1     |          |        |        |
|   1.1   | June 2023     |    63   |    8    |   20   |     2     |          |        |        |
|   2.0   | December 2015 |    24   |    2    |    3   |     1     |          |        |        |
|   3.0   | October 2023  |    68   |    9    |    0   |     1     |     0    |    8   |        |
|   3.5   | November 2023 |   118   |    36   |   40   |     3     |    226   |   109  |        |
|   4.0   | January 2024  |   125   |    41   |   40   |     10    |    234   |   112  |        |
|   4.2   | February 2024 |   128   |    47   |   52   |     13    |    342   |   119  |      7 |
|   4.3   | March 2024    |   131   |    52   |   52   |     15    |    371   |   128  |     27 |
|   4.4   | April 2024    |   132   |    66   |   53   |     15    |    398   |   142  |     49 |
|   4.6   |   June 2024   |   194   |    82   |   45   |     20    |    447   |   162  |   39   |
|   4.9   | November 2024 |   194   |    82   |   45   |     20    |    462   |   162  |   47   |
|   5.3   |   March 2025  |   202   |    87   |   48   |     20    |    475   |   166  |   52   |

## Inspirations

Some documents gave further insight and inspiration into this project.

- [Strengthen Your Faith in God's Word](https://www.jw.org/en/library/jw-meeting-workbook/january-february-2023-mwb/Life-and-Ministry-Meeting-Schedule-for-January-16-22-2023/Strengthen-Your-Faith-in-Gods-Word/) from mwb23.01 for January 16th, 2023
- [“The Whole House of Ahab Will Perish”—2Ki 9:8](https://www.jw.org/en/library/jw-meeting-workbook/november-december-2022-mwb/Life-and-Ministry-Meeting-Schedule-for-November-28-December-4-2022/The-Whole-House-of-Ahab-Will-Perish-2Ki-98/) from mwb22.11 for November 28th, 2022
- [Chart: Prophets and Kings of Judah and of Israel (Part 1)](https://www.jw.org/en/library/bible/study-bible/appendix-a/kings-of-judah/) from nwtsty in 2013
- [Chart: Prophets and Kings of Judah and of Israel (Part 2)](https://www.jw.org/en/library/bible/study-bible/appendix-a/kings-of-israel/) from nwtsty in 2013

## v3.0 Creation of an vector based version with python and reportlab in October 2023

After starting to write programs in python in 2018 and teaching it from 2022 on this looked like a good project to apply these skills. Reading values from a .csv data file would make the creation process much easier and structured. In early October 2023 I finally got reportlab working with python on both macOS and a WSL installation on Windows 11. The first step was to recreate the two pages from libreoffice with this new method. The targeted size is now 4 pages of A4 in landscape combined. This could be printed with the poster function or given to a professional printer to be released on one A0 paper and creating 4 timelines.

The current edition is v3.5. Early October I wrote "Hopefully by end of October 2023 this is done." That might be true for the initial edition, but the more you work with the document, the more ideas you get. See the growing content from v3.0 in October to v3.5 in November 2023:

![timeline v3.0](../docs/timeline20231022.png)
![timeline v3.1](../docs/timeline20231023.png)
![timeline v3.2](../docs/timeline20231102.png)
![timeline v3.3](../docs/timeline20231104.png)
![timeline v3.4](../docs/timeline20231106.png)
![timeline v3.5](../docs/timeline20231110.png)
![timeline v3.5 updated](../docs/timeline20231129.png)

Since v3.4 it is also translated to German, with v3.5 a Vietnamese translation was added. And the respective translations have to be extended with each new detail added. The latest addition above includes the king of the North and South from Daniel 11.

## v4.0 Increase of version number to reflect the year in January 2024

To reflect the year of the timeline edition for at least the next 6 years I simply use the last digit of the year as the leading version indicator. In 2030 this might change to a two-digit version number, if I'm still working on this project. Here we start with v4.0 from January 2024 with extended language and script support:

![timeline v4.0](../docs/timeline20240131_4.0.png)
![timeline v4.2](../docs/timeline20240309_4.2.png)
![timeline v4.4](../docs/timeline20240324_4.4.png)
![timeline v4.5](../docs/timeline20240413_4.5.png)
![timeline v4.6](../docs/timeline20240516_4.6.png)

### v4.7 Switch from reportlab to fpdf2 im May 2024

For 8 months I have been using the reportlab library in python to create the pdf files with the timeline. With a good documentation and support for utf-8 we were able to create the documents with embedded pixel and vector graphics. But by May 2024 I reached a limit of this package: the support for Text Shaping, especially the Glyph substitution is not implemented yet. The challenge is known for some time, but it requires significant manpower to implement properly. I documented my findings in [issue #35](https://github.com/kreier/timeline/issues/35). I tried other solutions like:

- [fpdf](http://www.fpdf.org/) as Free PDF in PHP on [github](https://github.com/Setasign/FPDF) since 2015, but [started in 2001 by Olivier Plathey](https://fr.wikipedia.org/wiki/FPDF) - currently at version 1.86
- [pdfkit](https://pdfkit.org/) library for Node.js in the browser, on [Github](https://github.com/foliojs/pdfkit) with 756 comits and 9600 stars, 16 releases since 2014, [latest 0.15.0](https://github.com/foliojs/pdfkit/releases/tag/v0.15.0) from March 2024
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) for data extraction and more, on [Github](https://github.com/pymupdf/pymupdf) with 2399 commits and 4300 stars, 144 releases since 2015, [latest 1.24.4](https://github.com/pymupdf/PyMuPDF/releases/tag/1.24.4) from May 2024
- [weasyprint](https://weasyprint.org/) mainly to convert HTML to PDF, a professional product with good [documentation](https://doc.courtbouillon.org/weasyprint/stable/) on [Github](https://github.com/Kozea/WeasyPrint) with 5548 commits and 6700 stars, 71 releases since 2016, [latest v62.1](https://github.com/Kozea/WeasyPrint/releases/tag/v62.1) from May 2024 - yet as font subsetter Harfbuzz is [currently experimental](https://github.com/Kozea/WeasyPrint/issues/2120)
- [iText Core](https://itextpdf.com/products/itext-core) with [pdfCalligraph](https://itextpdf.com/products/pdfcalligraph) as add-on for fonts like Arabic, Hebrew or Khmer, in Java; on [Github](https://github.com/itext/itext-java) with 6246 commits and 1900 stars, 41 releases since 2016, latest [8.0.4 Community](https://github.com/itext/itext-java/releases/tag/8.0.4) from April 2024
- [reportlab](https://www.reportlab.com/) with [sourcecode](https://hg.reportlab.com/hg-public/reportlab) mirrored [on Github](https://github.com/MrBitBucket/reportlab-mirror) - all the way back to 2000 with version 0.85, 2.0 in 2006, 3.0 in 2014 and currently at 4.2.1

Interestingly, fpdf2 itself is a fork from PyPDF from [reingart/pypdf](https://github.com/reingart/pyfpdf) 2016, itself being a fork of the [fpdf](http://www.fpdf.org/) library by Max Pat in 2006. See a [little history](https://py-pdf.github.io/fpdf2/History.html). The [release history](https://pypi.org/project/fpdf2/#history) indicates that [Text Shaping](https://py-pdf.github.io/fpdf2/TextShaping.html) was only introduced with 2.7.5 in August 2023. Now with 1479 commits and 969 stars, 33 releases since 2021, the latest being [2.7.9](https://github.com/py-pdf/fpdf2/releases/tag/2.7.9) from May 2024.

## Comparison v3.1 October 2023 to v4.4 March 2024

![timeline v3.1](../docs/timeline20231023.png)
![timeline v4.4](../docs/timeline20240324_4.4.png)


## v1.1 Translation of v1.0 to English in June 2023

The original files from 2009 were created in German. Starting summer 2017 most of my life was going on in English. When sharing this project with friends in early June 2023  I promised to have the translated version ready until the end of month. And the translation was inded completed by June 30th, 2023.

![timeline 2023](https://raw.githubusercontent.com/kreier/timeline/main/docs/timeline20230630.png)

Some black/white copies were print out and shared for feedback. Yet the back of my mind was thinking of an elegant way to make v2.0 come to life.

## v 2.0 Creating a Vector Image with .odg in October 2015

The use of a spreadsheet really limits the possible resolution of the final product, being digital or a printed pdf. Here is a comparison of the resolution of my various approaches:

| page             | begin | end   | timespan | width/mm | years/mm | resolution | columns | created    |
|------------------|-------|-------|----------|----------|----------|------------|---------|------------|
| table 1          | -4050 | -1450 | 2600     | 277      | 9.39     | 10         | 260     | 2009-02-10 |
| table 2          | -1550 | 150   | 1700     | 277      | 6.14     | 5          | 340     | 2009-02-10 |
| table 3          | -130  | 2050  | 2180     | 277      | 7.87     | 10         | 218     | 2009-02-10 |
| drawing odg      | -4000 | 2000  | 6000     | 1250     | 4.8      | ∞          | ∞       | 2015-12-13 |
| reportlab python | -4050 | 2050  | 6100     | 1168     | 5.22     | ∞          | ∞       | 2023-10-17 |

As next step I started to create a vector image that could be exported as pdf with the ability to zoom into details. On October 12, 2015 I started a LibreOffice 4.4 Drawing ODG with a scale of 1cm for 50 years or 5 years/millimeter, resulting in a document with the dimensions 1250x297 mm. This could be printed on my endless A4 paper roll. [Last export as pdf](https://github.com/kreier/timeline/blob/main/spreadsheet/Zeitleiste_wide_20151213.pdf) on December 13, 2015. 

![Zeitleiste 2015](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste2015.png)

## v1.0 Start with a spreadsheet in February 2009

The project to create a paper timeline of human history is done by teenagers around the world. I got an endless paper roll of 10 meters length to start this project, but decided to begin with a digital version. On February 10th, 2009 I created a spreadsheet in OpenOffice 3.0 with 3 tabs for the time 4050-1450 BCE, 1550 BCE - 150 CE and 150-2050 CE. All are designed to fit on a A4 paper, so these 3 pages can be glued together for a single timeline spanning 6000 years.

![Zeitleiste 2009](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste2009.png)

### 4050 - 1450 BCE

For these 2600 years I chose a resolution of 10 years. The spreadsheet has 260 columns, but for the long periods of this time it is precise enough.

![Zeitleiste 4050-1450](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste_4050-1450.png)

### 1550 BCE - 150 CE

The resolution of only 10 years makes it difficult to visualize shorter time perios like the 2 years that Pekachja ruled Israel from 780-778 BCE or the one year that Ahasja ruled Juda 907-906 BCE. The second tile therefore is divided into columns for 5 years and needs 340 columns for the 1700 years from 1550 BCE to 150 CE.

![Zeitleiste 1550 BCE - 150 CE](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste_1550-150.png)

### 130 BCE - 2050 CE

The third tile went back to 10 years per column and needs 218 columns.

![Zeitleiste 130 BCE - 2050 CE](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste_130-2050.png)

## Comparison 2009 vs. 2024

To visualize the progress after 15 years here is a comparison of the spreadsheet version versus a cutout from the python reportlab version for the first 2 time periods of the spreadsheet:

### 4050 BCE to 1450 BCE

![Zeitleiste 4050-1450](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste_4050-1450.png)
![Timeline 4050-1450](https://raw.githubusercontent.com/kreier/timeline/main/docs/timeline_4050-1450_new.png)


### 1550 BCE to 150 CE

![Zeitleiste 1550 BCE - 150 CE](https://raw.githubusercontent.com/kreier/timeline/main/docs/zeitleiste_1550-150.png)
![Zeitleiste 1550 BCE - 150 CE](https://raw.githubusercontent.com/kreier/timeline/main/docs/timeline_1550-150.png)

Now we changed this file in the KH.
