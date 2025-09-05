#!/usr/bin/env python3
"""
Fragment Generator

This script helps generate new fragments for the Unuseful project.
It updates the data.js file with new fragments while maintaining the existing ones.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import re

def load_data_js(file_path):
    """Load the existing data.js file and parse the FRAGMENTS_DATA object."""
    content = file_path.read_text(encoding='utf-8')
    # Extract the JSON part between 'FRAGMENTS_DATA = ' and the trailing semicolon
    match = re.search(r'FRAGMENTS_DATA = ({.*?});', content, re.DOTALL)
    if not match:
        return {"fragments": []}
    return json.loads(match.group(1))

def save_data_js(file_path, data):
    """Save the updated data back to data.js."""
    content = f"// Fragment data embedded directly in JavaScript\nconst FRAGMENTS_DATA = {json.dumps(data, indent=2)};"
    file_path.write_text(content, encoding='utf-8')

def get_next_id(fragments):
    """Get the next available fragment ID."""
    if not fragments:
        return 1
    return max(f["id"] for f in fragments) + 1

def add_fragment(file_path, source_code, title, patterns, source_info):
    """Add a new fragment to data.js."""
    data = load_data_js(file_path)
    
    new_fragment = {
        "id": get_next_id(data["fragments"]),
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "source": source_info,
        "content": source_code,
        "file_type": "python",  # Assuming Python for now
        "patterns": ",".join(patterns),
        "size": len(source_code.encode('utf-8'))
    }
    
    # Add the new fragment at the start (newest first)
    data["fragments"].insert(0, new_fragment)
    save_data_js(file_path, data)
    return new_fragment["id"]

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_fragment.py <source_file> <title> [pattern1,pattern2,...]")
        print("Example: generate_fragment.py my_code.py 'Pattern Analysis' 'struttura oggettuale,modello cognitivo'")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    title = sys.argv[2]
    patterns = sys.argv[3].split(',') if len(sys.argv) > 3 else []
    
    if not source_file.exists():
        print(f"Error: Source file {source_file} not found")
        sys.exit(1)
    
    # Read the source code
    source_code = source_file.read_text(encoding='utf-8')
    
    # Prepare source info
    source_info = {
        "repo": "https://github.com/fabriziosalmi/unuseful",
        "path": str(source_file),
        "keyword": ""  # Could be extracted from content
    }
    
    # Find data.js in the project
    data_js = Path(__file__).parent.parent / 'docs' / 'js' / 'data.js'
    if not data_js.exists():
        print(f"Error: data.js not found at {data_js}")
        sys.exit(1)
    
    # Add the fragment
    fragment_id = add_fragment(data_js, source_code, title, patterns, source_info)
    print(f"Fragment added successfully with ID: {fragment_id}")

if __name__ == "__main__":
    main()
