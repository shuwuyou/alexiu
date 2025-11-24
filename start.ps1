# Quick Start Script for Player Analytics System
# This script starts both the backend API and frontend dev server

Write-Host "==================================" -ForegroundColor Cyan
Write-Host " Player Analytics Quick Start" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

# Check if required packages are installed
Write-Host "Checking Python dependencies..." -ForegroundColor Green
$packages = @("fastapi", "uvicorn", "pandas", "numpy")
foreach ($package in $packages) {
    python -c "import $package" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing missing package: $package" -ForegroundColor Yellow
        pip install $package
    }
}

# Check if node_modules exists in frontend
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Green
    Set-Location frontend
    npm install
    Set-Location ..
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host " Starting Services" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Start backend API in background
Write-Host ""
Write-Host "Starting Backend API on http://localhost:8000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; python -m uvicorn src.api.main:app --reload --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend dev server in background  
Write-Host "Starting Frontend Dev Server on http://localhost:5173" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

# Wait for services to fully start
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host " Services Started Successfully!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available Players: 1,451 players with complete ML model data" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test Players (searchable):" -ForegroundColor Yellow
Write-Host "  - Jonas Hofmann (ID: 7161)" -ForegroundColor White
Write-Host "  - Lionel Carole (ID: 11530)" -ForegroundColor White
Write-Host "  - Search by name or ID in the webapp" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop this script (services will continue running)" -ForegroundColor Gray
Write-Host "Close the opened PowerShell windows to stop the services" -ForegroundColor Gray

# Keep script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} catch {
    Write-Host "Stopping..." -ForegroundColor Yellow
}
