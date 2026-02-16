
import json
import re
import yaml # PyYAML

la_path = '/Users/nateschulman/Desktop/la websites/la.html'
yaml_path = '/Users/nateschulman/Desktop/la websites/data.yaml'

def extract_to_yaml():
    print("Reading la.html...")
    with open(la_path, 'r') as f:
        content = f.read()

    # Extract JSON data
    match = re.search(r'const neighborhoodData = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Could not find neighborhoodData in la.html")
        return

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    print(f"Extracted {len(data)} neighborhoods.")

    # Transform to requested YAML structure
    # Request: 
    # - id: ...
    #   name: ...
    #   landmarks: 
    #     - name: ...
    
    yaml_data = []
    for hood in data:
        new_hood = {
            'id': hood.get('id', ''),
            'name': hood.get('name', ''),
            'region': hood.get('region', ''),
            'description': hood.get('description', '')
        }
        
        locations = hood.get('locations', [])
        if locations:
            new_hood['landmarks'] = []
            for loc in locations:
                landmark = {
                    'name': loc.get('name', ''),
                    'description': loc.get('description', ''),
                    # Keep type if it exists, or infer? User asked for standard YAML.
                    'type': loc.get('type', 'landmark'), 
                    'address': loc.get('address', ''),
                    'link': loc.get('mapUrl', '')
                }
                # Clean up empty fields if desired? Or keep them for editing?
                # Keeping them empty is better for a template.
                new_hood['landmarks'].append(landmark)
        
        yaml_data.append(new_hood)

    print(f"Writing to {yaml_path}...")
    with open(yaml_path, 'w') as f:
        # allow_unicode=True to keep specific characters, sort_keys=False to keep order
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    
    print("Done.")

if __name__ == "__main__":
    extract_to_yaml()
