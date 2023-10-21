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
