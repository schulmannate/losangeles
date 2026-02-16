
import yaml
import json
import os

# Paths
yaml_path = 'data.yaml'
js_output_path = 'neighborhoods.js'

def build():
    print(f"Reading {yaml_path}...")
    
    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found.")
        return

    with open(yaml_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")
            return

    print(f"Loaded {len(data)} neighborhoods from YAML.")

    # Transform YAML structure back to JS structure expected by la.html
    # YAML: landmarks: [{name, description, type, address, link}]
    # JS: locations: [{name, description, type, address, mapUrl}]
    
    js_data = []
    
    for hood in data:
        new_hood = {
            'id': hood.get('id', ''),
            'name': hood.get('name', ''),
            'region': hood.get('region', ''),
            'description': hood.get('description', '')
        }
        
        landmarks = hood.get('landmarks', [])
        if landmarks:
            locations = []
            for mark in landmarks:
                loc = {
                    'name': mark.get('name', ''),
                    'description': mark.get('description', ''),
                    'type': mark.get('type', 'landmark'), # Default to landmark if missing
                    'address': mark.get('address', ''),
                    'mapUrl': mark.get('link', '') # Rename 'link' back to 'mapUrl'
                }
                locations.append(loc)
            
            new_hood['locations'] = locations
        else:
            new_hood['locations'] = []
            
        js_data.append(new_hood)

    # Serialize to JSON
    json_str = json.dumps(js_data, indent=4)
    
    # Wrap in JS const
    js_content = f"const neighborhoodData = {json_str};\n"

    print(f"Writing to {js_output_path}...")
    with open(js_output_path, 'w') as f:
        f.write(js_content)
        
    print("Build complete. neighborhoods.js has been updated.")

if __name__ == "__main__":
    build()
