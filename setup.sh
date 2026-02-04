#!/bin/bash
# TikiShop - Setup Script (macOS/Linux)
# Tự động cài đặt dependencies và khởi tạo project

echo "================================"
echo "TikiShop - Automated Setup"
echo "================================"

# Kiểm tra Python
echo ""
echo "[1/5] Kiểm tra Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 không được cài đặt. Vui lòng cài đặt Python 3.10+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✓ $PYTHON_VERSION"

# Tạo Virtual Environment
echo ""
echo "[2/5] Tạo Virtual Environment..."
if [ -d ".venv" ]; then
    echo "✓ Virtual Environment đã tồn tại"
else
    python3 -m venv .venv
    echo "✓ Virtual Environment được tạo"
fi

# Kích hoạt Virtual Environment
echo ""
echo "[3/5] Kích hoạt Virtual Environment..."
source .venv/bin/activate
echo "✓ Virtual Environment được kích hoạt"

# Cài đặt Dependencies
echo ""
echo "[4/5] Cài đặt Dependencies (có thể mất 1-2 phút)..."
pip install -q -r requirements.txt
echo "✓ Dependencies được cài đặt"

# Chạy Migrations
echo ""
echo "[5/5] Chạy Migrations..."
python manage.py migrate --quiet
echo "✓ Migrations hoàn tất"

# Xong
echo ""
echo "================================"
echo "✓ SETUP HOÀN TẤT!"
echo "================================"

echo ""
echo "Bước tiếp theo:"
echo "1. Tạo tài khoản Admin (nếu chưa có):"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Khởi động Server:"
echo "   python manage.py runserver"
echo ""
echo "3. Truy cập:"
echo "   - Trang chủ: http://127.0.0.1:8000/"
echo "   - Admin: http://127.0.0.1:8000/admin/"
echo "   - Dashboard: http://127.0.0.1:8000/dashboard/"
