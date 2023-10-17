# A Timeline of human history

Human history graph created with python and reportlab. Currently only v3.0 with two pages from LibreOffice are finished.

![timeline](docs/timeline20230630.png)

## Reactivation 2023

After many years it was finally time to translate the project to English and share with my friends. In the 14 years since beginning this project I learned a lot about programming languages, vector graphics and possible solutions using pandas, csv files and reportlab (instead of matplotlib). In a first stage I translated the old OpenOffice documents to english. Then I collected data into csv files for later automated processing and graph generation. This way the translation to another language is just the change of one import file. So far I translated the first page:

![timeline one 4050 - 1450 BCE](docs/timeline_4050-1450.png)

This project started on here on Github on June 10th, 2023. My last day of work.

## Version history

- v1.0 2009/02/10 An [OpenOffice spreadsheet](https://github.com/kreier/timeline/blob/5ffa9bac5cb4ff3c2cdc362b63df161e0d909c9d/spreadsheet/Zeitleiste_3A4_20090210.ods) with 260, 340 and 218 columns to create the overview with a resolution of 5 or 10 years. See the [resulting pdf](https://github.com/kreier/timeline/blob/5ffa9bac5cb4ff3c2cdc362b63df161e0d909c9d/spreadsheet/Zeitleiste_3A4_20090211.pdf).
- v2.0 2015/10/12 A __vector image__ as a LibreOffice odf to cover 6000 years on [one pdf](https://github.com/kreier/timeline/blob/5ffa9bac5cb4ff3c2cdc362b63df161e0d909c9d/spreadsheet/Zeitleiste_wide_20151213.pdf) and no restrictions in the representation of years. It was very cumbersome to edit and by December only the first __24 persons__ were indicated with their lifetime.
- v3.0 2023/06/30 __Translation to English.__ For a broader audience and to get feedback on the planned vector version I translated the original OpenOffice Spreadsheet version to English. By June 30th the exported pdf was finished with __70 timespans__ depicted. And 17 comments on specific dates.
- v4.0 2023/10/30 __Vector document__ generated with [a python program](https://github.com/kreier/timeline/blob/main/python/6000.py) and reportlab.

### Scale challenges

To compensate for limited printing area I created a border of 1cm around each page. The effective drawing area on A4 landscape in each tile is 277 millimeter. This results in _different time scales_ for each page, since the covered timespan is not equal for each page. But this was one of the fundamental ideas of this project, to represent a *larger amount of time* with a *bigger amount of space* or length. Here are the values for comparison:

| page        | begin | end   | timespan | width/mm | years/mm | resolution | columns |
|-------------|-------|-------|----------|----------|----------|------------|---------|
| table 1     | -4050 | -1450 | 2600     | 277      | 9.39     | 10         | 260     |
| table 2     | -1550 | 150   | 1700     | 277      | 6.14     | 5          | 340     |
| table 3     | -130  | 2050  | 2180     | 277      | 7.87     | 10         | 218     |
| drawing odg | -4000 | 2000  | 6000     | 1250     | 4.80     | ∞          | ∞       |

See [scale.csv](spreadsheet/scale.csv)

