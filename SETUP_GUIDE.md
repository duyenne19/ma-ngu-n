# TikiShop - Hướng dẫn Cài đặt & Chạy

## 📋 Yêu cầu
- Python 3.10+ 
- pip (Package manager)
- Git

## 🚀 Hướng dẫn Cài đặt

### 1. Clone Repository
```bash
git clone https://github.com/duyenne19/ma-ngu-n.git
cd ma-ngu-n/ma-ngu-n
```

### 2. Tạo Virtual Environment
**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Chạy Migrations
```bash
python manage.py migrate
```

### 5. Tạo Tài khoản Admin (Superuser)
```bash
python manage.py createsuperuser
```

Nhập thông tin:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (hoặc mật khẩu của bạn)

### 6. Khởi động Server
```bash
python manage.py runserver
```

Server sẽ chạy tại: **http://127.0.0.1:8000/**

## 📊 Tạo Dữ liệu Mẫu (Tùy chọn)

Để xem dashboard hoạt động với dữ liệu:

### Tạo dữ liệu qua Admin Panel
1. Truy cập: http://127.0.0.1:8000/admin/
2. Đăng nhập với tài khoản admin vừa tạo
3. Tạo:
   - **Danh mục sản phẩm** (Categories)
   - **Sản phẩm** (Products)
   - **Đơn hàng** (Orders) - với trạng thái "delivered"
   - **Mã giảm giá** (Vouchers)

### Cập nhật Báo cáo
Sau khi có dữ liệu đơn hàng, chạy:

```bash
# Cập nhật báo cáo doanh thu
python manage.py cap_nhat_bao_cao_doanh_thu

# Cập nhật phân khúc khách hàng
python manage.py cap_nhat_phan_khuc_khach_hang

# Cập nhật thống kê voucher
python manage.py cap_nhat_thong_ke_voucher
```

## 📍 Truy cập Các Trang Chính

### Trang Khách Hàng
- **Trang chủ:** http://127.0.0.1:8000/
- **Danh mục:** http://127.0.0.1:8000/categories/
- **Giỏ hàng:** http://127.0.0.1:8000/cart/
- **Đơn hàng:** http://127.0.0.1:8000/orders/

### Trang Quản lý (Staff/Admin)
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Dashboard Tổng quan:** http://127.0.0.1:8000/dashboard/
- **Báo cáo Doanh thu:** http://127.0.0.1:8000/dashboard/doanh-thu/
- **Báo cáo Sản phẩm:** http://127.0.0.1:8000/dashboard/san-pham/
- **Phân tích Khách hàng:** http://127.0.0.1:8000/dashboard/khach-hang/
- **Báo cáo Voucher:** http://127.0.0.1:8000/dashboard/voucher/

## 🔧 Cấu hình Django Settings

File cấu hình: `tikishop/settings.py`

**Những cài đặt quan trọng:**
- `DEBUG = True` (Chế độ phát triển - thay đổi thành `False` khi deploy)
- `ALLOWED_HOSTS = []` (Thêm domain/IP khi deploy)
- `DATABASES` (SQLite3 mặc định - có thể thay đổi)
- `TIME_ZONE = 'Asia/Tomsk'` (Múi giờ)

## 📦 Structure Thư mục

```
ma-ngu-n/
├── ma-ngu-n/                 # Project folder
│   ├── store/                # Main Django app
│   │   ├── models.py         # Database models
│   │   ├── views.py          # Views & controllers
│   │   ├── urls.py           # URL routing
│   │   ├── admin.py          # Admin interface
│   │   └── management/       # Custom commands
│   ├── annoying/             # Utility app
│   ├── templates/            # HTML templates
│   │   ├── dashboard/        # Dashboard pages
│   │   └── ...
│   ├── tikishop/             # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py             # Django management
│   ├── db.sqlite3            # Database
│   └── requirements.txt       # Python dependencies
```

## ❓ Xử lý Sự cố

### Error: "ModuleNotFoundError: No module named 'django'"
**Giải pháp:** Chưa cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Error: "django.db.utils.OperationalError: no such table"
**Giải pháp:** Chưa chạy migrations
```bash
python manage.py migrate
```

### Port 8000 đang bị sử dụng
**Giải pháp:** Chạy trên port khác
```bash
python manage.py runserver 8001
```

### Database bị lỗi
**Giải pháp:** Reset database (xóa db.sqlite3 và chạy lại)
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 📝 Lưu ý Quan trọng

- ✅ Virtual environment nên được kích hoạt trước khi cài dependencies
- ✅ Không commit `db.sqlite3` và `__pycache__/` (đã thêm vào .gitignore)
- ✅ Khi có thay đổi models, cần tạo migration mới:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- ✅ Cài đặt dependencies mới vào requirements.txt:
  ```bash
  pip freeze > requirements.txt
  ```

## 🚀 Deploy (Production)

Khi deploy lên production:
1. Thay đổi `DEBUG = False` trong settings.py
2. Thêm domain vào `ALLOWED_HOSTS`
3. Sử dụng PostgreSQL thay vì SQLite3
4. Sử dụng Gunicorn hoặc uWSGI server
5. Setup Nginx hoặc Apache reverse proxy
6. Sử dụng SSL/TLS certificate

## 📞 Liên hệ Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
- Python version: `python --version`
- Pip packages: `pip list`
- Database migrations: `python manage.py showmigrations`
- Django settings: `python manage.py check`

---

**Last Updated:** February 4, 2026
