#!/usr/bin/env python3
import re

# Read the HTML file
with open("artikel.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Define a function to replace URLs with local paths
def replace_url_with_local(match):
    url = match.group(1)
    
    # Skip if not a readdy.ai URL
    if "readdy.ai" not in url:
        return f"background-image: url('{url}')"
    
    # Extract sequence number if available
    seq_match = re.search(r'seq=(\d+)', url)
    if not seq_match:
        return f"background-image: url('{url}')"  # Keep original if no seq
    
    seq_num = seq_match.group(1)
    
    # Extract query parameter to find the right file
    query_match = re.search(r'query=([^&]+)', url)
    if not query_match:
        return f"background-image: url('{url}')"  # Keep original if no query
    
    query_text = query_match.group(1)
    query_text = query_text.replace('%20', ' ')
    words = query_text.split(' ')
    short_name = '_'.join(words[:min(4, len(words))])
    short_name = re.sub(r'[^\w\s-]', '', short_name).strip().lower()
    short_name = re.sub(r'[-\s]+', '_', short_name)
    short_name = short_name[:30]  # Limit length
    
    # Construct the local filename
    local_filename = f"readdy_images/{short_name}_{seq_num}.jpg"
    
    return f"background-image: url('{local_filename}')"

# Replace background-image URLs
updated_html = re.sub(r"background-image:\s*url\('([^']+)'\)", replace_url_with_local, html_content)

# Write the updated HTML back to the file
with open("artikel.html", "w", encoding="utf-8") as f:
    f.write(updated_html)

print("Updated all Readdy.ai image URLs in artikel.html")
