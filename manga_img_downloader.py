import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# === Configuration ===
BASE_URL = 'https://read-borutomanga.com/manga/boruto-two-blue-vortex-chapter-{}/'
# BASE_URL = 'https://read-borutomanga.com/manga/boruto-naruto-next-generations-chapter-{}/'
START_CHAPTER = 24
END_CHAPTER = 25

for chapter in range(START_CHAPTER, END_CHAPTER + 1):
    URL = BASE_URL.format(chapter)
    if "two-blue-vortex" in BASE_URL:
        OUTPUT_DIR = f'downloaded_images/{chapter+80}'
    else:
        OUTPUT_DIR = f'downloaded_images/{chapter}'

    # === Skip if output directory already exists ===
    if os.path.exists(OUTPUT_DIR):
        print(f"Folder {OUTPUT_DIR} already exists, skipping chapter {chapter}.")
        continue

    # === Create output directory ===
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # === Fetch the page ===
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to load page {chapter}: {response.status_code}")
        continue

    # === Parse the page ===
    soup = BeautifulSoup(response.text, 'html.parser')
    entry_content = soup.find('div', class_='entry-content')

    if not entry_content:
        print(f"No div with class 'entry-content' found for chapter {chapter}.")
        continue

    # === Find all image tags within entry-content ===
    img_tags = entry_content.find_all('img')

    # === Download each image ===
    for idx, img in enumerate(img_tags, 1):
        img_url = img.get('src')
        if not img_url:
            continue

        # Make image URL absolute if needed
        img_url = urljoin(URL, img_url)
        parsed = urlparse(img_url)
        img_name = os.path.basename(parsed.path)

        # If there's no filename, make one up
        if not img_name:
            img_name = f'image_{idx}.jpg'

        # Download and save image
        img_path = os.path.join(OUTPUT_DIR, img_name)
        try:
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print(f'Chapter {chapter}: Downloaded {img_url} -> {img_path}')
        except Exception as e:
            print(f'Chapter {chapter}: Failed to download {img_url}: {e}')