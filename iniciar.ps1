Write-Host "Iniciando WhatsApp IA..." -ForegroundColor Green

Write-Host "Iniciando FastAPI..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --reload"

Start-Sleep -Seconds 3

Write-Host "Iniciando ngrok..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 8000"

Write-Host ""
Write-Host "Projeto iniciado!" -ForegroundColor Green
Write-Host "FastAPI: http://127.0.0.1:8000"
Write-Host "Documentacao: http://127.0.0.1:8000/docs"