# convert year - month - date to a float value

d = int(input("day: "))
m = int(input("month: "))
y = int(input("year: "))

print(f"In CE that would be {y + (m-1)/12 + (d-1)/360}")
print(f"In BCE that would be {-y+1 - (12-m)/12 - (31-d)/360}")

# return: concatenate