import re
strings = '[hi] there'
strings = re.sub(r'\[.*?\]', ' ', strings)

print(strings)
