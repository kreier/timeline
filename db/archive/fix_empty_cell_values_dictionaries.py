# Some cell values in the dictionaries are just empty, giving a NaN return value for pandas
# If it is a number, panda returns it as float instead of string
# The 'fix' is to replace empty cells with an ' ' empty space

import pandas as pd
import os

dicts = []
codes = []

for f in os.listdir("./"):
    if f.startswith("dictionary") and f.endswith("csv"):
        if os.path.isfile(os.path.join("./", f)):
            dicts.append(f)
            codes.append((f[11:])[:-4])

print(f"Found {len(dicts)} dictionaries. The language codes are:")
for i in range(len(codes)-1):
    print(f"{codes[i]}, ", end="")
print(codes[len(codes)-1])

to_fix = []
print("No need to fix ", end="")
for dict in dicts:
    dictionary = pd.read_csv("./" + dict, encoding='utf8')
    # dictionary = dictionary.fillna(" ")
    nan_count = dictionary.isna().sum()

    if nan_count['text'] == 0:
        print(".", end="")
        # print(f"{dict} needs no fix.")
    else:
        to_fix.append(dict)
        # print(nan_count)
    # if nan_count > 0:
    #     print(f"{dict} has {nan_count} empty cells to be fixed.")
print(f"\nThere are still {len(to_fix)} dictionaries to fix. They are:")
print(to_fix)

code = "ilo"

# dictionary = pd.read_csv("./dictionary_" + code + ".csv", encoding='utf8')
# dictionary = dictionary.fillna(" ")
# dictionary.to_csv("./dictionary_" + code + ".csv", encoding='utf8', index=False)
