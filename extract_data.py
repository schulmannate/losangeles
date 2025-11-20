import re
import json
import os

html_path = 'addressing-la-modern.html'
output_path = 'data.js'

try:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match neighborhood cards
    # <article class="neighborhood-card" data-region="..."> ... </article>
    card_regex = re.compile(r'<article class="neighborhood-card" data-region="([^"]+)">([\s\S]*?)</article>')
    
    neighborhoods = []
    
    for match in card_regex.finditer(content):
        region = match.group(1)
        card_content = match.group(2)
        
        # Extract Name
        name_match = re.search(r'<h2>(.*?)</h2>', card_content)
        name = name_match.group(1).strip() if name_match else 'Unknown'
        
        # Extract Description
        desc_match = re.search(r'<div class="description">([\s\S]*?)</div>', card_content)
        description = desc_match.group(1).strip() if desc_match else ''
        
        # Extract Sub-areas
        sub_areas_match = re.search(r'<div class="sub-areas">([\s\S]*?)</div>', card_content)
        sub_areas = sub_areas_match.group(1).strip() if sub_areas_match else ''
        
        # Create ID
        id_str = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        
        neighborhoods.append({
            'id': id_str,
            'name': name,
            'region': region,
            'description': description,
            'subAreas': sub_areas
        })

    js_content = f"const neighborhoodData = {json.dumps(neighborhoods, indent=2)};\n\nif (typeof module !== 'undefined') module.exports = neighborhoodData;"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Successfully extracted {len(neighborhoods)} neighborhoods to data.js")

except Exception as e:
    print(f"Error extracting data: {e}")
