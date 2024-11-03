import os
import json
from PIL import Image
from datetime import datetime
import piexif

# Paths to JSON files and photo directory
photos_dir = r"C:\bereal\Photos\post"
# memories_json_path = r"C:\bereal\memories.json"
posts_json_path = r"C:\bereal\posts.json"
output_dir = r"C:\bereal\ProcessedPhotos"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Load JSON data from momories
#with open(memories_json_path, 'r', encoding='utf-8') as f:
#    memories_data = json.load(f)

# Load JSON data from posts
with open(posts_json_path, 'r', encoding='utf-8') as f:
    posts_data = json.load(f)

def add_exif_piexif(timestamp_str):
    # Convert timestamp to EXIF-compatible format
    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    exif_time_str = timestamp.strftime("%Y:%m:%d %H:%M:%S")

    # Create EXIF dictionary
    exif_dict = {"Exif": {}, "0th": {}}
    
    # Set DateTimeOriginal, DateTimeDigitized, and DateTime
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = exif_time_str
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = exif_time_str
    exif_dict["0th"][piexif.ImageIFD.DateTime] = exif_time_str

    # Convert EXIF dictionary to bytes
    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes

# Process each entry
for item in posts_data:
    # Determine image paths and timestamps
    primary_path = item.get("primary")["path"]
    secondary_path = item.get("secondary")["path"]
    timestamp = item.get("takenAt")

    # Load images
    primary_img_path = os.path.join(photos_dir, os.path.basename(primary_path))
    secondary_img_path = os.path.join(photos_dir, os.path.basename(secondary_path))
    
    if not os.path.exists(primary_img_path) or not os.path.exists(secondary_img_path):
        print(f"Missing files: {primary_img_path} or {secondary_img_path}")
        continue

    primary_img = Image.open(primary_img_path)
    secondary_img = Image.open(secondary_img_path)
    
    # Combine images horizontally
    combined_width = primary_img.width + secondary_img.width
    combined_height = max(primary_img.height, secondary_img.height)
    combined_img = Image.new("RGB", (combined_width, combined_height))
    combined_img.paste(primary_img, (0, 0))
    combined_img.paste(secondary_img, (primary_img.width, 0))

    # Add EXIF data
    exif_data = add_exif_piexif(timestamp)
    
    # Save the final image with EXIF data
    output_path = os.path.join(output_dir, f"{os.path.basename(primary_path)}_combined.jpg")
    combined_img.save(output_path, "JPEG", exif=exif_data)
    print(f"Saved combined image: {output_path}")