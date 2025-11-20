import re
import urllib.parse

file_path = '/Users/nateschulman/Desktop/addressing la website/data.js'

with open(file_path, 'r') as f:
    content = f.read()

# Pattern matches: <span class=\"location\">\ud83d\udccd Address</span>
# Note: The file content has literal backslashes for escaping quotes and unicode.
pattern = r'<span class=\\"location\\">\\ud83d\\udccd\s*(.*?)</span>'

def replacement(match):
    address = match.group(1)
    # Encode the address for the URL query parameter
    encoded_address = urllib.parse.quote(address)
    
    # Construct the new anchor tag
    # We need to maintain the escaping for the JS string context
    return f'<a href=\\"https://www.google.com/maps/search/?api=1&query={encoded_address}\\" target=\\"_blank\\" class=\\"location\\">\\ud83d\\udccd {address}</a>'

new_content, count = re.subn(pattern, replacement, content)

with open(file_path, 'w') as f:
    f.write(new_content)

print(f"Replaced {count} occurrences.")
