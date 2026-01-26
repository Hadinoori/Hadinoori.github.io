import os
import json
import re
from datetime import datetime

# Configuration
SOURCE_DIR = '_insights'
OUTPUT_FILE = 'insights.json'

def parse_frontmatter(content):
    # Extract YAML frontmatter
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    
    yaml_text = match.group(1)
    metadata = {}
    
    # Simple line-by-line parsing (Robust enough for your CMS)
    for line in yaml_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            metadata[key] = value
            
    return metadata

def build_json():
    posts = []
    
    if not os.path.exists(SOURCE_DIR):
        print(f"Directory {SOURCE_DIR} not found.")
        return

    # Loop through all .md files
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(SOURCE_DIR, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            meta = parse_frontmatter(content)
            
            # Skip if no title found
            if 'title' not in meta:
                continue

            # Calculate Slug and Link
            slug = filename.replace('.md', '')
            external_url = meta.get('external_url')
            final_link = external_url if external_url else f"/insights/{slug}.html"
            
            # Create post object
            post = {
                'title': meta.get('title', 'Untitled'),
                'date': meta.get('date', ''),
                'description': meta.get('description', ''),
                'external_url': external_url,
                'url': final_link,
                'is_external': bool(external_url)
            }
            posts.append(post)

    # Sort by date (Newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)

    # Write to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated {OUTPUT_FILE} with {len(posts)} posts.")

if __name__ == "__main__":
    build_json()
