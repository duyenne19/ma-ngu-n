# HỆ THỐNG BÁO CÁO & THỐNG KÊ E-COMMERCE

## 📊 I. DOANH THU THEO NGÀY/THÁNG

### 1. SQL Query - Doanh thu theo ngày
```sql
-- Doanh thu theo ngày (30 ngày gần nhất)
SELECT 
    DATE(ngay_dat) as ngay,
    COUNT(DISTINCT id) as so_don_hang,
    SUM(tong_tien - tien_giam + phi_ship) as doanh_thu,
    AVG(tong_tien - tien_giam + phi_ship) as gia_tri_trung_binh
FROM store_donhang
WHERE trang_thai_don_hang = 'delivered'
  AND ngay_dat >= DATE('now', '-30 days')
GROUP BY DATE(ngay_dat)
ORDER BY ngay DESC;
```

### 2. SQL Query - Doanh thu theo tháng
```sql
-- Doanh thu theo tháng (12 tháng gần nhất)
SELECT 
    strftime('%Y-%m', ngay_dat) as thang,
    COUNT(DISTINCT id) as so_don_hang,
    SUM(tong_tien - tien_giam + phi_ship) as doanh_thu,
    SUM(tien_giam) as tong_giam_gia,
    AVG(tong_tien - tien_giam + phi_ship) as gia_tri_trung_binh,
    COUNT(DISTINCT nguoi_dung_id) as khach_hang_mua
FROM store_donhang
WHERE trang_thai_don_hang = 'delivered'
  AND ngay_dat >= DATE('now', '-12 months')
GROUP BY strftime('%Y-%m', ngay_dat)
ORDER BY thang DESC;
```

### 3. Django ORM - Doanh thu theo tháng
```python
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth, TruncDate
from datetime import datetime, timedelta

# Doanh thu theo tháng
doanh_thu_thang = DonHang.objects.filter(
    trang_thai_don_hang='delivered',
    ngay_dat__gte=datetime.now() - timedelta(days=365)
).annotate(
    thang=TruncMonth('ngay_dat')
).values('thang').annotate(
    so_don_hang=Count('id'),
    doanh_thu=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
    gia_tri_tb=Avg(F('tong_tien') - F('tien_giam') + F('phi_ship')),
    khach_hang=Count('nguoi_dung', distinct=True)
).order_by('-thang')

# Doanh thu theo ngày
doanh_thu_ngay = DonHang.objects.filter(
    trang_thai_don_hang='delivered',
    ngay_dat__gte=datetime.now() - timedelta(days=30)
).annotate(
    ngay=TruncDate('ngay_dat')
).values('ngay').annotate(
    so_don_hang=Count('id'),
    doanh_thu=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship'))
).order_by('-ngay')
```

### 4. View cho Dashboard
```python
# store/views.py
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_doanh_thu(request):
    """Dashboard doanh thu"""
    
    # Tháng này
    thang_nay_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    doanh_thu_thang_nay = DonHang.objects.filter(
        trang_thai_don_hang='delivered',
        ngay_dat__gte=thang_nay_start
    ).aggregate(
        tong=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
        so_don=Count('id')
    )
    
    # Hôm nay
    ngay_hom_nay = datetime.now().replace(hour=0, minute=0, second=0)
    doanh_thu_hom_nay = DonHang.objects.filter(
        trang_thai_don_hang='delivered',
        ngay_dat__gte=ngay_hom_nay
    ).aggregate(
        tong=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
        so_don=Count('id')
    )
    
    # Chart data - 30 ngày
    chart_data = list(DonHang.objects.filter(
        trang_thai_don_hang='delivered',
        ngay_dat__gte=datetime.now() - timedelta(days=30)
    ).annotate(
        ngay=TruncDate('ngay_dat')
    ).values('ngay').annotate(
        doanh_thu=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship'))
    ).order_by('ngay'))
    
    context = {
        'doanh_thu_thang_nay': doanh_thu_thang_nay,
        'doanh_thu_hom_nay': doanh_thu_hom_nay,
        'chart_data': chart_data,
    }
    
    return render(request, 'admin/dashboard_doanh_thu.html', context)
```

---

## 🔥 II. TOP SẢN PHẨM BÁN CHẠY

### 1. SQL Query
```sql
-- Top 20 sản phẩm bán chạy nhất
SELECT 
    sp.id,
    sp.ten_san_pham,
    sp.ma_san_pham,
    sp.gia,
    sp.gia_khuyen_mai,
    COUNT(DISTINCT dh.id) as so_don_hang,
    SUM(ctdh.so_luong) as tong_so_luong_ban,
    SUM(ctdh.so_luong * ctdh.gia) as doanh_thu,
    dm.ten_danh_muc
FROM store_sanpham sp
LEFT JOIN store_chitietdonhang ctdh ON sp.id = ctdh.san_pham_id
LEFT JOIN store_donhang dh ON ctdh.don_hang_id = dh.id
LEFT JOIN store_danhmuc dm ON sp.danh_muc_id = dm.id
WHERE dh.trang_thai_don_hang = 'delivered'
  AND dh.ngay_dat >= DATE('now', '-30 days')
GROUP BY sp.id
ORDER BY tong_so_luong_ban DESC
LIMIT 20;
```

### 2. SQL Query - Top theo danh mục
```sql
-- Top sản phẩm bán chạy theo từng danh mục
WITH san_pham_ban_chay AS (
    SELECT 
        sp.id,
        sp.ten_san_pham,
        sp.danh_muc_id,
        dm.ten_danh_muc,
        SUM(ctdh.so_luong) as tong_ban,
        SUM(ctdh.so_luong * ctdh.gia) as doanh_thu,
        ROW_NUMBER() OVER (PARTITION BY sp.danh_muc_id ORDER BY SUM(ctdh.so_luong) DESC) as rank_in_category
    FROM store_sanpham sp
    JOIN store_chitietdonhang ctdh ON sp.id = ctdh.san_pham_id
    JOIN store_donhang dh ON ctdh.don_hang_id = dh.id
    JOIN store_danhmuc dm ON sp.danh_muc_id = dm.id
    WHERE dh.trang_thai_don_hang = 'delivered'
      AND dh.ngay_dat >= DATE('now', '-30 days')
    GROUP BY sp.id, sp.danh_muc_id
)
SELECT * FROM san_pham_ban_chay
WHERE rank_in_category <= 5
ORDER BY danh_muc_id, rank_in_category;
```

### 3. Django ORM
```python
# Top sản phẩm bán chạy
from django.db.models import Sum, Count, F

top_san_pham = ChiTietDonHang.objects.filter(
    don_hang__trang_thai_don_hang='delivered',
    don_hang__ngay_dat__gte=datetime.now() - timedelta(days=30)
).values(
    'san_pham__id',
    'san_pham__ten_san_pham',
    'san_pham__ma_san_pham',
    'san_pham__gia',
    'san_pham__danh_muc__ten_danh_muc'
).annotate(
    so_luong_ban=Sum('so_luong'),
    so_don_hang=Count('don_hang', distinct=True),
    doanh_thu=Sum(F('so_luong') * F('gia'))
).order_by('-so_luong_ban')[:20]

# Sản phẩm bán ít (cần xử lý)
san_pham_ban_cham = SanPham.objects.annotate(
    da_ban_30_ngay=Sum(
        'chitietdonhang__so_luong',
        filter=Q(
            chitietdonhang__don_hang__trang_thai_don_hang='delivered',
            chitietdonhang__don_hang__ngay_dat__gte=datetime.now() - timedelta(days=30)
        )
    )
).filter(
    trang_thai='active',
    da_ban_30_ngay__lt=5  # Bán dưới 5 sản phẩm
).order_by('da_ban_30_ngay')[:20]
```

---

## 👥 III. NGƯỜI DÙNG HOẠT ĐỘNG NHIỀU

### 1. SQL Query
```sql
-- Top khách hàng VIP (mua nhiều nhất)
SELECT 
    u.id,
    u.username,
    u.email,
    p.ho_ten,
    p.so_dien_thoai,
    COUNT(DISTINCT dh.id) as so_don_hang,
    SUM(dh.tong_tien - dh.tien_giam + dh.phi_ship) as tong_chi_tieu,
    AVG(dh.tong_tien - dh.tien_giam + dh.phi_ship) as gia_tri_don_hang_tb,
    MAX(dh.ngay_dat) as mua_gan_nhat,
    JULIANDAY('now') - JULIANDAY(MAX(dh.ngay_dat)) as ngay_khong_mua
FROM auth_user u
LEFT JOIN store_profile p ON u.id = p.user_id
LEFT JOIN store_donhang dh ON u.id = dh.nguoi_dung_id
WHERE dh.trang_thai_don_hang = 'delivered'
GROUP BY u.id
HAVING COUNT(DISTINCT dh.id) >= 3
ORDER BY tong_chi_tieu DESC
LIMIT 50;
```

### 2. SQL Query - Phân tích RFM (Recency, Frequency, Monetary)
```sql
-- RFM Analysis
WITH rfm_data AS (
    SELECT 
        u.id as user_id,
        u.username,
        p.ho_ten,
        -- Recency: Số ngày từ lần mua cuối
        JULIANDAY('now') - JULIANDAY(MAX(dh.ngay_dat)) as recency,
        -- Frequency: Số đơn hàng
        COUNT(DISTINCT dh.id) as frequency,
        -- Monetary: Tổng chi tiêu
        SUM(dh.tong_tien - dh.tien_giam + dh.phi_ship) as monetary
    FROM auth_user u
    LEFT JOIN store_profile p ON u.id = p.user_id
    LEFT JOIN store_donhang dh ON u.id = dh.nguoi_dung_id
    WHERE dh.trang_thai_don_hang = 'delivered'
    GROUP BY u.id
),
rfm_score AS (
    SELECT *,
        CASE 
            WHEN recency <= 30 THEN 5
            WHEN recency <= 60 THEN 4
            WHEN recency <= 90 THEN 3
            WHEN recency <= 180 THEN 2
            ELSE 1
        END as r_score,
        CASE 
            WHEN frequency >= 10 THEN 5
            WHEN frequency >= 7 THEN 4
            WHEN frequency >= 5 THEN 3
            WHEN frequency >= 3 THEN 2
            ELSE 1
        END as f_score,
        CASE 
            WHEN monetary >= 10000000 THEN 5
            WHEN monetary >= 5000000 THEN 4
            WHEN monetary >= 2000000 THEN 3
            WHEN monetary >= 1000000 THEN 2
            ELSE 1
        END as m_score
    FROM rfm_data
)
SELECT *,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'VIP'
        WHEN r_score >= 4 AND f_score >= 3 THEN 'Loyal'
        WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        ELSE 'Regular'
    END as segment
FROM rfm_score
ORDER BY monetary DESC;
```

### 3. Django ORM
```python
# Top khách hàng VIP
from django.contrib.auth.models import User

top_khach_hang = User.objects.annotate(
    so_don_hang=Count(
        'don_hang_list',
        filter=Q(don_hang_list__trang_thai_don_hang='delivered')
    ),
    tong_chi_tieu=Sum(
        F('don_hang_list__tong_tien') - F('don_hang_list__tien_giam') + F('don_hang_list__phi_ship'),
        filter=Q(don_hang_list__trang_thai_don_hang='delivered')
    ),
    gia_tri_tb=Avg(
        F('don_hang_list__tong_tien') - F('don_hang_list__tien_giam') + F('don_hang_list__phi_ship'),
        filter=Q(don_hang_list__trang_thai_don_hang='delivered')
    ),
    mua_gan_nhat=Max('don_hang_list__ngay_dat')
).filter(
    so_don_hang__gte=3
).order_by('-tong_chi_tieu')[:50]

# Khách hàng nguy cơ rời bỏ (không mua >90 ngày)
from django.utils import timezone

khach_hang_at_risk = User.objects.annotate(
    mua_cuoi=Max('don_hang_list__ngay_dat'),
    so_don=Count('don_hang_list', filter=Q(don_hang_list__trang_thai_don_hang='delivered'))
).filter(
    so_don__gte=3,
    mua_cuoi__lt=timezone.now() - timedelta(days=90)
).order_by('mua_cuoi')
```

---

## 🎁 IV. HIỆU QUẢ MÃ GIẢM GIÁ

### 1. SQL Query
```sql
-- Hiệu quả từng mã giảm giá
SELECT 
    mgm.id,
    mgm.ma_code,
    mgm.ten_chuong_trinh,
    mgm.loai_giam,
    mgm.gia_tri_giam,
    mgm.so_luong as tong_so_luong,
    mgm.da_su_dung,
    ROUND(mgm.da_su_dung * 100.0 / mgm.so_luong, 2) as ti_le_su_dung,
    COUNT(DISTINCT dh_mg.don_hang_id) as so_don_hang_ap_dung,
    SUM(dh_mg.so_tien_giam) as tong_giam,
    SUM(dh.tong_tien) as tong_gia_tri_don_hang,
    AVG(dh.tong_tien) as gia_tri_don_hang_tb,
    mgm.ngay_bat_dau,
    mgm.ngay_ket_thuc
FROM store_magiamgia mgm
LEFT JOIN store_donhang_magiamgia dh_mg ON mgm.id = dh_mg.ma_giam_gia_id
LEFT JOIN store_donhang dh ON dh_mg.don_hang_id = dh.id
WHERE mgm.ngay_bat_dau >= DATE('now', '-90 days')
GROUP BY mgm.id
ORDER BY tong_giam DESC;
```

### 2. SQL Query - ROI của voucher
```sql
-- ROI (Return on Investment) của mã giảm giá
SELECT 
    mgm.ma_code,
    mgm.ten_chuong_trinh,
    -- Tổng giảm giá
    SUM(dh_mg.so_tien_giam) as tong_chi_phi_giam_gia,
    -- Tổng doanh thu từ đơn có voucher
    SUM(dh.tong_tien - dh.tien_giam + dh.phi_ship) as tong_doanh_thu,
    -- Số đơn hàng
    COUNT(DISTINCT dh.id) as so_don_hang,
    -- ROI = (Doanh thu - Chi phí) / Chi phí * 100
    ROUND((SUM(dh.tong_tien - dh.tien_giam + dh.phi_ship) - SUM(dh_mg.so_tien_giam)) * 100.0 / SUM(dh_mg.so_tien_giam), 2) as roi_percent,
    -- Giá trị đơn hàng trung bình
    AVG(dh.tong_tien) as gia_tri_don_tb
FROM store_magiamgia mgm
JOIN store_donhang_magiamgia dh_mg ON mgm.id = dh_mg.ma_giam_gia_id
JOIN store_donhang dh ON dh_mg.don_hang_id = dh.id
WHERE dh.trang_thai_don_hang = 'delivered'
  AND mgm.ngay_bat_dau >= DATE('now', '-90 days')
GROUP BY mgm.id
ORDER BY roi_percent DESC;
```

### 3. Django ORM
```python
# Hiệu quả mã giảm giá
hieu_qua_voucher = MaGiamGia.objects.annotate(
    so_don_su_dung=Count('donhang_magiamgia__don_hang', distinct=True),
    tong_giam=Sum('donhang_magiamgia__so_tien_giam'),
    tong_doanh_thu=Sum(
        F('donhang_magiamgia__don_hang__tong_tien') - 
        F('donhang_magiamgia__don_hang__tien_giam') + 
        F('donhang_magiamgia__don_hang__phi_ship')
    ),
    ti_le_su_dung=F('da_su_dung') * 100.0 / F('so_luong')
).filter(
    ngay_bat_dau__gte=datetime.now() - timedelta(days=90)
).order_by('-tong_giam')
```

---

## 📈 V. DASHBOARD BI - GỢI Ý THIẾT KẾ

### 1. Trang Dashboard Tổng Quan

**KPI Cards (Thẻ chỉ số):**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Doanh thu hôm nay│  │  Đơn hàng mới  │  │  Sản phẩm bán  │  │  Khách hàng mới │
│   15,750,000đ    │  │       24       │  │      156       │  │        8        │
│   ↑ 12% vs hqua  │  │   ↑ 18% vs hqua│  │   ↓ 5% vs hqua │  │   ↑ 25% vs hqua│
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Biểu đồ Line Chart - Doanh thu 30 ngày:**
```javascript
// Chart.js config
{
    type: 'line',
    data: {
        labels: ['1/1', '2/1', '3/1', ...],
        datasets: [{
            label: 'Doanh thu',
            data: [1500000, 2300000, 1800000, ...],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    }
}
```

**Biểu đồ Bar Chart - So sánh theo tháng:**
```javascript
{
    type: 'bar',
    data: {
        labels: ['T8/2025', 'T9/2025', 'T10/2025', 'T11/2025', 'T12/2025', 'T1/2026'],
        datasets: [{
            label: 'Doanh thu',
            data: [45000000, 52000000, 48000000, 61000000, 55000000, 15000000]
        }]
    }
}
```

### 2. Trang Top Sản Phẩm

**Bảng Top Sản Phẩm:**
```
┌────┬──────────────────┬──────────┬───────────┬─────────────┬──────────┐
│ #  │   Sản phẩm      │ Đã bán   │ Doanh thu │  Đơn hàng   │  Trend   │
├────┼──────────────────┼──────────┼───────────┼─────────────┼──────────┤
│ 1  │ iPhone 15 Pro    │   156    │ 450M đ    │     142     │    ↑↑    │
│ 2  │ MacBook Air M2   │   89     │ 320M đ    │     85      │    ↑     │
│ 3  │ AirPods Pro 2    │   234    │ 156M đ    │     187     │    →     │
└────┴──────────────────┴──────────┴───────────┴─────────────┴──────────┘
```

**Pie Chart - Phân bố theo danh mục:**
```javascript
{
    type: 'pie',
    data: {
        labels: ['Điện thoại', 'Laptop', 'Phụ kiện', 'Tablet'],
        datasets: [{
            data: [45, 30, 15, 10],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
        }]
    }
}
```

### 3. Trang Khách Hàng VIP

**Segmentation Matrix:**
```
                      ┌─────────────────────────────────────┐
                      │        FREQUENCY (Tần suất)         │
                      ├─────────────┬───────────────────────┤
                      │   Thấp      │        Cao            │
        ┌─────────────┼─────────────┼───────────────────────┤
        │    Gần      │   New       │      Loyal            │
RECENCY │             │ Customers   │    Customers          │
        │             │   (Mới)     │    (Trung thành)      │
        ├─────────────┼─────────────┼───────────────────────┤
        │    Xa       │   Lost      │      At Risk          │
        │             │ Customers   │    Customers          │
        │             │ (Đã mất)    │   (Nguy cơ rời bỏ)    │
        └─────────────┴─────────────┴───────────────────────┘
```

**Bảng RFM:**
```
┌────────────┬─────────┬───────────┬────────────┬─────────┬──────────┐
│   Khách    │ Recency │ Frequency │  Monetary  │   RFM   │ Segment  │
├────────────┼─────────┼───────────┼────────────┼─────────┼──────────┤
│ Nguyễn A   │   15    │    12     │  25,000,000│   545   │   VIP    │
│ Trần B     │   45    │     8     │  18,000,000│   443   │  Loyal   │
│ Lê C       │  120    │    15     │  32,000,000│   255   │ At Risk  │
└────────────┴─────────┴───────────┴────────────┴─────────┴──────────┘
```

### 4. Trang Voucher Performance

**Funnel Chart - Hiệu suất voucher:**
```
Phát hành:  1,000  ████████████████████████████████  100%
Nhận:         800  ████████████████████████          80%
Sử dụng:      450  ██████████████                    45%
Hoàn thành:   380  ████████████                      38%
```

**Scatter Plot - ROI vs Chi phí:**
```javascript
{
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Vouchers',
            data: [
                {x: 5000000, y: 250},  // Chi phí vs ROI%
                {x: 3000000, y: 180},
                {x: 8000000, y: 320}
            ]
        }]
    },
    options: {
        scales: {
            x: {title: {display: true, text: 'Chi phí (VND)'}},
            y: {title: {display: true, text: 'ROI (%)'}}
        }
    }
}
```

---

## 🛠️ VI. IMPLEMENTATION PLAN

### Phase 1: Tạo Models Báo Cáo (Tuần 1)

```python
# store/models.py - Thêm models mới

class BaoCaoDanhThu(models.Model):
    """Snapshot doanh thu theo ngày"""
    ngay = models.DateField(unique=True)
    so_don_hang = models.IntegerField(default=0)
    doanh_thu = models.DecimalField(max_digits=15, decimal_places=0)
    tien_giam = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    phi_ship = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    gia_tri_trung_binh = models.DecimalField(max_digits=12, decimal_places=0)
    so_khach_hang = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-ngay']
        indexes = [models.Index(fields=['ngay'])]


class ThongKeVoucher(models.Model):
    """Thống kê hiệu quả voucher"""
    ma_giam_gia = models.ForeignKey(MaGiamGia, on_delete=models.CASCADE)
    so_don_su_dung = models.IntegerField(default=0)
    tong_giam = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    tong_doanh_thu = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    roi = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['ma_giam_gia', 'ngay_cap_nhat']


class PhanKhucKhachHang(models.Model):
    """RFM Segmentation"""
    nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE)
    recency_score = models.IntegerField()  # 1-5
    frequency_score = models.IntegerField()  # 1-5
    monetary_score = models.IntegerField()  # 1-5
    segment = models.CharField(max_length=20, choices=[
        ('vip', 'VIP'),
        ('loyal', 'Loyal'),
        ('at_risk', 'At Risk'),
        ('lost', 'Lost'),
        ('new', 'New'),
        ('regular', 'Regular')
    ])
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
```

### Phase 2: Tạo Management Commands (Tuần 2)

```python
# store/management/commands/cap_nhat_bao_cao.py

from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Cập nhật báo cáo doanh thu hàng ngày'
    
    def handle(self, *args, **options):
        ngay_hom_qua = datetime.now().date() - timedelta(days=1)
        
        # Tính doanh thu hôm qua
        stats = DonHang.objects.filter(
            trang_thai_don_hang='delivered',
            ngay_dat__date=ngay_hom_qua
        ).aggregate(
            so_don=Count('id'),
            doanh_thu=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
            tien_giam=Sum('tien_giam'),
            phi_ship=Sum('phi_ship'),
            gia_tri_tb=Avg(F('tong_tien') - F('tien_giam') + F('phi_ship')),
            so_khach=Count('nguoi_dung', distinct=True)
        )
        
        # Lưu vào database
        BaoCaoDanhThu.objects.update_or_create(
            ngay=ngay_hom_qua,
            defaults=stats
        )
        
        self.stdout.write(f'✅ Đã cập nhật báo cáo {ngay_hom_qua}')


# Chạy command:
# python manage.py cap_nhat_bao_cao

# Hoặc tự động với Celery/Cron:
# 0 1 * * * cd /path/to/project && python manage.py cap_nhat_bao_cao
```

### Phase 3: Tạo Views & URLs (Tuần 3)

```python
# store/urls.py - Thêm URLs

urlpatterns = [
    # ... existing urls ...
    
    # Dashboard
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('dashboard/doanh-thu/', views.dashboard_doanh_thu, name='dashboard-doanhthu'),
    path('dashboard/san-pham/', views.dashboard_sanpham, name='dashboard-sanpham'),
    path('dashboard/khach-hang/', views.dashboard_khachhang, name='dashboard-khachhang'),
    path('dashboard/voucher/', views.dashboard_voucher, name='dashboard-voucher'),
    
    # API endpoints cho charts
    path('api/doanh-thu/chart/', views.api_doanhthu_chart, name='api-doanhthu-chart'),
    path('api/top-sanpham/', views.api_top_sanpham, name='api-top-sanpham'),
]
```

### Phase 4: Frontend Templates (Tuần 4)

```html
<!-- templates/admin/dashboard_doanh_thu.html -->
{% extends "admin/base_site.html" %}
{% load static %}

{% block content %}
<div class="dashboard">
    <!-- KPI Cards -->
    <div class="row">
        <div class="col-md-3">
            <div class="card kpi-card">
                <h3>Doanh thu hôm nay</h3>
                <h2>{{ doanh_thu_hom_nay.tong|floatformat:0 }} đ</h2>
                <span class="trend up">↑ 12%</span>
            </div>
        </div>
        <!-- More KPI cards -->
    </div>
    
    <!-- Charts -->
    <div class="row mt-4">
        <div class="col-md-12">
            <canvas id="doanhThuChart"></canvas>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Fetch data và render chart
    fetch('/api/doanh-thu/chart/')
        .then(res => res.json())
        .then(data => {
            new Chart(document.getElementById('doanhThuChart'), {
                type: 'line',
                data: data
            });
        });
</script>
{% endblock %}
```

---

## 📊 VII. CÔNG CỤ BI KHUYẾN NGHỊ

### 1. Tích hợp sẵn (Free)
- **Django Admin + Chart.js**: Tự build dashboard
- **Plotly Dash**: Dashboard Python interactive
- **Streamlit**: BI app nhanh

### 2. Công cụ chuyên nghiệp (Paid)
- **Metabase**: Open-source BI, kết nối trực tiếp DB
- **Redash**: Query, visualize, share
- **Apache Superset**: Modern BI platform

### 3. Cloud BI (Enterprise)
- **Google Data Studio** (Free): Kết nối PostgreSQL
- **Tableau**: Professional analytics
- **Power BI**: Microsoft ecosystem

---

## 🎯 VIII. NEXT STEPS

### Triển khai ngay:
1. ✅ Tạo file này làm tài liệu tham khảo
2. ⬜ Implement Phase 1 (Models)
3. ⬜ Tạo management commands
4. ⬜ Build dashboard với Chart.js
5. ⬜ Setup Celery cho auto-report

### Future enhancements:
- Machine Learning: Dự đoán doanh thu
- Cohort Analysis: Phân tích nhóm khách hàng
- A/B Testing: Test hiệu quả voucher
- Real-time Dashboard: WebSocket updates

---

**File này:** `BAO_CAO_THONG_KE.md`
**Ngày tạo:** 2026-02-02
**Version:** 1.0
