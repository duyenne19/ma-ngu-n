from django.contrib import admin
from .models import (
    Profile, DiaChi, DanhMuc, SanPham, AnhSanPham, 
    YeuThich, DaXemGanDay, GioHang, ChiTietGioHang,
    MaGiamGia, DonHang, ChiTietDonHang, DonHang_MaGiamGia,
    HoaDon, ThanhToan, DanhGia, ThongBao, LichSuKho,
    TroChuyen, TinNhan,
    BaoCaoDoanThu, ThongKeVoucher, PhanKhucKhachHang
)
from django.utils.html import format_html


# ==================== NGƯỜI DÙNG ====================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ho_ten', 'so_dien_thoai', 'trang_thai', 'ngay_tao')
    list_filter = ('trang_thai', 'ngay_tao')
    search_fields = ('user__username', 'user__email', 'ho_ten', 'so_dien_thoai')
    list_per_page = 20


# ==================== ĐỊA CHỈ ====================
@admin.register(DiaChi)
class DiaChiAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'ten_nguoi_nhan', 'so_dien_thoai', 'tinh_thanh', 'mac_dinh')
    list_filter = ('mac_dinh', 'tinh_thanh')
    search_fields = ('ten_nguoi_nhan', 'so_dien_thoai', 'dia_chi_chi_tiet')
    list_per_page = 20


# ==================== DANH MỤC ====================
@admin.register(DanhMuc)
class DanhMucAdmin(admin.ModelAdmin):
    list_display = ('ten_danh_muc', 'slug', 'danh_muc_cha', 'hien_thi', 'noi_bat', 'thu_tu')
    list_editable = ('hien_thi', 'noi_bat', 'thu_tu')
    list_filter = ('hien_thi', 'noi_bat', 'danh_muc_cha')
    search_fields = ('ten_danh_muc', 'slug')
    prepopulated_fields = {'slug': ('ten_danh_muc',)}
    list_per_page = 20


# ==================== SẢN PHẨM ====================
class AnhSanPhamInline(admin.TabularInline):
    model = AnhSanPham
    extra = 1
    fields = ('duong_dan_anh', 'anh_chinh', 'thu_tu')


@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ('ten_san_pham', 'ma_san_pham', 'danh_muc', 'gia', 'gia_khuyen_mai', 
                    'so_luong_ton', 'trang_thai', 'noi_bat', 'luot_xem', 'da_ban')
    list_editable = ('gia', 'gia_khuyen_mai', 'so_luong_ton', 'trang_thai', 'noi_bat')
    list_filter = ('trang_thai', 'noi_bat', 'danh_muc', 'ngay_tao')
    search_fields = ('ten_san_pham', 'ma_san_pham', 'slug')
    prepopulated_fields = {'slug': ('ten_san_pham',)}
    readonly_fields = ('luot_xem', 'da_ban', 'ngay_tao', 'ngay_cap_nhat')
    inlines = [AnhSanPhamInline]
    list_per_page = 20
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('ten_san_pham', 'slug', 'ma_san_pham', 'danh_muc')
        }),
        ('Mô tả', {
            'fields': ('mo_ta', 'mo_ta_chi_tiet')
        }),
        ('Giá & Kho', {
            'fields': ('gia', 'gia_khuyen_mai', 'so_luong_ton', 'so_luong_canh_bao')
        }),
        ('Trạng thái', {
            'fields': ('trang_thai', 'noi_bat')
        }),
        ('Thống kê', {
            'fields': ('luot_xem', 'da_ban', 'ngay_tao', 'ngay_cap_nhat'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnhSanPham)
class AnhSanPhamAdmin(admin.ModelAdmin):
    list_display = ('san_pham', 'anh_chinh', 'thu_tu', 'duong_dan_anh')
    list_filter = ('anh_chinh', 'san_pham')
    list_editable = ('anh_chinh', 'thu_tu')


# ==================== YÊU THÍCH ====================
@admin.register(YeuThich)
class YeuThichAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'san_pham', 'ngay_tao')
    list_filter = ('ngay_tao',)
    search_fields = ('nguoi_dung__username', 'san_pham__ten_san_pham')
    date_hierarchy = 'ngay_tao'


@admin.register(DaXemGanDay)
class DaXemGanDayAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'san_pham', 'thoi_gian_xem')
    list_filter = ('thoi_gian_xem',)
    search_fields = ('nguoi_dung__username', 'san_pham__ten_san_pham')
    date_hierarchy = 'thoi_gian_xem'


# ==================== GIỎ HÀNG ====================
class ChiTietGioHangInline(admin.TabularInline):
    model = ChiTietGioHang
    extra = 0
    readonly_fields = ('thanh_tien',)


@admin.register(GioHang)
class GioHangAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'tong_so_luong', 'tong_tien', 'ngay_cap_nhat')
    search_fields = ('nguoi_dung__username',)
    readonly_fields = ('tong_so_luong', 'tong_tien')
    inlines = [ChiTietGioHangInline]


@admin.register(ChiTietGioHang)
class ChiTietGioHangAdmin(admin.ModelAdmin):
    list_display = ('gio_hang', 'san_pham', 'so_luong', 'gia', 'thanh_tien', 'ngay_them')
    list_filter = ('ngay_them',)
    readonly_fields = ('thanh_tien',)


# ==================== MÃ GIẢM GIÁ ====================
@admin.register(MaGiamGia)
class MaGiamGiaAdmin(admin.ModelAdmin):
    list_display = ('ma_code', 'ten_chuong_trinh', 'loai_giam', 'gia_tri_giam', 
                    'so_luong', 'da_su_dung', 'ngay_bat_dau', 'ngay_ket_thuc', 'trang_thai')
    list_editable = ('trang_thai',)
    list_filter = ('loai_giam', 'trang_thai', 'ngay_bat_dau', 'ngay_ket_thuc')
    search_fields = ('ma_code', 'ten_chuong_trinh')
    readonly_fields = ('da_su_dung', 'con_hieu_luc')
    date_hierarchy = 'ngay_bat_dau'


# ==================== ĐƠN HÀNG ====================
class ChiTietDonHangInline(admin.TabularInline):
    model = ChiTietDonHang
    extra = 0
    readonly_fields = ('thanh_tien',)


class DonHang_MaGiamGiaInline(admin.TabularInline):
    model = DonHang_MaGiamGia
    extra = 0


@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    list_display = ('ma_don_hang', 'nguoi_dung', 'tong_thanh_toan', 
                    'phuong_thuc_thanh_toan', 'trang_thai_thanh_toan', 
                    'trang_thai_don_hang', 'ngay_dat')
    list_editable = ('trang_thai_thanh_toan', 'trang_thai_don_hang')
    list_filter = ('trang_thai_don_hang', 'trang_thai_thanh_toan', 
                   'phuong_thuc_thanh_toan', 'ngay_dat')
    search_fields = ('ma_don_hang', 'nguoi_dung__username')
    readonly_fields = ('ma_don_hang', 'tong_thanh_toan', 'ngay_dat', 'ngay_cap_nhat')
    date_hierarchy = 'ngay_dat'
    inlines = [ChiTietDonHangInline, DonHang_MaGiamGiaInline]
    list_per_page = 20
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('ma_don_hang', 'nguoi_dung', 'dia_chi')
        }),
        ('Giá trị', {
            'fields': ('tong_tien', 'tien_giam', 'phi_ship', 'tong_thanh_toan')
        }),
        ('Thanh toán', {
            'fields': ('phuong_thuc_thanh_toan', 'trang_thai_thanh_toan')
        }),
        ('Trạng thái', {
            'fields': ('trang_thai_don_hang', 'ghi_chu')
        }),
        ('Thời gian', {
            'fields': ('ngay_dat', 'ngay_cap_nhat'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChiTietDonHang)
class ChiTietDonHangAdmin(admin.ModelAdmin):
    list_display = ('don_hang', 'san_pham', 'ten_san_pham', 'so_luong', 'gia', 'thanh_tien')
    list_filter = ('don_hang__ngay_dat',)
    search_fields = ('don_hang__ma_don_hang', 'ten_san_pham')
    readonly_fields = ('thanh_tien',)


# ==================== HÓA ĐƠN ====================
@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    list_display = ('ma_hoa_don', 'don_hang', 'tong_tien', 'ngay_xuat')
    search_fields = ('ma_hoa_don', 'don_hang__ma_don_hang')
    readonly_fields = ('ma_hoa_don', 'ngay_xuat')
    date_hierarchy = 'ngay_xuat'


# ==================== THANH TOÁN ====================
@admin.register(ThanhToan)
class ThanhToanAdmin(admin.ModelAdmin):
    list_display = ('don_hang', 'cong_thanh_toan', 'ma_giao_dich', 
                    'so_tien', 'trang_thai', 'ngay_thanh_toan')
    list_filter = ('cong_thanh_toan', 'trang_thai', 'ngay_thanh_toan')
    search_fields = ('don_hang__ma_don_hang', 'ma_giao_dich')
    readonly_fields = ('ngay_thanh_toan',)
    date_hierarchy = 'ngay_thanh_toan'


# ==================== ĐÁNH GIÁ ====================
@admin.register(DanhGia)
class DanhGiaAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'san_pham', 'so_sao', 'huu_ich', 'ngay_tao')
    list_filter = ('so_sao', 'ngay_tao')
    search_fields = ('nguoi_dung__username', 'san_pham__ten_san_pham', 'binh_luan')
    readonly_fields = ('ngay_tao',)
    date_hierarchy = 'ngay_tao'


# ==================== THÔNG BÁO ====================
@admin.register(ThongBao)
class ThongBaoAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'loai_thong_bao', 'tieu_de', 'da_doc', 'ngay_tao')
    list_filter = ('loai_thong_bao', 'da_doc', 'ngay_tao')
    search_fields = ('nguoi_dung__username', 'tieu_de', 'noi_dung')
    readonly_fields = ('ngay_tao',)
    date_hierarchy = 'ngay_tao'


# ==================== LỊCH SỬ KHO ====================
@admin.register(LichSuKho)
class LichSuKhoAdmin(admin.ModelAdmin):
    list_display = ('san_pham', 'so_luong_thay_doi', 'so_luong_truoc', 
                    'so_luong_sau', 'ly_do', 'nguoi_thuc_hien', 'ngay_tao')
    list_filter = ('ly_do', 'ngay_tao')
    search_fields = ('san_pham__ten_san_pham', 'ghi_chu')
    readonly_fields = ('ngay_tao',)
    date_hierarchy = 'ngay_tao'


# ==================== TRÒ CHUYỆN ====================
class TinNhanInline(admin.TabularInline):
    model = TinNhan
    extra = 0
    readonly_fields = ('thoi_gian_gui',)


@admin.register(TroChuyen)
class TroChuyenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nguoi_dung', 'quan_tri', 'trang_thai', 'ngay_tao', 'ngay_cap_nhat')
    list_filter = ('trang_thai', 'ngay_tao')
    search_fields = ('nguoi_dung__username', 'quan_tri__username')
    readonly_fields = ('ngay_tao', 'ngay_cap_nhat')
    inlines = [TinNhanInline]


@admin.register(TinNhan)
class TinNhanAdmin(admin.ModelAdmin):
    list_display = ('tro_chuyen', 'nguoi_gui', 'noi_dung_rut_gon', 'da_doc', 'thoi_gian_gui')
    list_filter = ('da_doc', 'thoi_gian_gui')
    search_fields = ('noi_dung', 'nguoi_gui__username')
    readonly_fields = ('thoi_gian_gui',)
    
    def noi_dung_rut_gon(self, obj):
        return obj.noi_dung[:50] + '...' if len(obj.noi_dung) > 50 else obj.noi_dung
    noi_dung_rut_gon.short_description = 'Nội dung'


# ==================== ADMIN BÁO CÁO & THỐNG KÊ ====================

@admin.register(BaoCaoDoanThu)
class BaoCaoDoanThuAdmin(admin.ModelAdmin):
    """Admin cho báo cáo doanh thu"""
    list_display = [
        'ngay',
        'doanh_thu_formatted',
        'so_don_hang',
        'so_khach_hang',
        'so_san_pham_ban',
        'gia_tri_trung_binh_formatted',
        'tien_giam_formatted',
    ]
    list_filter = ['ngay']
    search_fields = ['ngay']
    date_hierarchy = 'ngay'
    readonly_fields = ['ngay_tao']
    
    def doanh_thu_formatted(self, obj):
        return f"{obj.doanh_thu:,.0f} đ"
    doanh_thu_formatted.short_description = 'Doanh thu'
    doanh_thu_formatted.admin_order_field = 'doanh_thu'
    
    def gia_tri_trung_binh_formatted(self, obj):
        return f"{obj.gia_tri_trung_binh:,.0f} đ"
    gia_tri_trung_binh_formatted.short_description = 'Giá trị TB'
    
    def tien_giam_formatted(self, obj):
        return f"{obj.tien_giam:,.0f} đ"
    tien_giam_formatted.short_description = 'Tiền giảm'
    
    def has_add_permission(self, request):
        """Không cho phép thêm thủ công - chỉ tạo bằng command"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Không cho phép xóa"""
        return False


@admin.register(ThongKeVoucher)
class ThongKeVoucherAdmin(admin.ModelAdmin):
    """Admin cho thống kê voucher"""
    list_display = [
        'ma_giam_gia',
        'thang',
        'so_don_su_dung',
        'tong_giam_formatted',
        'tong_doanh_thu_formatted',
        'roi_formatted',
        'ti_le_su_dung_formatted',
    ]
    list_filter = ['thang', 'ma_giam_gia']
    search_fields = ['ma_giam_gia__ma_code', 'ma_giam_gia__ten_chuong_trinh']
    date_hierarchy = 'thang'
    readonly_fields = ['ngay_cap_nhat']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('ma_giam_gia', 'thang')
        }),
        ('Số liệu thống kê', {
            'fields': (
                'so_don_su_dung',
                'tong_giam',
                'tong_doanh_thu',
                'gia_tri_don_hang_tb',
                'ti_le_su_dung',
                'roi',
            )
        }),
        ('Hệ thống', {
            'fields': ('ngay_cap_nhat',),
            'classes': ('collapse',)
        }),
    )
    
    def tong_giam_formatted(self, obj):
        return f"{obj.tong_giam:,.0f} đ"
    tong_giam_formatted.short_description = 'Tổng giảm'
    tong_giam_formatted.admin_order_field = 'tong_giam'
    
    def tong_doanh_thu_formatted(self, obj):
        return f"{obj.tong_doanh_thu:,.0f} đ"
    tong_doanh_thu_formatted.short_description = 'Doanh thu'
    tong_doanh_thu_formatted.admin_order_field = 'tong_doanh_thu'
    
    def roi_formatted(self, obj):
        if obj.roi > 0:
            return f"+{obj.roi:.1f}%"
        return f"{obj.roi:.1f}%"
    roi_formatted.short_description = 'ROI'
    roi_formatted.admin_order_field = 'roi'
    
    def ti_le_su_dung_formatted(self, obj):
        return f"{obj.ti_le_su_dung:.1f}%"
    ti_le_su_dung_formatted.short_description = 'Tỷ lệ SD'
    
    def has_add_permission(self, request):
        """Không cho phép thêm thủ công"""
        return False


@admin.register(PhanKhucKhachHang)
class PhanKhucKhachHangAdmin(admin.ModelAdmin):
    """Admin cho phân khúc khách hàng"""
    list_display = [
        'nguoi_dung',
        'segment_colored',
        'rfm_score',
        'tong_chi_tieu_formatted',
        'tong_so_don_hang',
        'ngay_mua_cuoi',
        'so_ngay_khong_mua',
    ]
    list_filter = ['segment', 'recency_score', 'frequency_score', 'monetary_score']
    search_fields = ['nguoi_dung__username', 'nguoi_dung__email']
    readonly_fields = ['rfm_score', 'lan_cuoi_tinh']
    
    fieldsets = (
        ('Khách hàng', {
            'fields': ('nguoi_dung', 'segment', 'rfm_score')
        }),
        ('RFM Scores', {
            'fields': (
                ('recency_score', 'frequency_score', 'monetary_score'),
            )
        }),
        ('Thông tin chi tiết', {
            'fields': (
                'ngay_mua_cuoi',
                'so_ngay_khong_mua',
                'tong_so_don_hang',
                'tong_chi_tieu',
                'gia_tri_don_hang_tb',
            )
        }),
        ('Ghi chú', {
            'fields': ('ghi_chu', 'lan_cuoi_tinh'),
            'classes': ('collapse',)
        }),
    )
    
    def segment_colored(self, obj):
        colors = {
            'vip': '#FF6B6B',
            'loyal': '#4ECDC4',
            'at_risk': '#FFD93D',
            'lost': '#95A5A6',
            'new': '#A8E6CF',
            'regular': '#74B9FF',
            'promising': '#FD79A8',
            'need_attention': '#FDCB6E',
        }
        color = colors.get(obj.segment, '#BDC3C7')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_segment_display()
        )
    segment_colored.short_description = 'Phân khúc'
    segment_colored.admin_order_field = 'segment'
    
    def tong_chi_tieu_formatted(self, obj):
        return f"{obj.tong_chi_tieu:,.0f} đ"
    tong_chi_tieu_formatted.short_description = 'Tổng chi tiêu'
    tong_chi_tieu_formatted.admin_order_field = 'tong_chi_tieu'
    
    actions = ['cap_nhat_phan_khuc']
    
    def cap_nhat_phan_khuc(self, request, queryset):
        """Action để cập nhật phân khúc cho các khách hàng đã chọn"""
        for phan_khuc in queryset:
            phan_khuc.xac_dinh_segment()
            phan_khuc.save()
        self.message_user(request, f"Đã cập nhật phân khúc cho {queryset.count()} khách hàng")
    cap_nhat_phan_khuc.short_description = "Cập nhật phân khúc RFM"
    
    def has_add_permission(self, request):
        """Không cho phép thêm thủ công"""
        return False

