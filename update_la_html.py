
import re

la_path = 'la.html'

def update_la_html():
    print("Reading la.html...")
    with open(la_path, 'r') as f:
        content = f.read()

    # 1. Remove inline data
    # Look for: const neighborhoodData = [ ... ];
    # Use re.DOTALL to match across lines
    pattern = r'const neighborhoodData = \[\s*\{.*?\n\];'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print("Found inline neighborhoodData. Removing...")
        content = content[:match.start()] + "// Data loaded from neighborhoods.js" + content[match.end():]
    else:
        print("Inline neighborhoodData not found (checked regex).")

    # 2. Add script tag if missing
    if '<script src="neighborhoods.js"></script>' not in content:
        print("Adding script tag...")
        # Find the main script tag or close of body
        # The main script starts with <script> and contains logic. 
        # But we want to load data BEFORE the main script logic runs.
        # Actually, since neighborhoodData is used inside the DOMContentLoaded event, 
        # loading it just before the main script block is fine.
        
        # We look for the script that contains "document.addEventListener" or just the last script tag?
        # In this file, there is a script block starting around line 613.
        # We can insert before that specific script block.
        
        # Regex to find the script tag that starts the logic block (which originally contained the data)
        # It starts with <script> and then has the implementation. 
        # Since we removed the data, it now starts with empty space or comments.
        
        # Simpler approach: Insert before </body> if we can ensure it's loaded? 
        # No, `neighborhoodData` is used in the main script which is inline. 
        # So we MUST load neighborhoods.js BEFORE that inline script.
        
        # Let's find the inline script tag. It's likely the last large script tag.
        # We can look for <script> followed by "document.addEventListener"
        
        script_pattern = r'<script>\s*// --- 2. LOGIC ---' 
        # Wait, the original file had "// --- 1. DATASET ---" then data.
        # I removed data. The comments might still be there if I wasn't careful with regex.
        # My regex `const neighborhoodData = ... ];` likely left the surrounding comments.
        # So the file now has `<script> ... // --- 1. DATASET --- ... // Data loaded ... // --- 2. LOGIC ---`
        
        # This means we are INSIDE a script tag.
        # Converting `const neighborhoodData` to an external file means `neighborhoods.js` must be loaded *before* this script tag.
        
        # So, we need to:
        # A) Close the script tag before the logic? 
        #    <script src="neighborhoods.js"></script>
        #    <script> ... logic ... </script>
        # B) Or just load it before.
        
        # The current file structure is:
        # <script>
        #   const neighborhoodData = [...];
        #   ... logic ...
        # </script>
        
        # If I just remove the data, `neighborhoodData` is not defined in that scope.
        # If I add `<script src="neighborhoods.js">` *before* this script block, `neighborhoodData` will be a global variable.
        # The inline script can then access it.
        
        # So I need to find `<script>` that contains the code.
        # It's the one that had `const neighborhoodData`.
        # I can find the insertion point by looking for that distinct comment structure or just before `<script>` tag that matches.
        
        # Let's find `<script>` that is followed by `// --- 1. DATASET ---` (or similar)
        # We can replace `<script>` with `<script src="neighborhoods.js"></script>\n<script>`
        
        # But wait, looking at the file earlier, the script tag was:
        # <script>
        #    // --- 1. DATASET ---
        
        match_script = re.search(r'(<script>)(\s*// --- 1. DATASET ---)', content)
        if match_script:
            print("Found main script tag start. Inserting external script ref before it.")
            injection = '<script src="neighborhoods.js"></script>\n'
            # We replace `<script>` with `<script src...><script>`
            # But wait, the original `<script>` is needed for the legacy code (logic).
            replacement = injection + match_script.group(1) + match_script.group(2)
            content = content.replace(match_script.group(0), replacement)
        else:
             print("Could not find exact script start. Inserting before body close as fallback (might risk ordering issues).")
             # Fallback
             content = content.replace('</body>', '<script src="neighborhoods.js"></script>\n</body>')
    
    print("Writing updated la.html...")
    with open(la_path, 'w') as f:
        f.write(content)
    print("Done.")

if __name__ == "__main__":
    update_la_html()
