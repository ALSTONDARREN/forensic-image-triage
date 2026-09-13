import os
import shutil
import cv2
import glob
from icrawler.builtin import BingImageCrawler

# Configuration
DATA_DIR = r"C:\Users\perei\Documents\thesis\data\dataset_split"
DRUG_QUERIES = [
    "LSD acid tabs",
    "Morphine medical vial",
    "Cannabis weed bud",
    "Nicotine vape device",
    "Cocaine white powder bag",
    "Heroin syringe needle",
    "Methamphetamine crystal meth",
    "MDMA ecstasy colorful pills",
    "Fentanyl powder",
    "Ketamine powder vial",
    "Psilocybin magic mushrooms dried",
    "Crack cocaine rocks",
    "Amphetamine speed pills"
]

MAX_IMAGES_PER_QUERY = 15

def main():
    print("Starting Massive Drug Image Scraper using Bing...")
    train_dir = os.path.join(DATA_DIR, 'train', 'drugs')
    val_dir = os.path.join(DATA_DIR, 'val', 'drugs')
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    
    # Temporary download directory
    temp_dir = os.path.join(DATA_DIR, "temp_downloads")
    os.makedirs(temp_dir, exist_ok=True)
    
    total_downloaded = 0
    
    for query in DRUG_QUERIES:
        print(f"\n=================================")
        print(f"Scraping images for: '{query}'")
        print(f"=================================")
        
        # Clear temp dir
        for f in glob.glob(os.path.join(temp_dir, "*")):
            os.remove(f)
            
        bing_crawler = BingImageCrawler(storage={'root_dir': temp_dir})
        bing_crawler.crawl(keyword=query, max_num=MAX_IMAGES_PER_QUERY)
        
        # Process downloaded images
        downloaded_files = glob.glob(os.path.join(temp_dir, "*.*"))
        for file_path in downloaded_files:
            try:
                img = cv2.imread(file_path)
                if img is None:
                    continue
                
                # Resize and save
                img = cv2.resize(img, (256, 256))
                
                # Create clean filename
                safe_query = query.replace(" ", "_")
                filename = f"{safe_query}_{total_downloaded}.jpg"
                
                # Split 80/20 train/val
                if total_downloaded % 5 == 0:
                    dest = os.path.join(val_dir, filename)
                else:
                    dest = os.path.join(train_dir, filename)
                    
                cv2.imwrite(dest, img)
                total_downloaded += 1
                
            except Exception as e:
                print(f"Failed processing image: {e}")
                
    # Cleanup temp
    shutil.rmtree(temp_dir)
    print(f"\n[SUCCESS] Scraping complete! Added {total_downloaded} new drug images to the dataset.")

if __name__ == "__main__":
    main()
