import os
from icrawler.builtin import BingImageCrawler

# Configuration
# Expanding queries significantly to reach ~5000 images total (roughly 1600 per category)
CATEGORIES = {
    'weapons': [
        'handgun weapon', 'assault rifle weapon', 'combat knife', 'revolver gun', 'shotgun firearm',
        'sniper rifle', 'm16 rifle', 'glock pistol', 'hunting knife', 'switchblade', 
        'uzi submachine gun', 'ar-15 rifle', 'machete weapon', 'tactical knife', 'ak-47 rifle'
    ],
    'drugs': [
        'cocaine powder', 'prescription pills', 'heroin syringe', 'meth crystals', 'ecstasy pills',
        'marijuana buds', 'cannabis plant', 'fentanyl pills', 'oxycodone pills', 'MDMA powder',
        'magic mushrooms', 'crack cocaine rocks', 'lsd tabs', 'drug paraphernalia', 'syringe needle drugs'
    ],
    'alcohol': [
        'beer bottles', 'wine glass', 'liquor bottle', 'whiskey glass', 'vodka bottle',
        'champagne bottle', 'tequila shot', 'rum bottle', 'gin and tonic', 'margarita cocktail',
        'craft beer cans', 'wine cellar bottles', 'bar drinks line', 'cognac glass', 'martini'
    ]
}
IMAGES_PER_QUERY = 120 # 15 queries * 120 = 1800 images per category maximum
BASE_DIR = './data/raw_images'

def scrape_images():
    print(f"Starting MASSIVE multi-threaded dataset download using icrawler...")
    
    # Ensure directories exist
    for category in CATEGORIES:
        os.makedirs(os.path.join(BASE_DIR, category), exist_ok=True)
    
    for category, queries in CATEGORIES.items():
        print(f"\\n--- Processing Category: {category.upper()} ---")
        category_dir = os.path.join(BASE_DIR, category)
        
        for i, query in enumerate(queries):
            print(f"Searching Bing for: '{query}'")
            
            crawler = BingImageCrawler(
                downloader_threads=5, # Increase threads slightly
                storage={'root_dir': category_dir},
                log_level=30
            )
            crawler.storage.file_prefix = f"{category}_v2_{i}_"
            
            crawler.crawl(
                keyword=query,
                max_num=IMAGES_PER_QUERY
            )
            
        print(f"Finished crawling queries for {category}.")
            
if __name__ == "__main__":
    scrape_images()
