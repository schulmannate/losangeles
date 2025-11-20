import re

with open('/Users/nateschulman/Desktop/addressing la website/data.js', 'r') as f:
    content = f.read()

# Pattern to find span with location class and pin emoji
# The emoji might be encoded as \ud83d\udccd or actual bytes
# In the file read by python, it might be the actual character if utf-8
# But the view_file showed \ud83d\udccd which suggests it might be escaped in the JS string
# Let's look for both

pattern = r'<span class="location">\\ud83d\\udccd\s*(.*?)</span>'
matches = re.findall(pattern, content)

print(f"Found {len(matches)} matches with escaped unicode.")
for m in matches[:5]:
    print(f"Match: {m}")

pattern_utf8 = r'<span class="location">📍\s*(.*?)</span>'
matches_utf8 = re.findall(pattern_utf8, content)
print(f"Found {len(matches_utf8)} matches with utf8 emoji.")
for m in matches_utf8[:5]:
    print(f"Match: {m}")
