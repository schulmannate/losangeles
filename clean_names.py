
import json
import re

la_path = '/Users/nateschulman/Desktop/la websites/la.html'

def clean_names():
    print("Reading la.html...")
    with open(la_path, 'r') as f:
        content = f.read()

    match = re.search(r'const neighborhoodData = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Could not find neighborhoodData")
        return

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    cleaned_count = 0
    for hood in data:
        for loc in hood.get('locations', []):
            original_name = loc['name']
            cleaned_name = original_name.strip(" *")
            if original_name != cleaned_name:
                loc['name'] = cleaned_name
                cleaned_count += 1
                # print(f"Cleaned: '{original_name}' -> '{cleaned_name}'")

    print(f"Total names cleaned: {cleaned_count}")

    new_json_str = json.dumps(data, indent=4)
    new_page_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

    with open(la_path, 'w') as f:
        f.write(new_page_content)
    print("Successfully wrote updates to la.html")

if __name__ == "__main__":
    clean_names()
