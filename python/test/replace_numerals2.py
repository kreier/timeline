# Mapping of Arabic numerals to Khmer numerals
arabic_to_khmer = {
    '0': '០',
    '1': '១',
    '2': '២',
    '3': '៣',
    '4': '៤',
    '5': '៥',
    '6': '៦',
    '7': '៧',
    '8': '៨',
    '9': '៩'
}

# Creating a translation table
translation_table = str.maketrans(arabic_to_khmer)

# Function to replace Arabic numerals with Khmer numerals
def replace_arabic_with_khmer(input_string):
    return input_string.translate(translation_table)

# Example usage
input_string = "4.6 សង្គ្រាមលោកលើកទី 1 - 1914-1918 គ."
output_string = replace_arabic_with_khmer(input_string)
print("Original string:", input_string)
print("Modified string:", output_string)
