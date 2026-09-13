$models = @("resnet50", "vgg16", "mobilenetv3")
$epochs = 15
$dataDir = "./data/dataset_split"

foreach ($model in $models) {
    Write-Host "====================================="
    Write-Host "Starting training for $model..."
    Write-Host "====================================="
    
    $logFile = "./models_output/$model/training.log"
    
    # Run the python script and redirect all output to log file and console
    C:\Users\perei\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/train_models_fast.py --model $model --data_dir $dataDir --epochs $epochs | Tee-Object -FilePath $logFile
    
    Write-Host "Finished training $model. Log saved to $logFile"
    Write-Host ""
}
