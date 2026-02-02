# 🚀 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG BÁO CÁO & THỐNG KÊ

## ✅ Phase 1: ĐÃ HOÀN THÀNH

### 1. Models đã tạo:
- ✅ **BaoCaoDoanThu**: Báo cáo doanh thu theo ngày
- ✅ **ThongKeVoucher**: Thống kê hiệu quả mã giảm giá
- ✅ **PhanKhucKhachHang**: Phân khúc khách hàng theo RFM

### 2. Admin Interface:
- ✅ Đã đăng ký 3 models trong admin panel
- ✅ Có colored segments cho RFM
- ✅ Có formatted fields (tiền tệ, ROI, etc.)

### 3. Management Commands:
- ✅ `cap_nhat_bao_cao_doanh_thu`: Cập nhật báo cáo doanh thu
- ✅ `cap_nhat_thong_ke_voucher`: Thống kê voucher
- ✅ `cap_nhat_phan_khuc_khach_hang`: Phân tích RFM khách hàng

---

## 📖 HƯỚNG DẪN SỬ DỤNG

### A. Xem Báo Cáo trong Admin Panel

1. **Truy cập Admin:**
   ```
   http://127.0.0.1:8000/admin/
   Username: admin
   Password: admin123
   ```

2. **Các menu báo cáo:**
   - **Báo cáo doanh thu** (`store/BaoCaoDoanThu`)
   - **Thống kê voucher** (`store/ThongKeVoucher`)
   - **Phân khúc khách hàng** (`store/PhanKhucKhachHang`)

---

### B. Cập Nhật Báo Cáo Doanh Thu

#### 1. Cập nhật ngày hôm qua (mặc định):
```bash
python manage.py cap_nhat_bao_cao_doanh_thu
```

#### 2. Cập nhật ngày cụ thể:
```bash
python manage.py cap_nhat_bao_cao_doanh_thu --ngay 2026-02-01
```

#### 3. Cập nhật cả tháng:
```bash
python manage.py cap_nhat_bao_cao_doanh_thu --thang 2026-01
```

**Output mẫu:**
```
📊 Đang cập nhật báo cáo ngày 2026-02-01...
✅ Tạo mới báo cáo 2026-02-01:
   - Đơn hàng: 15
   - Doanh thu: 25,750,000 đ
   - Khách hàng: 12
   - Sản phẩm bán: 45
```

---

### C. Thống Kê Voucher

#### 1. Thống kê tháng trước (mặc định):
```bash
python manage.py cap_nhat_thong_ke_voucher
```

#### 2. Thống kê tháng cụ thể:
```bash
python manage.py cap_nhat_thong_ke_voucher --thang 2026-01
```

#### 3. Thống kê tất cả voucher (4 tháng gần nhất):
```bash
python manage.py cap_nhat_thong_ke_voucher --tat-ca
```

**Output mẫu:**
```
📊 Thống kê voucher tháng 01/2026...
🆕 SUMMER2026: 25 đơn, 45,000,000đ, ROI: 320.5%
🔄 NEWYEAR2026: 18 đơn, 32,000,000đ, ROI: 280.3%
✅ Hoàn thành thống kê 2 voucher!
```

---

### D. Phân Khúc Khách Hàng (RFM)

#### 1. Phân tích tất cả khách hàng:
```bash
python manage.py cap_nhat_phan_khuc_khach_hang
```

#### 2. Phân tích user cụ thể:
```bash
python manage.py cap_nhat_phan_khuc_khach_hang --user-id 1
```

**Output mẫu:**
```
📊 Bắt đầu phân tích RFM cho tất cả khách hàng...
Tìm thấy 50 khách hàng cần phân tích

👑 nguyen.van.a         | RFM: 555 | VIP - Khách hàng VIP  |   25,000,000đ |  15 đơn
💎 tran.thi.b           | RFM: 445 | Loyal - Trung thành   |   18,000,000đ |  12 đơn
⚠️ le.van.c             | RFM: 254 | At Risk - Nguy cơ rời |   32,000,000đ |  20 đơn
🆕 pham.thi.d           | RFM: 511 | New - Khách mới       |    3,500,000đ |   1 đơn

✅ Hoàn thành!
   - Tạo mới: 10
   - Cập nhật: 40
   - Tổng: 50
```

**Các phân khúc RFM:**
- 👑 **VIP**: R>=4, F>=4, M>=4 (Khách hàng VIP)
- 💎 **Loyal**: R>=3, F>=4 (Trung thành)
- ⚠️ **At Risk**: R<=2, F>=4 (Nguy cơ rời bỏ)
- 💔 **Lost**: R<=2, F<=2 (Đã mất)
- 🆕 **New**: F<=1 (Khách mới)
- 🌟 **Promising**: R>=4, F<=2, M>=3 (Tiềm năng)
- 🔔 **Need Attention**: R<=2, M>=3 (Cần chăm sóc)
- 👤 **Regular**: Others (Thường xuyên)

---

## 🤖 TỰ ĐỘNG HÓA

### 1. Windows Task Scheduler

#### Tạo file batch: `cap_nhat_bao_cao_hang_ngay.bat`
```batch
@echo off
cd D:\ma-ngu-n\ma-ngu-n
D:\ma-ngu-n\.venv\Scripts\python.exe manage.py cap_nhat_bao_cao_doanh_thu
D:\ma-ngu-n\.venv\Scripts\python.exe manage.py cap_nhat_phan_khuc_khach_hang
```

#### Đặt lịch chạy:
1. Mở **Task Scheduler** (gõ `taskschd.msc`)
2. **Create Basic Task**
3. Trigger: Daily, 1:00 AM
4. Action: Start a program
5. Program: `D:\ma-ngu-n\ma-ngu-n\cap_nhat_bao_cao_hang_ngay.bat`

### 2. Cron Job (Linux/Mac)
```bash
# Crontab
# Chạy mỗi ngày lúc 1:00 AM
0 1 * * * cd /path/to/project && python manage.py cap_nhat_bao_cao_doanh_thu
0 1 * * * cd /path/to/project && python manage.py cap_nhat_phan_khuc_khach_hang

# Chạy mỗi đầu tháng lúc 2:00 AM
0 2 1 * * cd /path/to/project && python manage.py cap_nhat_thong_ke_voucher
```

### 3. Celery (Nâng cao)
```python
# tikishop/celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('tikishop')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def cap_nhat_bao_cao_hang_ngay():
    from django.core.management import call_command
    call_command('cap_nhat_bao_cao_doanh_thu')
    call_command('cap_nhat_phan_khuc_khach_hang')

@app.task
def cap_nhat_thong_ke_hang_thang():
    from django.core.management import call_command
    call_command('cap_nhat_thong_ke_voucher')

# Lịch trình
app.conf.beat_schedule = {
    'cap-nhat-hang-ngay': {
        'task': 'tikishop.celery.cap_nhat_bao_cao_hang_ngay',
        'schedule': crontab(hour=1, minute=0),
    },
    'cap-nhat-hang-thang': {
        'task': 'tikishop.celery.cap_nhat_thong_ke_hang_thang',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),
    },
}
```

---

## 📊 SQL QUERIES NHANH

### 1. Xem doanh thu 7 ngày gần nhất:
```sql
SELECT ngay, doanh_thu, so_don_hang, so_khach_hang
FROM store_baocaodoanthu
ORDER BY ngay DESC
LIMIT 7;
```

### 2. Top voucher có ROI cao nhất:
```sql
SELECT 
    mgm.ma_code,
    mgm.ten_chuong_trinh,
    tkv.roi,
    tkv.tong_doanh_thu,
    tkv.so_don_su_dung
FROM store_thongkevoucher tkv
JOIN store_magiamgia mgm ON tkv.ma_giam_gia_id = mgm.id
ORDER BY tkv.roi DESC
LIMIT 10;
```

### 3. Khách hàng VIP:
```sql
SELECT 
    u.username,
    u.email,
    pkh.rfm_score,
    pkh.tong_chi_tieu,
    pkh.tong_so_don_hang
FROM store_phankhuckhachhang pkh
JOIN auth_user u ON pkh.nguoi_dung_id = u.id
WHERE pkh.segment = 'vip'
ORDER BY pkh.tong_chi_tieu DESC;
```

---

## 🎯 NEXT STEPS

### Phase 2: Dashboard Views (Tuần 3)
```bash
# Sẽ tạo:
- store/views.py: dashboard_doanh_thu(), dashboard_sanpham(), etc.
- store/urls.py: URL patterns cho dashboard
- API endpoints cho charts
```

### Phase 3: Frontend Templates (Tuần 4)
```bash
# Sẽ tạo:
- templates/admin/dashboard_doanh_thu.html
- templates/admin/dashboard_sanpham.html
- templates/admin/dashboard_khachhang.html
- Chart.js integration
```

### Phase 4: BI Tools (Tuần 5)
```bash
# Tích hợp:
- Metabase hoặc Redash
- Google Data Studio
- Export CSV/Excel
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: No module named 'store.management'
```bash
# Đảm bảo có file __init__.py
touch store/management/__init__.py
touch store/management/commands/__init__.py
```

### Lỗi: Command not found
```bash
# List tất cả commands
python manage.py help

# Kiểm tra file command có lỗi syntax không
python -m py_compile store/management/commands/cap_nhat_bao_cao_doanh_thu.py
```

### Lỗi: Database locked
```bash
# SQLite đang được sử dụng, dừng server trước
# Ctrl+C để dừng runserver
# Sau đó chạy lại command
```

---

## 📞 SUPPORT

- **Tài liệu đầy đủ**: `BAO_CAO_THONG_KE.md`
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Models**: `store/models.py` (dòng 788+)
- **Commands**: `store/management/commands/`

---

**Ngày tạo:** 2026-02-02  
**Version:** 1.0  
**Status:** ✅ Phase 1 Completed
