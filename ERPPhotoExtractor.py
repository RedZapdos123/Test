#A python program to download student photos from IIITA ERP system based on roll numbers.
#It reads roll numbers from a text file, constructs URLs, and downloads images.
#It also logs any missing images based on HTTP status and Content-Type checks.

import os
import requests
import time

#The configurartions.
#Path to the .txt file with one roll per line
ROLL_FILE_PATH     = r"C:\Users\Xeron\OneDrive\Desktop\roll_numbers.txt"\
#The output folder for images and logs.
OUTPUT_DIR         = r"C:\Users\Xeron\OneDrive\Desktop\ERPPhotos"          
IMAGES_DIR         = os.path.join(OUTPUT_DIR, "images")
MISSING_LOG_PATH   = os.path.join(OUTPUT_DIR, "missing_rolls.txt")
#The URL for fetching student photos.
BASE_URL           = "https://erp.iiita.ac.in/uploads/iiita/photos/"
#The header to mimic a browser request.
HEADERS            = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
#The fixed delay between requests to avoid overwhelming the server, and raising suspicion.
FIXED_DELAY        = 0.25  

#Ensure that output directories exist.
os.makedirs(IMAGES_DIR, exist_ok=True)

#Create the missing-rolls log file
with open(MISSING_LOG_PATH, "w") as log_f:
    log_f.write("")  #Overwrite the file if exists.

#Read the roll numbers from the text file.
with open(ROLL_FILE_PATH, "r") as f:
    rolls = [line.strip() for line in f if line.strip()]

print(f"Found {len(rolls)} roll numbers. Starting download...\n")

for roll_raw in rolls:
    #Normalize to lowercase and append .jpg.
    roll     = roll_raw.lower()
    filename = f"{roll}.jpg"
    url      = BASE_URL + filename
    save_path = os.path.join(IMAGES_DIR, filename)

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        #Check HTTP status.
        if response.status_code != 200:
            print(f"[x] Missing (HTTP {response.status_code}): {filename}")
            with open(MISSING_LOG_PATH, "a") as log_f:
                log_f.write(f"{roll}\n")
        else:
            #Verify Content-Type is an actual image.
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                #Received a non-image (likely HTML 200 page), treat as missing.
                print(f"[x] Missing or invalid (Content-Type: {content_type}): {filename}")
                with open(MISSING_LOG_PATH, "a") as log_f:
                    log_f.write(f"{roll}\n")
            else:
                #Valid image being found so save to disk.
                with open(save_path, "wb") as img_file:
                    img_file.write(response.content)
                print(f"[✓] Downloaded: {filename}")

    except Exception as e:
        print(f"[!] Error fetching {filename}: {e}")
        with open(MISSING_LOG_PATH, "a") as log_f:
            log_f.write(f"{roll}\n")

    #The fixed delay to avoid overwhelming the server.
    print(f"Sleeping for {FIXED_DELAY:.2f} seconds...\n")
    time.sleep(FIXED_DELAY)

print("Scraping complete.")
print(f"Downloaded images are in: {IMAGES_DIR}")
print(f"Missing roll numbers are logged in: {MISSING_LOG_PATH}")
