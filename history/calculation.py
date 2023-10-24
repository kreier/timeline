# some imports?
# at least some functions

def year(date_float):
    year = int(date_float)
    if year < 0:
        year -= 1
    return year

def month(date_float):
    month = int((date_float - int(date_float))*12)
    if date_float < 0:
        month = 13 + month
    return month

def day(date_float):
    month = (date_float - int(date_float))*12
    if date_float < 0:
        month = 13 + month
    day = int((month - int(month))*30) + 1
    return day


date = -4025.25
datestring = "0037-12-15"


print("____________________________ converting ________________________________")
y = int(datestring[0:4])
m = int(datestring[5:7])
d = int(datestring[8:])
print(f"The decoded datestring {datestring} is day {d}, month {m} and year {y}.")
ce_float = y + m/12 - 1+ d/360
bce_float = -y+1 - (12-m)/12 - (31-d)/360
print(f"The respective float values are {ce_float:.7} for CE and {bce_float:.7} for BCE.\n")

print(f"Decoded float date {date} is year {year(date)}, month {month(date)} and day {day(date)}.\n")

print("Year conversion")
print("positive:")
print(f"The float value of year is {date}")
print(f"year:  {int(date)}")
month = (date - int(date)) * 12
print(f"month: {int(month)}")
day = int((month - int(month))*30) + 1
print(f"day:   {int(day)}\n")

print("negative:")
date *= -1
print(f"The float value of year is {date}")
year_negative = int(date)
if date < int(date):
    year_negative -= 1
print(f"year:  {int(year_negative)}")
month = 13 + (date - int(date)) * 12
print(f"month: {int(month)}")
day = int((month - int(month))*30) + 1
print(f"day:   {int(day)}\n")

# Calculate the scale of the timeline
print("Scale of the timeline")
print("---------------------\n")

# Horizontally: time
print("Horizontally: Time")

start = -4075
end   = 2075
timespan = end - start
print(f"For the time from {start} to {end} we have a span of {timespan} years")

x_scale_years_per_mm = 5
width_min_mm = timespan / x_scale_years_per_mm
print(f"With a scale of {x_scale_years_per_mm} years per millimeter we need at \
least {width_min_mm} millimeters width.\n")

# Vertically: persons and time periods
print("Vertically: people and time periods")

paper_height_mm = 210
border_tb_mm = 10
drawing_height_mm = paper_height_mm - 2 * border_tb_mm
print(f"A paper A4 landscape has a height of {paper_height_mm} millimeters. \
With a border of {border_tb_mm} millimeter on top and bottom the drawing \
height is {drawing_height_mm} millimeters.")

drawing_height_dot = drawing_height_mm / 25.4 * 72
print(f"With 25.4 millimeter in an inch and 1/72 inch in a dot this gives us \
a drawing height of {drawing_height_dot:.5} dots.")

font_size = 12
line_height = font_size * 1.2
possible_lines = drawing_height_dot / line_height
print(f"With a font size of {font_size} dots and 20% extra space for the lines \
we get a line height of {line_height:.4} dots. This in turn results in \
{possible_lines:.3} possible lines in our timeline.")

# Kings of Juda and Israel
kings_israel = 21
kings_juda = 20
print(f"The northern kingdom of Israel had {kings_israel} kings from the \
division of the kingdom in 997 BCE until the desctruction of Samarila in \
740 BCE by Assyria. The southern kingdom of Jusa had {kings_juda} kings \
from 997 BCE until the desctruction of Jerusalem in 607 BCE by Babylon.")
print(f"To map this period from 997 - 607 BCE ({997-607} years) we \
need {kings_israel + kings_juda} lines if they should not overlap.")


