
import json
import re
from bs4 import BeautifulSoup

la_path = '/Users/nateschulman/Desktop/la websites/la.html'
laold_path = '/Users/nateschulman/Desktop/la websites/laold.html'

def parse_html_subareas(html_str):
    """
    Parses the legacy HTML subAreas string into a list of location objects.
    """
    locations = []
    if not html_str or html_str == "None":
        return locations

    soup = BeautifulSoup(html_str, 'html.parser')
    items = soup.find_all('li') # Changed to recursive to find LIs inside ULs

    if not items and "<li>" in html_str:
         # Fallback for malformed HTML or just raw string - ensure we wrap it if needed, though find_all('li') should catch it.
         soup = BeautifulSoup(f"<ul>{html_str}</ul>", 'html.parser')
         items = soup.find_all('li')
    
    # print(f"DEBUG: Found {len(items)} items in subareas")


    for li in items:
        # Extract Name
        b_tag = li.find('b')
        name = b_tag.get_text(strip=True) if b_tag else li.get_text(strip=True).split('<br>')[0].split('\n')[0]
        
        # Remove name from text to get description
        full_text = li.get_text(" ", strip=True) 
        description = full_text.replace(name, "", 1).strip()
        
        # Extract Address and Map URL
        address = ""
        map_url = ""
        a_tag = li.find('a')
        if a_tag:
            map_url = a_tag.get('href', '')
            address = a_tag.get_text(strip=True)
            # Remove address from description if it's there
            description = description.replace(address, "").replace("📍", "").strip()
        
        # Clean description
        description = description.strip(" -")

        # Heuristic for Type
        loc_type = "sub-neighborhood"
        if address or len(description) > 30 or "Historic" in description or "Landmark" in description:
            loc_type = "landmark"
            
        # Clean name
        name = name.strip(" -:*")

        if name:
            locations.append({
                "name": name,
                "type": loc_type,
                "address": address,
                "mapUrl": map_url,
                "description": description
            })
            
    return locations

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower()) if text else ""

def extract_js_data(content):
    """
    Manually extracts neighborhood data from JS object literals that use backticks.
    Returns a list of dicts with 'id', 'name', 'subAreas' (raw HTML string).
    """
    # Regex to capture content inside: { "id": "...", ... "subAreas": `...` }
    # We use a non-greedy logic.
    # Note: This regex assumes the structure matches the viewed file content.
    pattern = r'\{\s*"id":\s*"([^"]+)",\s*"name":\s*"([^"]+)",.*?"subAreas":\s*`([^`]*)`'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    data = []
    for m in matches:
        data.append({
            "id": m.group(1),
            "name": m.group(2),
            "subAreas": m.group(3)
        })
    return data

def merge_content():
    print("Reading laold.html...")
    with open(laold_path, 'r') as f:
        old_content = f.read()

    # Extract strictly using regex because of backticks
    old_data = extract_js_data(old_content)
    print(f"Found {len(old_data)} neighborhoods in laold.html")

    print("Reading la.html...")
    with open(la_path, 'r') as f:
        current_content = f.read()

    # la.html is expected to be valid JSON inside the variable declaration
    # We look for: const neighborhoodData = [...];
    match_current = re.search(r'const neighborhoodData = (\[.*?\]);', current_content, re.DOTALL)
    if not match_current:
        print("Could not find neighborhoodData in la.html")
        return

    try:
        current_data = json.loads(match_current.group(1))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON in la.html: {e}")
        # Identify where it failed
        # print(match_current.group(1)[e.pos-20:e.pos+20])
        return

    print(f"Found {len(current_data)} neighborhoods in la.html")

    # 3. Merge
    updates_count = 0
    added_locations_count = 0

    for old_hood in old_data:
        old_id = old_hood['id']
        old_subareas_html = old_hood['subAreas']
        
        if not old_subareas_html or old_subareas_html.strip() == "":
            continue

        # Find matching new hood
        target_hood = next((h for h in current_data if h['id'] == old_id), None)
        
        if target_hood:
            # Parse old locations
            old_locations = parse_html_subareas(old_subareas_html)
            
            if not old_locations:
                continue

            current_locations = target_hood.get('locations', [])
            
            # Create set of normalized existing names/addresses for fast lookup
            existing_signatures = set()
            for loc in current_locations:
                existing_signatures.add(normalize(loc['name']))
                if loc.get('address'):
                    existing_signatures.add(normalize(loc['address']))

            # Merge
            hood_updated = False
            for loc in old_locations:
                name_sig = normalize(loc['name'])
                addr_sig = normalize(loc['address'])
                
                is_duplicate = False
                if name_sig and name_sig in existing_signatures:
                    is_duplicate = True
                elif addr_sig and addr_sig in existing_signatures:
                    is_duplicate = True
                
                if not is_duplicate:
                    # Append new location
                    current_locations.append(loc)
                    existing_signatures.add(name_sig) # Add to set to prevent internal duplicates
                    if addr_sig:
                        existing_signatures.add(addr_sig)
                    
                    added_locations_count += 1
                    hood_updated = True
                    # Optional: Print added items for debugging
                    # print(f"  + Added to {target_hood['name']}: {loc['name']}")

            if hood_updated:
                target_hood['locations'] = current_locations
                updates_count += 1
                # print(f"Updated {target_hood['name']} with new content.")
        
    print(f"Total neighborhoods updated: {updates_count}")
    print(f"Total new locations added: {added_locations_count}")

    # 4. Write back to la.html
    new_json_str = json.dumps(current_data, indent=4)
    new_page_content = current_content[:match_current.start(1)] + new_json_str + current_content[match_current.end(1):]

    with open(la_path, 'w') as f:
        f.write(new_page_content)
    print("Successfully wrote updates to la.html")

if __name__ == "__main__":
    merge_content()
