from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from annoying.fields import AutoOneToOneField


# ==================== NGƯỜI DÙNG ====================
class Profile(models.Model):
    """Mở rộng thông tin User"""
    user = AutoOneToOneField(
        User, 
        primary_key=True, 
        on_delete=models.CASCADE, 
        verbose_name="Tài khoản"
    )
    ho_ten = models.CharField(max_length=200, verbose_name="Họ tên", blank=True)
    so_dien_thoai = models.CharField(max_length=20, verbose_name="Số điện thoại", blank=True)
    anh_dai_dien = models.ImageField(
        upload_to='avatar', 
        default="avatar/default avatar.jpg",
        verbose_name="Ảnh đại diện"
    )
    trang_thai = models.CharField(
        max_length=20, 
        choices=[
            ('active', 'Đang hoạt động'),
            ('inactive', 'Tạm khóa'),
            ('banned', 'Đã cấm')
        ],
        default='active',
        verbose_name="Trạng thái"
    )
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Hồ sơ người dùng"
        verbose_name_plural = "Hồ sơ người dùng"
    
    def __str__(self):
        return self.user.username


# ==================== ĐỊA CHỈ ====================
class DiaChi(models.Model):
    """Địa chỉ giao hàng của người dùng"""
    nguoi_dung = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='dia_chi_list',
        verbose_name="Người dùng"
    )
    ten_nguoi_nhan = models.CharField(max_length=200, verbose_name="Tên người nhận")
    so_dien_thoai = models.CharField(max_length=20, verbose_name="Số điện thoại")
    dia_chi_chi_tiet = models.TextField(verbose_name="Địa chỉ chi tiết")
    tinh_thanh = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    quan_huyen = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    phuong_xa = models.CharField(max_length=100, verbose_name="Phường/Xã")
    mac_dinh = models.BooleanField(default=False, verbose_name="Địa chỉ mặc định")
    
    class Meta:
        verbose_name = "Địa chỉ"
        verbose_name_plural = "Địa chỉ"
        ordering = ['-mac_dinh', '-id']
    
    def __str__(self):
        return f"{self.ten_nguoi_nhan} - {self.tinh_thanh}"
    
    def save(self, *args, **kwargs):
        # Nếu đây là địa chỉ mặc định, bỏ mặc định của các địa chỉ khác
        if self.mac_dinh:
            DiaChi.objects.filter(nguoi_dung=self.nguoi_dung, mac_dinh=True).update(mac_dinh=False)
        super().save(*args, **kwargs)


# ==================== DANH MỤC ====================
class DanhMuc(models.Model):
    """Danh mục sản phẩm - hỗ trợ danh mục con"""
    ten_danh_muc = models.CharField(max_length=200, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Slug")
    danh_muc_cha = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='danh_muc_con',
        verbose_name="Danh mục cha"
    )
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")
    anh_danh_muc = models.ImageField(
        upload_to='category', 
        blank=True, 
        null=True, 
        verbose_name="Ảnh danh mục"
    )
    hien_thi = models.BooleanField(default=True, verbose_name="Hiển thị")
    noi_bat = models.BooleanField(default=False, verbose_name="Nổi bật")
    thu_tu = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['thu_tu', 'ten_danh_muc']
    
    def __str__(self):
        return self.ten_danh_muc


# ==================== SẢN PHẨM ====================
class SanPham(models.Model):
    """Sản phẩm"""
    danh_muc = models.ForeignKey(
        DanhMuc,
        on_delete=models.CASCADE,
        related_name='san_pham_list',
        verbose_name="Danh mục"
    )
    ten_san_pham = models.CharField(max_length=300, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=320, unique=True, verbose_name="Slug")
    ma_san_pham = models.CharField(max_length=100, unique=True, verbose_name="Mã sản phẩm (SKU)")
    mo_ta = models.TextField(verbose_name="Mô tả")
    mo_ta_chi_tiet = models.TextField(blank=True, verbose_name="Mô tả chi tiết")
    gia = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá gốc")
    gia_khuyen_mai = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        null=True, 
        blank=True,
        verbose_name="Giá khuyến mãi"
    )
    so_luong_ton = models.IntegerField(default=0, verbose_name="Số lượng tồn kho")
    so_luong_canh_bao = models.IntegerField(default=10, verbose_name="Cảnh báo hết hàng")
    noi_bat = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật")
    luot_xem = models.IntegerField(default=0, verbose_name="Lượt xem")
    da_ban = models.IntegerField(default=0, verbose_name="Đã bán")
    trang_thai = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Đang bán'),
            ('out_of_stock', 'Hết hàng'),
            ('inactive', 'Ngừng bán')
        ],
        default='active',
        verbose_name="Trạng thái"
    )
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-ngay_tao']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['ma_san_pham']),
            models.Index(fields=['-luot_xem']),
            models.Index(fields=['-da_ban']),
        ]
    
    def __str__(self):
        return self.ten_san_pham
    
    @property
    def gia_hien_thi(self):
        """Giá hiển thị (ưu tiên giá khuyến mãi)"""
        return self.gia_khuyen_mai if self.gia_khuyen_mai else self.gia
    
    @property
    def phan_tram_giam(self):
        """Phần trăm giảm giá"""
        if self.gia_khuyen_mai and self.gia > 0:
            return int((1 - self.gia_khuyen_mai / self.gia) * 100)
        return 0
    
    @property
    def con_hang(self):
        """Kiểm tra còn hàng"""
        return self.so_luong_ton > 0


# ==================== ẢNH SẢN PHẨM ====================
class AnhSanPham(models.Model):
    """Ảnh sản phẩm - cho phép nhiều ảnh cho một sản phẩm"""
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='anh_list',
        verbose_name="Sản phẩm"
    )
    duong_dan_anh = models.ImageField(upload_to='product', verbose_name="Hình ảnh")
    anh_chinh = models.BooleanField(default=False, verbose_name="Ảnh chính")
    thu_tu = models.IntegerField(default=0, verbose_name="Thứ tự")
    
    class Meta:
        verbose_name = "Ảnh sản phẩm"
        verbose_name_plural = "Ảnh sản phẩm"
        ordering = ['-anh_chinh', 'thu_tu']
    
    def __str__(self):
        return f"Ảnh: {self.san_pham.ten_san_pham}"
    
    def save(self, *args, **kwargs):
        # Nếu đây là ảnh chính, bỏ ảnh chính của các ảnh khác
        if self.anh_chinh:
            AnhSanPham.objects.filter(san_pham=self.san_pham, anh_chinh=True).update(anh_chinh=False)
        super().save(*args, **kwargs)


# ==================== YÊU THÍCH ====================
class YeuThich(models.Model):
    """Sản phẩm yêu thích của người dùng"""
    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='yeu_thich_list',
        verbose_name="Người dùng"
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='yeu_thich_list',
        verbose_name="Sản phẩm"
    )
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thêm")
    
    class Meta:
        verbose_name = "Yêu thích"
        verbose_name_plural = "Yêu thích"
        unique_together = ['nguoi_dung', 'san_pham']
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.san_pham.ten_san_pham}"


# ==================== ĐÃ XEM GẦN ĐÂY ====================
class DaXemGanDay(models.Model):
    """Lịch sử xem sản phẩm"""
    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lich_su_xem',
        verbose_name="Người dùng"
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='lich_su_xem',
        verbose_name="Sản phẩm"
    )
    thoi_gian_xem = models.DateTimeField(auto_now=True, verbose_name="Thời gian xem")
    
    class Meta:
        verbose_name = "Đã xem gần đây"
        verbose_name_plural = "Đã xem gần đây"
        ordering = ['-thoi_gian_xem']
        unique_together = ['nguoi_dung', 'san_pham']
    
    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.san_pham.ten_san_pham}"


# ==================== GIỎ HÀNG ====================
class GioHang(models.Model):
    """Giỏ hàng của người dùng"""
    nguoi_dung = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='gio_hang',
        verbose_name="Người dùng"
    )
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    
    class Meta:
        verbose_name = "Giỏ hàng"
        verbose_name_plural = "Giỏ hàng"
    
    def __str__(self):
        return f"Giỏ hàng: {self.nguoi_dung.username}"
    
    @property
    def tong_so_luong(self):
        """Tổng số lượng sản phẩm trong giỏ"""
        return sum(item.so_luong for item in self.chi_tiet.all())
    
    @property
    def tong_tien(self):
        """Tổng tiền trong giỏ"""
        return sum(item.thanh_tien for item in self.chi_tiet.all())


class ChiTietGioHang(models.Model):
    """Chi tiết giỏ hàng"""
    gio_hang = models.ForeignKey(
        GioHang,
        on_delete=models.CASCADE,
        related_name='chi_tiet',
        verbose_name="Giỏ hàng"
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        verbose_name="Sản phẩm"
    )
    so_luong = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    gia = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá tại thời điểm thêm")
    ngay_them = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thêm")
    
    class Meta:
        verbose_name = "Chi tiết giỏ hàng"
        verbose_name_plural = "Chi tiết giỏ hàng"
        unique_together = ['gio_hang', 'san_pham']
    
    def __str__(self):
        return f"{self.san_pham.ten_san_pham} x {self.so_luong}"
    
    @property
    def thanh_tien(self):
        """Thành tiền"""
        if self.gia and self.so_luong:
            return self.gia * self.so_luong
        return 0
    
    def save(self, *args, **kwargs):
        # Tự động lấy giá hiện tại của sản phẩm nếu chưa có
        if not self.gia:
            self.gia = self.san_pham.gia_hien_thi
        super().save(*args, **kwargs)


# ==================== MÃ GIẢM GIÁ ====================
class MaGiamGia(models.Model):
    """Mã giảm giá/Voucher"""
    ma_code = models.CharField(max_length=50, unique=True, verbose_name="Mã giảm giá")
    ten_chuong_trinh = models.CharField(max_length=200, verbose_name="Tên chương trình")
    loai_giam = models.CharField(
        max_length=20,
        choices=[
            ('percent', 'Giảm phần trăm'),
            ('fixed', 'Giảm cố định'),
            ('freeship', 'Miễn phí ship')
        ],
        verbose_name="Loại giảm giá"
    )
    gia_tri_giam = models.DecimalField(
        max_digits=12, 
        decimal_places=0,
        verbose_name="Giá trị giảm"
    )
    gia_tri_don_toi_thieu = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Giá trị đơn tối thiểu"
    )
    giam_toi_da = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Giảm tối đa (với %)"
    )
    ngay_bat_dau = models.DateTimeField(verbose_name="Ngày bắt đầu")
    ngay_ket_thuc = models.DateTimeField(verbose_name="Ngày kết thúc")
    so_luong = models.IntegerField(verbose_name="Số lượng mã")
    da_su_dung = models.IntegerField(default=0, verbose_name="Đã sử dụng")
    trang_thai = models.BooleanField(default=True, verbose_name="Kích hoạt")
    
    class Meta:
        verbose_name = "Mã giảm giá"
        verbose_name_plural = "Mã giảm giá"
        ordering = ['-ngay_tao']
    
    ngay_tao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ma_code
    
    @property
    def con_hieu_luc(self):
        """Kiểm tra mã còn hiệu lực"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.trang_thai and 
            self.ngay_bat_dau <= now <= self.ngay_ket_thuc and
            self.da_su_dung < self.so_luong
        )


# ==================== ĐỌN HÀNG ====================
class DonHang(models.Model):
    """Đơn hàng"""
    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='don_hang_list',
        verbose_name="Người dùng"
    )
    dia_chi = models.ForeignKey(
        DiaChi,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Địa chỉ giao hàng"
    )
    ma_don_hang = models.CharField(max_length=50, unique=True, verbose_name="Mã đơn hàng")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền")
    tien_giam = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        default=0,
        verbose_name="Tiền giảm"
    )
    phi_ship = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Phí ship"
    )
    phuong_thuc_thanh_toan = models.CharField(
        max_length=30,
        choices=[
            ('cod', 'Thanh toán khi nhận hàng'),
            ('vnpay', 'VNPay'),
            ('momo', 'MoMo'),
            ('zalopay', 'ZaloPay'),
            ('bank_transfer', 'Chuyển khoản ngân hàng')
        ],
        default='cod',
        verbose_name="Phương thức thanh toán"
    )
    trang_thai_thanh_toan = models.CharField(
        max_length=20,
        choices=[
            ('unpaid', 'Chưa thanh toán'),
            ('paid', 'Đã thanh toán'),
            ('refunded', 'Đã hoàn tiền')
        ],
        default='unpaid',
        verbose_name="Trạng thái thanh toán"
    )
    trang_thai_don_hang = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Chờ xác nhận'),
            ('confirmed', 'Đã xác nhận'),
            ('preparing', 'Đang chuẩn bị hàng'),
            ('shipping', 'Đang giao hàng'),
            ('delivered', 'Đã giao hàng'),
            ('cancelled', 'Đã hủy'),
            ('returned', 'Đã trả hàng')
        ],
        default='pending',
        verbose_name="Trạng thái đơn hàng"
    )
    ghi_chu = models.TextField(blank=True, verbose_name="Ghi chú")
    ngay_dat = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-ngay_dat']
        indexes = [
            models.Index(fields=['ma_don_hang']),
            models.Index(fields=['-ngay_dat']),
        ]
    
    def __str__(self):
        return f"#{self.ma_don_hang}"
    
    @property
    def tong_thanh_toan(self):
        """Tổng tiền phải thanh toán"""
        return self.tong_tien - self.tien_giam + self.phi_ship


class ChiTietDonHang(models.Model):
    """Chi tiết đơn hàng"""
    don_hang = models.ForeignKey(
        DonHang,
        on_delete=models.CASCADE,
        related_name='chi_tiet',
        verbose_name="Đơn hàng"
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Sản phẩm"
    )
    ten_san_pham = models.CharField(max_length=300, verbose_name="Tên sản phẩm")
    so_luong = models.PositiveIntegerField(verbose_name="Số lượng")
    gia = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá")
    
    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"
    
    def __str__(self):
        return f"{self.ten_san_pham} x {self.so_luong}"
    
    @property
    def thanh_tien(self):
        """Thành tiền"""
        if self.gia and self.so_luong:
            return self.gia * self.so_luong
        return 0


class DonHang_MaGiamGia(models.Model):
    """Mã giảm giá áp dụng cho đơn hàng"""
    don_hang = models.ForeignKey(
        DonHang,
        on_delete=models.CASCADE,
        related_name='ma_giam_gia_ap_dung',
        verbose_name="Đơn hàng"
    )
    ma_giam_gia = models.ForeignKey(
        MaGiamGia,
        on_delete=models.CASCADE,
        verbose_name="Mã giảm giá"
    )
    so_tien_giam = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Số tiền giảm"
    )
    
    class Meta:
        verbose_name = "Mã giảm giá đơn hàng"
        verbose_name_plural = "Mã giảm giá đơn hàng"
    
    def __str__(self):
        return f"{self.don_hang.ma_don_hang} - {self.ma_giam_gia.ma_code}"


# ==================== HÓA ĐƠN ====================
class HoaDon(models.Model):
    """Hóa đơn"""
    don_hang = models.OneToOneField(
        DonHang,
        on_delete=models.CASCADE,
        related_name='hoa_don',
        verbose_name="Đơn hàng"
    )
    ma_hoa_don = models.CharField(max_length=50, unique=True, verbose_name="Mã hóa đơn")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền")
    ngay_xuat = models.DateTimeField(auto_now_add=True, verbose_name="Ngày xuất")
    
    class Meta:
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"
        ordering = ['-ngay_xuat']
    
    def __str__(self):
        return f"HĐ: {self.ma_hoa_don}"


# ==================== THANH TOÁN ====================
class ThanhToan(models.Model):
    """Lịch sử thanh toán"""
    don_hang = models.ForeignKey(
        DonHang,
        on_delete=models.CASCADE,
        related_name='lich_su_thanh_toan',
        verbose_name="Đơn hàng"
    )
    cong_thanh_toan = models.CharField(
        max_length=50,
        choices=[
            ('vnpay', 'VNPay'),
            ('momo', 'MoMo'),
            ('zalopay', 'ZaloPay'),
            ('bank_transfer', 'Chuyển khoản'),
            ('cod', 'COD')
        ],
        verbose_name="Cổng thanh toán"
    )
    ma_giao_dich = models.CharField(max_length=200, verbose_name="Mã giao dịch")
    so_tien = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Số tiền")
    trang_thai = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Đang xử lý'),
            ('success', 'Thành công'),
            ('failed', 'Thất bại'),
            ('cancelled', 'Đã hủy')
        ],
        verbose_name="Trạng thái"
    )
    noi_dung = models.TextField(blank=True, verbose_name="Nội dung")
    ngay_thanh_toan = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thanh toán")
    
    class Meta:
        verbose_name = "Thanh toán"
        verbose_name_plural = "Thanh toán"
        ordering = ['-ngay_thanh_toan']
    
    def __str__(self):
        return f"{self.don_hang.ma_don_hang} - {self.ma_giao_dich}"


# ==================== ĐÁNH GIÁ ====================
class DanhGia(models.Model):
    """Đánh giá sản phẩm"""
    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='danh_gia_list',
        verbose_name="Người dùng"
    )
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='danh_gia_list',
        verbose_name="Sản phẩm"
    )
    so_sao = models.IntegerField(
        choices=[(i, f"{i} sao") for i in range(1, 6)],
        verbose_name="Số sao"
    )
    binh_luan = models.TextField(blank=True, verbose_name="Bình luận")
    anh_danh_gia = models.ImageField(
        upload_to='reviews',
        blank=True,
        null=True,
        verbose_name="Ảnh đánh giá"
    )
    huu_ich = models.IntegerField(default=0, verbose_name="Số người thấy hữu ích")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ['-ngay_tao']
        unique_together = ['nguoi_dung', 'san_pham']
    
    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.san_pham.ten_san_pham} ({self.so_sao}⭐)"


# ==================== THÔNG BÁO ====================
class ThongBao(models.Model):
    """Thông báo cho người dùng"""
    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='thong_bao_list',
        verbose_name="Người dùng"
    )
    loai_thong_bao = models.CharField(
        max_length=30,
        choices=[
            ('order', 'Đơn hàng'),
            ('promotion', 'Khuyến mãi'),
            ('system', 'Hệ thống'),
            ('review', 'Đánh giá'),
        ],
        default='system',
        verbose_name="Loại thông báo"
    )
    tieu_de = models.CharField(max_length=200, verbose_name="Tiêu đề")
    noi_dung = models.TextField(verbose_name="Nội dung")
    lien_ket = models.CharField(max_length=500, blank=True, verbose_name="Liên kết")
    da_doc = models.BooleanField(default=False, verbose_name="Đã đọc")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.tieu_de}"


# ==================== LỊCH SỬ KHO ====================
class LichSuKho(models.Model):
    """Lịch sử nhập/xuất kho"""
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='lich_su_kho',
        verbose_name="Sản phẩm"
    )
    so_luong_thay_doi = models.IntegerField(verbose_name="Số lượng thay đổi (+/-)")
    so_luong_truoc = models.IntegerField(verbose_name="Số lượng trước")
    so_luong_sau = models.IntegerField(verbose_name="Số lượng sau")
    ly_do = models.CharField(
        max_length=50,
        choices=[
            ('import', 'Nhập hàng'),
            ('sold', 'Đã bán'),
            ('returned', 'Trả hàng'),
            ('damaged', 'Hàng hỏng'),
            ('adjustment', 'Điều chỉnh')
        ],
        verbose_name="Lý do"
    )
    ghi_chu = models.TextField(blank=True, verbose_name="Ghi chú")
    nguoi_thuc_hien = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Người thực hiện"
    )
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Lịch sử kho"
        verbose_name_plural = "Lịch sử kho"
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.san_pham.ten_san_pham} ({self.so_luong_thay_doi:+d})"


# ==================== TRÒ CHUYỆN & HỖ TRỢ ====================
class TroChuyen(models.Model):
    """Phiên trò chuyện"""
    nguoi_dung = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tro_chuyen_khach',
        verbose_name="Khách hàng"
    )
    quan_tri = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tro_chuyen_admin',
        verbose_name="Quản trị viên"
    )
    trang_thai = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Đang chat'),
            ('closed', 'Đã đóng'),
            ('waiting', 'Chờ phản hồi')
        ],
        default='active',
        verbose_name="Trạng thái"
    )
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")
    
    class Meta:
        verbose_name = "Trò chuyện"
        verbose_name_plural = "Trò chuyện"
        ordering = ['-ngay_cap_nhat']
    
    def __str__(self):
        return f"Chat #{self.id} - {self.nguoi_dung.username}"


class TinNhan(models.Model):
    """Tin nhắn trong trò chuyện"""
    tro_chuyen = models.ForeignKey(
        TroChuyen,
        on_delete=models.CASCADE,
        related_name='tin_nhan_list',
        verbose_name="Trò chuyện"
    )
    nguoi_gui = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Người gửi"
    )
    noi_dung = models.TextField(verbose_name="Nội dung")
    anh_dinh_kem = models.ImageField(
        upload_to='chat',
        blank=True,
        null=True,
        verbose_name="Ảnh đính kèm"
    )
    da_doc = models.BooleanField(default=False, verbose_name="Đã đọc")
    thoi_gian_gui = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian gửi")
    
    class Meta:
        verbose_name = "Tin nhắn"
        verbose_name_plural = "Tin nhắn"
        ordering = ['thoi_gian_gui']


# ==================== MODELS BÁO CÁO & THỐNG KÊ ====================

class BaoCaoDoanThu(models.Model):
    """
    Model lưu trữ snapshot doanh thu theo ngày
    Dùng cho việc query nhanh và theo dõi xu hướng
    """
    ngay = models.DateField(unique=True, verbose_name="Ngày")
    so_don_hang = models.IntegerField(default=0, verbose_name="Số đơn hàng")
    doanh_thu = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Doanh thu"
    )
    tien_giam = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Tiền giảm giá"
    )
    phi_ship = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Phí ship"
    )
    gia_tri_trung_binh = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Giá trị đơn hàng TB"
    )
    so_khach_hang = models.IntegerField(default=0, verbose_name="Số khách hàng")
    so_san_pham_ban = models.IntegerField(default=0, verbose_name="Số sản phẩm bán")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Báo cáo doanh thu"
        verbose_name_plural = "Báo cáo doanh thu"
        ordering = ['-ngay']
        indexes = [
            models.Index(fields=['ngay']),
            models.Index(fields=['-ngay', '-doanh_thu']),
        ]
    
    def __str__(self):
        return f"Báo cáo {self.ngay}: {self.doanh_thu:,.0f}đ"


class ThongKeVoucher(models.Model):
    """
    Model theo dõi hiệu quả của từng mã giảm giá
    Tính toán ROI và các chỉ số performance
    """
    ma_giam_gia = models.ForeignKey(
        MaGiamGia,
        on_delete=models.CASCADE,
        related_name='thong_ke',
        verbose_name="Mã giảm giá"
    )
    thang = models.DateField(verbose_name="Tháng thống kê")
    so_don_su_dung = models.IntegerField(default=0, verbose_name="Số đơn sử dụng")
    tong_giam = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Tổng tiền giảm"
    )
    tong_doanh_thu = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Tổng doanh thu"
    )
    roi = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="ROI (%)",
        help_text="ROI = (Doanh thu - Chi phí giảm giá) / Chi phí * 100"
    )
    gia_tri_don_hang_tb = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Giá trị đơn hàng TB"
    )
    ti_le_su_dung = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Tỷ lệ sử dụng (%)"
    )
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Thống kê voucher"
        verbose_name_plural = "Thống kê voucher"
        ordering = ['-thang', '-tong_doanh_thu']
        unique_together = ['ma_giam_gia', 'thang']
        indexes = [
            models.Index(fields=['thang']),
            models.Index(fields=['ma_giam_gia', '-roi']),
        ]
    
    def __str__(self):
        return f"Thống kê {self.ma_giam_gia.ma_code} - {self.thang.strftime('%m/%Y')}"
    
    def tinh_roi(self):
        """Tính toán ROI tự động"""
        if self.tong_giam > 0:
            self.roi = ((self.tong_doanh_thu - self.tong_giam) / self.tong_giam) * 100
        else:
            self.roi = 0
        return self.roi


class PhanKhucKhachHang(models.Model):
    """
    Model phân khúc khách hàng theo RFM (Recency, Frequency, Monetary)
    - Recency: Gần đây mua bao lâu
    - Frequency: Tần suất mua hàng
    - Monetary: Tổng chi tiêu
    """
    SEGMENT_CHOICES = [
        ('vip', 'VIP - Khách hàng VIP'),
        ('loyal', 'Loyal - Trung thành'),
        ('at_risk', 'At Risk - Nguy cơ rời bỏ'),
        ('lost', 'Lost - Đã mất'),
        ('new', 'New - Khách mới'),
        ('regular', 'Regular - Thường xuyên'),
        ('promising', 'Promising - Tiềm năng'),
        ('need_attention', 'Need Attention - Cần chăm sóc'),
    ]
    
    nguoi_dung = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='phan_khuc',
        verbose_name="Người dùng"
    )
    
    # RFM Scores (1-5)
    recency_score = models.IntegerField(
        default=1,
        verbose_name="Điểm Recency",
        help_text="1-5: Số ngày từ lần mua cuối (5 = mua gần nhất)"
    )
    frequency_score = models.IntegerField(
        default=1,
        verbose_name="Điểm Frequency",
        help_text="1-5: Số lần mua hàng (5 = mua nhiều nhất)"
    )
    monetary_score = models.IntegerField(
        default=1,
        verbose_name="Điểm Monetary",
        help_text="1-5: Tổng chi tiêu (5 = chi nhiều nhất)"
    )
    
    # Raw values
    ngay_mua_cuoi = models.DateField(null=True, blank=True, verbose_name="Ngày mua cuối")
    so_ngay_khong_mua = models.IntegerField(default=0, verbose_name="Số ngày không mua")
    tong_so_don_hang = models.IntegerField(default=0, verbose_name="Tổng số đơn hàng")
    tong_chi_tieu = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Tổng chi tiêu"
    )
    gia_tri_don_hang_tb = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Giá trị đơn hàng TB"
    )
    
    # Segment
    segment = models.CharField(
        max_length=20,
        choices=SEGMENT_CHOICES,
        default='new',
        verbose_name="Phân khúc"
    )
    rfm_score = models.CharField(
        max_length=3,
        default='111',
        verbose_name="RFM Score",
        help_text="VD: 555 = R5F5M5"
    )
    
    # Thông tin thêm
    lan_cuoi_tinh = models.DateTimeField(auto_now=True, verbose_name="Lần cuối tính")
    ghi_chu = models.TextField(blank=True, verbose_name="Ghi chú")
    
    class Meta:
        verbose_name = "Phân khúc khách hàng"
        verbose_name_plural = "Phân khúc khách hàng"
        ordering = ['-monetary_score', '-frequency_score', '-recency_score']
        indexes = [
            models.Index(fields=['segment']),
            models.Index(fields=['-monetary_score', '-frequency_score']),
            models.Index(fields=['ngay_mua_cuoi']),
        ]
    
    def __str__(self):
        return f"{self.nguoi_dung.username} - {self.get_segment_display()} (RFM: {self.rfm_score})"
    
    def tinh_rfm_score(self):
        """Tự động tính RFM score từ 3 điểm thành phần"""
        self.rfm_score = f"{self.recency_score}{self.frequency_score}{self.monetary_score}"
        return self.rfm_score
    
    def xac_dinh_segment(self):
        """
        Tự động xác định phân khúc dựa trên RFM scores
        Logic phân khúc:
        - VIP: R>=4, F>=4, M>=4
        - Loyal: R>=3, F>=4
        - At Risk: R<=2, F>=4
        - Lost: R<=2, F<=2
        - Promising: R>=4, F<=2, M>=3
        - New: F<=1
        - Regular: Others
        """
        r, f, m = self.recency_score, self.frequency_score, self.monetary_score
        
        if r >= 4 and f >= 4 and m >= 4:
            self.segment = 'vip'
        elif r >= 3 and f >= 4:
            self.segment = 'loyal'
        elif r <= 2 and f >= 4:
            self.segment = 'at_risk'
        elif r <= 2 and f <= 2:
            self.segment = 'lost'
        elif r >= 4 and f <= 2 and m >= 3:
            self.segment = 'promising'
        elif f <= 1:
            self.segment = 'new'
        elif r <= 2 and m >= 3:
            self.segment = 'need_attention'
        else:
            self.segment = 'regular'
        
        return self.segment
    
    def save(self, *args, **kwargs):
        """Override save để tự động tính toán"""
        self.tinh_rfm_score()
        self.xac_dinh_segment()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nguoi_gui.username}: {self.noi_dung[:50]}"
