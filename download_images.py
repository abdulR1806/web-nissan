#!/usr/bin/env python3
import os
import re
import requests
from urllib.parse import unquote
import time

# Create output directory if it doesn't exist
output_dir = "readdy_images"
os.makedirs(output_dir, exist_ok=True)

# Read the HTML file
with open("artikel.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Find all image URLs using regex
# Looking for URLs in style attributes like: background-image: url('URL')
image_urls = re.findall(r"background-image:\s*url\('([^']+)'\)", html_content)

# Add any other image sources (like <img src="..."> if they exist)
img_src_urls = re.findall(r'<img\s+[^>]*src="([^"]+)"', html_content)
image_urls.extend(img_src_urls)

# Filter to only include readdy.ai URLs
readdy_urls = [url for url in image_urls if "readdy.ai" in url]

print(f"Found {len(readdy_urls)} Readdy.ai image URLs")

# Download each image
for i, url in enumerate(readdy_urls):
    try:
        # Decode URL if it's encoded
        decoded_url = unquote(url)

        # Extract a meaningful filename from the URL
        if "query=" in decoded_url:
            # Extract the query parameter
            query_match = re.search(r'query=([^&]+)', decoded_url)
            if query_match:
                # Get the first few words of the query to create a short filename
                query_text = query_match.group(1)
                # Replace URL encoding for spaces with actual spaces
                query_text = query_text.replace('%20', ' ')
                # Take first 3-4 words for the filename
                words = query_text.split(' ')
                short_name = '_'.join(words[:min(4, len(words))])
                # Clean up the filename - remove special chars and limit length
                short_name = re.sub(r'[^\w\s-]', '', short_name).strip().lower()
                short_name = re.sub(r'[-\s]+', '_', short_name)
                short_name = short_name[:30]  # Limit length

                # Add sequence number if available
                seq_match = re.search(r'seq=(\d+)', decoded_url)
                if seq_match:
                    seq_num = seq_match.group(1)
                    filename = f"{short_name}_{seq_num}.jpg"
                else:
                    filename = f"{short_name}.jpg"
            else:
                filename = f"readdy_image_{i+1}.jpg"
        else:
            # For other URLs, use the last part of the path
            filename = os.path.basename(decoded_url)
            if not filename:
                filename = f"image_{i+1}.jpg"

        # Full path to save the image
        filepath = os.path.join(output_dir, filename)

        print(f"Downloading {url} to {filepath}")

        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the image
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded {filename}")

        # Add a small delay to avoid overwhelming the server
        time.sleep(0.5)

    except Exception as e:
        print(f"Error downloading {url}: {e}")

print("Download complete!")
