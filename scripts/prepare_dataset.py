import os
import shutil
import random
import argparse

def split_dataset(source_dir, output_dir, split_ratio=0.8, seed=42):
    """
    Splits a raw folder of categorized images into train and validation sets.
    
    Expected source structure:
        source_dir/
            benign/
                img1.jpg, img2.png ...
            weapons/
                img3.jpg, img4.png ...
                
    Generated output structure:
        output_dir/
            train/
                benign/
                weapons/
            val/
                benign/
                weapons/
    """
    random.seed(seed)
    
    # Ensure source directory exists
    if not os.path.exists(source_dir):
        print(f"[Error] Source directory '{source_dir}' does not exist.")
        return
        
    categories = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    print(f"[Info] Found categories: {categories}")
    
    # Create target directories
    for split in ['train', 'val']:
        for cat in categories:
            os.makedirs(os.path.join(output_dir, split, cat), exist_ok=True)
            
    for cat in categories:
        cat_src_dir = os.path.join(source_dir, cat)
        files = []
        for root, _, filenames in os.walk(cat_src_dir):
            for f in filenames:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    # Store tuple of (full_path, filename) to copy correctly
                    files.append((os.path.join(root, f), f))
        
        # Shuffle files randomly
        random.shuffle(files)
        
        split_idx = int(len(files) * split_ratio)
        train_files = files[:split_idx]
        val_files = files[split_idx:]
        
        print(f"Category '{cat}': Total={len(files)} -> Train={len(train_files)}, Val={len(val_files)}")
        
        # Copy files to train directory
        for full_path, filename in train_files:
            dest_file = os.path.join(output_dir, 'train', cat, filename)
            shutil.copy2(full_path, dest_file)
            
        # Copy files to val directory
        for full_path, filename in val_files:
            dest_file = os.path.join(output_dir, 'val', cat, filename)
            shutil.copy2(full_path, dest_file)
            
    print(f"\n[Success] Dataset split successfully! Saved to '{output_dir}'")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split raw images into train/val datasets")
    parser.add_argument('--src', type=str, default='./raw_images', help="Path to raw unsplit images folder")
    parser.add_argument('--dest', type=str, default='./dataset', help="Path to write split dataset")
    parser.add_argument('--ratio', type=float, default=0.8, help="Train split ratio (e.g. 0.8)")
    
    args, unknown = parser.parse_known_args()
    
    split_dataset(source_dir=args.src, output_dir=args.dest, split_ratio=args.ratio)
