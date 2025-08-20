import os
import subprocess
import shutil

SRC_DIR = 'downloaded_images'
DEST_DIR = 'converted_images'
os.makedirs(DEST_DIR, exist_ok=True)

for chapter in os.listdir(SRC_DIR):
    chapter_path = os.path.join(SRC_DIR, chapter)
    if not os.path.isdir(chapter_path):
        continue

    try:
        chap_num = int(chapter)
    except ValueError:
        print(f"Skipping non-numeric folder: {chapter}")
        continue

    jpg_files = [f for f in os.listdir(chapter_path) if f.lower().endswith('.jpg')]
    if not jpg_files:
        print(f"No JPGs found in {chapter_path}, skipping.")
        continue

    if chap_num > 80:
        prefix = "boruto-two-blue-vortex"
        out_num = chap_num - 80
        out_name = f"{prefix}-{out_num:02d}.cbr"
    else:
        prefix = "boruto-next-generations"
        out_name = f"{prefix}-{chap_num}.cbr"

    out_path = os.path.join(DEST_DIR, out_name)
    temp_cbr_path = os.path.join(chapter_path, out_name)

    # Skip if .cbr already exists in converted_images
    if os.path.exists(out_path):
        print(f"{out_name} already exists, skipping.")
        continue

    # Create .cbr in chapter folder
    cmd = ['rar', 'a', '-ep', out_name] + jpg_files
    try:
        subprocess.run(cmd, cwd=chapter_path, check=True)
        shutil.move(temp_cbr_path, out_path)
        print(f"Created {out_name} from {chapter_path}")
    except Exception as e:
        print(f"Failed to create {out_name} for {chapter_path}: {e}")