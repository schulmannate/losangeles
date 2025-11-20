import re

with open('/Users/nateschulman/Desktop/addressing la website/data.js', 'r') as f:
    content = f.read()

pattern = r'<span class=\\"location\\">\\ud83d\\udccd\s*(.*?)</span>'
matches = re.findall(pattern, content)

found_quotes = False
for m in matches:
    if '\\"' in m:
        print(f"Found escaped quote in address: {m}")
        found_quotes = True

if not found_quotes:
    print("No escaped quotes found in addresses.")
