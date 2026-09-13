Write-Host "=========================================="
Write-Host "PHASE 1: Splitting Dataset (80/20)"
Write-Host "=========================================="
C:\Users\perei\AppData\Local\Python\pythoncore-3.14-64\python.exe .\scripts\prepare_dataset.py --src ./data/raw_images --dest ./data/dataset_split

Write-Host "=========================================="
Write-Host "PHASE 2: Multi-Model Training (15 Epochs)"
Write-Host "=========================================="
powershell -ExecutionPolicy Bypass -File .\scripts\run_all_experiments.ps1

Write-Host "=========================================="
Write-Host "PIPELINE COMPLETE!"
Write-Host "=========================================="
