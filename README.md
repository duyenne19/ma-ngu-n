# 🛍️ TikiShop - Web Bán Hàng Online

**Hệ thống e-commerce đầy đủ với dashboard quản lý doanh thu, sản phẩm, khách hàng và voucher.**

---

## ⚡ Cài đặt & Chạy Nhanh

### 🪟 Windows (PowerShell)
```powershell
cd ma-ngu-n
.\setup.ps1
```

### 🍎 macOS / 🐧 Linux
```bash
cd ma-ngu-n
chmod +x setup.sh
./setup.sh
```

### 📖 Cài đặt Thủ công
Xem [SETUP_GUIDE.md](SETUP_GUIDE.md) để hướng dẫn chi tiết từng bước.

---

## 🎯 Sau cài đặt

### 1️⃣ Tạo tài khoản Admin (nếu chưa có)
```bash
python manage.py createsuperuser
```

### 2️⃣ Khởi động Server
```bash
python manage.py runserver
```

### 3️⃣ Truy cập các trang
- 🏠 **Trang chủ:** http://127.0.0.1:8000/
- 🛒 **Cửa hàng:** http://127.0.0.1:8000/shop/
- 🎯 **Danh mục:** http://127.0.0.1:8000/categories/
- 🛍️ **Giỏ hàng:** http://127.0.0.1:8000/cart/
- 📦 **Đơn hàng:** http://127.0.0.1:8000/orders/
- 👤 **Tài khoản:** http://127.0.0.1:8000/account/
- 🔐 **Admin Panel:** http://127.0.0.1:8000/admin/
- 📊 **Dashboard:** http://127.0.0.1:8000/dashboard/

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|-----------|----------|---------|
| **Django** | 6.0.1 | Backend framework |
| **Python** | 3.10+ | Ngôn ngữ lập trình |
| **Chart.js** | 3.9.1 | Biểu đồ dashboard |
| **Bootstrap** | 5.1.3 | Responsive UI |
| **SQLite3** | Latest | Database |
| **HTML/CSS/JS** | - | Frontend |
| **Pillow** | 10.1.0 | Image processing |

---

## 📊 Tính năng chính

### 👥 Khách hàng
- ✅ Đăng ký tài khoản, đổi mật khẩu
- ✅ Xem sản phẩm theo danh mục, lọc theo giá
- ✅ Tìm kiếm sản phẩm nhanh
- ✅ Thêm vào giỏ hàng, thanh toán
- ✅ Quản lý đơn hàng và hóa đơn
- ✅ Đánh giá và bình luận sản phẩm
- ✅ Lưu sản phẩm yêu thích
- ✅ Xem lịch sử mua hàng

### 📈 Quản lý (Staff/Admin)
- 📊 **Dashboard Tổng quan** - KPI chính, doanh thu 7 ngày, sản phẩm bán chạy
- 💰 **Báo cáo Doanh thu** - Phân tích doanh thu theo ngày/tháng, biểu đồ xu hướng
- 📦 **Quản lý Sản phẩm** - Top sellers, sản phẩm bán chậm, tồn kho thấp
- 👥 **Phân tích Khách hàng** - Phân khúc RFM, khách hàng VIP, khách hàng có nguy cơ
- 🎟️ **Báo cáo Voucher** - ROI voucher, hiệu quả khuyến mãi
- 🏷️ **Quản lý Sản phẩm** - Thêm/sửa/xóa sản phẩm, danh mục
- 📝 **Quản lý Đơn hàng** - Duyệt, cập nhật trạng thái đơn hàng
- 💳 **Quản lý Voucher** - Tạo mã giảm giá, theo dõi sử dụng

---

## 📂 Cấu trúc thư mục

```
ma-ngu-n/
├── store/                      # Django app chính
│   ├── models.py              # Database models (26 models)
│   ├── views.py               # Views & API endpoints
│   ├── urls.py                # URL routing
│   ├── admin.py               # Django admin interface
│   ├── forms.py               # Django forms
│   ├── migrations/            # Database migrations
│   ├── management/commands/   # Custom management commands
│   └── __pycache__/           # Python cache
├── annoying/                   # Utility app
│   ├── decorators.py          # Custom decorators
│   ├── fields.py              # Custom fields
│   ├── functions.py           # Utility functions
│   └── middlewares.py         # Custom middleware
├── templates/                  # HTML templates
│   ├── dashboard/             # 6 dashboard pages
│   ├── account/               # User account pages
│   ├── store/                 # Store pages
│   ├── base.html              # Base template
│   └── navbar.html            # Navigation bar
├── tikishop/                   # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL router
│   ├── asgi.py                # ASGI config
│   └── wsgi.py                # WSGI config
├── media/                      # User uploads
│   ├── avatar/                # User avatars
│   ├── category/              # Category images
│   └── product/               # Product images
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management
├── requirements.txt           # Python dependencies
├── SETUP_GUIDE.md             # Detailed setup guide
├── setup.ps1                  # Windows setup script
├── setup.sh                   # Linux/macOS setup script
└── README.md                  # This file
```

---

## 🎨 Dashboard Pages

| Trang | URL | Mô tả |
|-------|-----|-------|
| **Tổng quan** | `/dashboard/` | KPI, doanh thu 7 ngày, top 5 sản phẩm |
| **Doanh thu** | `/dashboard/doanh-thu/` | Phân tích doanh thu với bộ lọc ngày |
| **Sản phẩm** | `/dashboard/san-pham/` | Top 20 sản phẩm, phân tích danh mục, tồn kho |
| **Khách hàng** | `/dashboard/khach-hang/` | RFM segmentation, VIP customers, at-risk |
| **Voucher** | `/dashboard/voucher/` | ROI analysis, performance metrics |

---

## 🔐 Bảo mật

- ✅ PBKDF2 SHA256 password hashing
- ✅ @staff_member_required decorator cho admin pages
- ✅ @login_required cho user pages
- ✅ CSRF protection trên forms
- ✅ SQL injection prevention (ORM queries)
- ✅ XSS protection (template escaping)

---

## 📦 Yêu cầu hệ thống

- **Python:** 3.10 trở lên
- **pip:** Package manager
- **Git:** Để clone repository
- **RAM:** Tối thiểu 1GB
- **Disk:** Tối thiểu 500MB

---

## 🐛 Xử lý sự cố

### ❌ "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### ❌ "OperationalError: no such table"
```bash
python manage.py migrate
```

### ❌ Port 8000 đang bị sử dụng
```bash
python manage.py runserver 8001
```

### ❌ Database bị lỗi
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

Xem [SETUP_GUIDE.md](SETUP_GUIDE.md#-xử-lý-sự-cố) để xử lý lỗi chi tiết hơn.

---

## 👥 Thành viên nhóm

- **Lê Thị Mỹ Duyên** - Nhóm trưởng
- **Vũ Thanh Hiền**
- **Vũ Thùy Dương**
- ** Nguyễn Thị Bích Thảo**

---

## 📊 Database Diagram

Xem [chart.drawio](chart.drawio) hoặc truy cập [dbdiagram.io](https://dbdiagram.io/) để xem sơ đồ database.

Tổng cộng: **26 models** được định nghĩa trong [store/models.py](store/models.py)

---

## 🚀 Deployment

Để deploy lên production, xem hướng dẫn trong [SETUP_GUIDE.md#-deploy-production](SETUP_GUIDE.md#-deploy-production).

---

## 📚 Tài liệu thêm

- 📖 [Django Documentation](https://docs.djangoproject.com/)
- 📊 [Chart.js Documentation](https://www.chartjs.org/docs/)
- 🎨 [Bootstrap Documentation](https://getbootstrap.com/docs/)
- 🗄️ [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 📝 License

Dự án này là một phần của khóa học đại học.

---

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Chạy `python manage.py check` để kiểm tra lỗi Django
3. Kiểm tra log server
4. Tạo issue trên GitHub

---

**Last Updated:** February 4, 2026 | **Version:** 2.0
