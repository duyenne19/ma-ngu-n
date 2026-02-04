# TikiShop - Setup Script (Windows PowerShell)
# Tự động cài đặt dependencies và khởi tạo project

Write-Host "================================" -ForegroundColor Cyan
Write-Host "TikiShop - Automated Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Kiểm tra Python
Write-Host "`n[1/5] Kiểm tra Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python không được cài đặt. Vui lòng cài đặt Python 3.10+" -ForegroundColor Red
    exit 1
}

# Tạo Virtual Environment
Write-Host "`n[2/5] Tạo Virtual Environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "✓ Virtual Environment đã tồn tại" -ForegroundColor Green
} else {
    python -m venv .venv
    Write-Host "✓ Virtual Environment được tạo" -ForegroundColor Green
}

# Kích hoạt Virtual Environment
Write-Host "`n[3/5] Kích hoạt Virtual Environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✓ Virtual Environment được kích hoạt" -ForegroundColor Green

# Cài đặt Dependencies
Write-Host "`n[4/5] Cài đặt Dependencies (có thể mất 1-2 phút)..." -ForegroundColor Yellow
pip install -q -r requirements.txt
Write-Host "✓ Dependencies được cài đặt" -ForegroundColor Green

# Chạy Migrations
Write-Host "`n[5/5] Chạy Migrations..." -ForegroundColor Yellow
python manage.py migrate --quiet
Write-Host "✓ Migrations hoàn tất" -ForegroundColor Green

# Xong
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✓ SETUP HOÀN TẤT!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan

Write-Host "`nBước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. Tạo tài khoản Admin (nếu chưa có):" -ForegroundColor Gray
Write-Host "   python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Khởi động Server:" -ForegroundColor Gray
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Truy cập:" -ForegroundColor Gray
Write-Host "   - Trang chủ: http://127.0.0.1:8000/" -ForegroundColor Gray
Write-Host "   - Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Gray
Write-Host "   - Dashboard: http://127.0.0.1:8000/dashboard/" -ForegroundColor Gray
