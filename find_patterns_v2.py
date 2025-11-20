import re

with open('/Users/nateschulman/Desktop/addressing la website/data.js', 'r') as f:
    content = f.read()

# Pattern to find span with escaped quotes and unicode
# The file content has class=\"location\" inside the string
# So we need to match class=\\"location\\"
# And \ud83d\udccd is likely literal characters \ u d ...

pattern = r'<span class=\\"location\\">\\ud83d\\udccd\s*(.*?)</span>'
matches = re.findall(pattern, content)

print(f"Found {len(matches)} matches with escaped quotes and unicode.")
for m in matches[:5]:
    print(f"Match: {m}")
