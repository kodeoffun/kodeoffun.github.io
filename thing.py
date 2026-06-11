import os
import re

# This regex looks for image files (.jpg, .png, etc.) inside src="..." or url(...)
# It ignores paths that already start with "http", "assets/", or "/"
extensions = r'\.(jpg|jpeg|png|gif|webp|svg)'

# Matches: src="image.JPG"
src_pattern = re.compile(r'src="(?!(?:http|assets/|/))([^"]+' + extensions + r')"', re.IGNORECASE)

# Matches: url('image.JPG') or url("image.JPG")
url_pattern = re.compile(r'url\([\'"]?(?!(?:http|assets/|/))([^\'")]+' + extensions + r')[\'"]?\)', re.IGNORECASE)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Add assets/ to src=""
    new_content = src_pattern.sub(r'src="assets/\1"', content)
    
    # Add assets/ to url()
    new_content = url_pattern.sub(r"url('assets/\1')", new_content)

    # Only overwrite the file if changes were actually made
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"✅ Updated image paths in: {filepath}")

# Scan all files in the directory and subdirectories
files_changed = 0
for root, dirs, files in os.walk('.'):
    # Skip the hidden .git folder
    if '.git' in root:
        continue
        
    for filename in files:
        if filename.endswith('.html') or filename.endswith('.css'):
            update_file(os.path.join(root, filename))
            files_changed += 1

print("\n🎉 All done! Image paths have been updated.")