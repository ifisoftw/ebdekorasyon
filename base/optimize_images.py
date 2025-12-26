import os
from PIL import Image

ARTIFACT_DIR = "/Users/macbook/.gemini/antigravity/brain/d83be39d-dabf-4dca-86e7-ee15b7e6273c"
BASE_MEDIA_DIR = "/Users/macbook/Documents/Django Projects/Django Projects/Bussiness/EB Dekorasyon/base/media/uploads"

# Map artifact filenames (partial match) to target filenames (relative to BASE_MEDIA_DIR)
# Value can be a string or a list of strings
files_map = {
    "default_service_hero": ["service_default.jpg", "projects/project_flooring_main.jpg"],
    "default_before": ["defaults/default_before.jpg", "projects/project_renovation_before.jpg", "projects/project_flooring_before.jpg"],
    "default_after": ["defaults/default_after.jpg", "projects/project_renovation_after.jpg"],
    
    # Kitchen Project
    "luxury_kitchen_renovation_white": "projects/project_kitchen_main.jpg",
    "project_kitchen_before": "projects/project_kitchen_before.jpg",
    "mutfak_dolabi_result": "projects/project_kitchen_after.jpg",

    # Renovation Project (Main)
    "modern_salon_istanbul": "projects/project_renovation_main.jpg",
    
    # Flooring Project (After)
    "bedroom_remodel_peaceful": ["projects/project_flooring_after.jpg", "projects/project_office_flooring_main.jpg"], # Reuse specifically
    
    # Bathroom Project
    "bathroom_modern_tiles": ["projects/project_bathroom_main.jpg", "projects/project_bathroom_after.jpg"],
    
    # Bedroom Project
    "yatak_odasi_boyama_new": ["projects/project_bedroom_main.jpg", "projects/project_bedroom_after.jpg"],
    
    # Office Project (reuse hero as main)
    "default_service_hero": ["service_default.jpg", "projects/project_office_flooring_main.jpg", "projects/project_office_flooring_after.jpg", "projects/project_flooring_main.jpg"],

    # Reusing default before for multiple matching "old" states where specific one missing
    "default_before": [
        "defaults/default_before.jpg", 
        "projects/project_renovation_before.jpg", 
        "projects/project_flooring_before.jpg",
        "projects/project_bathroom_before.jpg",
        "projects/project_bedroom_before.jpg",
        "projects/project_office_flooring_before.jpg"
    ]
}

def compress_image(source_path, target_path, max_size_kb=80):
    img = Image.open(source_path)
    
    # Resize first to a reasonable web size if too large (e.g., width 1200px)
    if img.width > 1200:
        ratio = 1200 / img.width
        new_height = int(img.height * ratio)
        img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Binary search for quality
    low, high = 1, 95
    best_quality = 50
    
    # Initial save to check size
    img.save(target_path, "JPEG", quality=85, optimize=True)
    if os.path.getsize(target_path) / 1024 < max_size_kb:
        print(f"✅ {target_path} saved at 85 quality. Size: {os.path.getsize(target_path)/1024:.2f} KB")
        return

    # If too big, compress hard
    while low <= high:
        mid = (low + high) // 2
        img.save(target_path, "JPEG", quality=mid, optimize=True)
        size_kb = os.path.getsize(target_path) / 1024
        
        if size_kb < max_size_kb:
            best_quality = mid
            low = mid + 1
        else:
            high = mid - 1
            
    img.save(target_path, "JPEG", quality=best_quality, optimize=True)
    print(f"✅ {target_path} saved at {best_quality} quality. Size: {os.path.getsize(target_path)/1024:.2f} KB")

# Find files in artifact dir and process
found_files = 0
for filename in os.listdir(ARTIFACT_DIR):
    for key, targets in files_map.items():
        if key in filename and filename.endswith(".png"):
            source = os.path.join(ARTIFACT_DIR, filename)
            
            # Identify if targets is list or string
            if isinstance(targets, str):
                targets = [targets]
            
            for target_name in targets:
                target = os.path.join(BASE_MEDIA_DIR, target_name)
                # Ensure target directory exists
                os.makedirs(os.path.dirname(target), exist_ok=True)
                
                print(f"Processing {source} -> {target}")
                compress_image(source, target)
                found_files += 1

if found_files == 0:
    print("❌ No matching files found in artifact directory!")
else:
    print(f"Total {found_files} images processed.")
