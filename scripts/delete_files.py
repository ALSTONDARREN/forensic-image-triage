import os
import shutil

dir_path = r'C:\Users\perei\Documents\thesis\data\raw_images\alcohol'
count = 0
for f in os.listdir(dir_path):
    f_lower = f.lower()
    if 'smoke' in f_lower or 'cig' in f_lower:
        file_path = os.path.join(dir_path, f)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
        count += 1
print(f'Deleted {count} items.')
