import os
import json
from PIL import Image, ExifTags, PngImagePlugin
from datetime import datetime

# Paths to JSON files and photo directory
photos_dir = r"C:\bereal\Photos\post"
memories_json_path = r"C:\bereal\memories.json"
posts_json_path = r"C:\bereal\posts.json"
output_dir = r"C:\bereal\ProcessedPhotos"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Load JSON data
with open(memories_json_path, 'r', encoding='utf-8') as f:
    memories_data = json.load(f)

with open(posts_json_path, 'r', encoding='utf-8') as f:
    posts_data = json.load(f)

# Function to add EXIF data
from PIL import Image, ExifTags
from datetime import datetime

# Add this inside the add_exif function
def add_exif(img, timestamp_str):
    # Convert timestamp to EXIF-compatible format
    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    exif_time_str = timestamp.strftime("%Y:%m:%d %H:%M:%S")

    # Prepare EXIF data dictionary
    exif_data = img.getexif()  # Get current EXIF data if available

    # Get EXIF tags for DateTimeOriginal, DateTimeDigitized, and DateTime
    date_time_original_tag = next(tag for tag, name in ExifTags.TAGS.items() if name == "DateTimeOriginal")
    date_time_digitized_tag = next(tag for tag, name in ExifTags.TAGS.items() if name == "DateTimeDigitized")
    date_time_tag = next(tag for tag, name in ExifTags.TAGS.items() if name == "DateTime")

    # Set all three tags to ensure compatibility with Windows "Date taken"
    exif_data[date_time_original_tag] = exif_time_str
    exif_data[date_time_digitized_tag] = exif_time_str
    exif_data[date_time_tag] = exif_time_str

    return exif_data

# Process each entry
for item in memories_data + posts_data:  # Combines both memories and posts
    # Determine image paths and timestamps
    primary_path = item.get("frontImage", item.get("primary"))["path"]
    secondary_path = item.get("backImage", item.get("secondary"))["path"]
    timestamp = item.get("takenTime", item.get("takenAt"))

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
    exif_data = add_exif(combined_img, timestamp)
    
    # Save the final image with EXIF data
    output_path = os.path.join(output_dir, f"{os.path.basename(primary_path)}_combined.jpg")
    exif_data = add_exif(combined_img, timestamp)
    combined_img.save(output_path, "JPEG", exif=exif_data)
    print(f"Saved combined image: {output_path}")
