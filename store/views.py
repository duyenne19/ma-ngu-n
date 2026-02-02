from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg, F, Q, Max
from django.db.models.functions import TruncDate, TruncMonth
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    DonHang, ChiTietDonHang, SanPham, DanhMuc, MaGiamGia,
    BaoCaoDoanThu, ThongKeVoucher, PhanKhucKhachHang,
    Profile, GioHang, ThongBao
)

def home(request):
    return render(request, 'store/index.html', {})

def detail(request, slug):
    return render(request, 'store/detail.html', {})

def all_categories(request):
    return render(request, 'store/categories.html', {})

def introduce(request):
    return render(request, 'store/introduce.html')

def category_products(request, slug):
    return render(request, 'store/category_products.html', {})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'account/register.html', {})
    
    def post(self, request):
        return redirect('store:login')

def profile(request):
    return render(request, 'account/profile.html', {})

class AddressView(View):
    def get(self, request):
        return render(request, 'account/add_address.html', {})

    def post(self, request):
        return redirect('store:profile')

def remove_address(request, id):
    return redirect('store:profile')

def add_to_cart(request):
    return redirect('store:home')

def cart(request):
    return render(request, 'store/cart.html', {})

def remove_cart(request, cart_id):
    return redirect('store:cart')

def plus_cart(request, cart_id):
    return redirect('store:cart')

def minus_cart(request, cart_id):
    return redirect('store:cart')

def checkout(request):
    return render(request, 'store/checkout.html', {})

def checkout_test(request):
    return render(request, 'store/checkout.html', {})

def orders(request):
    return render(request, 'store/orders.html', {})

def billing(request):
    return render(request, 'store/billing.html', {})

def purchase_orders(request):
    return render(request, 'store/purchase_orders.html', {})

def invoice(request):
    return render(request, 'store/invoice.html', {})

def like_products(request):
    return render(request, 'store/like_products.html', {})

def remove_like(request, favorite_id):
    return redirect('store:like-products')

def shop(request):
    return render(request, 'store/shop.html', {})

def test(request):
    return render(request, 'store/test.html', {})

def add_notifi_like_home(request):
    return redirect('store:home')

def add_notifi_like_cp(request):
    return redirect('store:home')

def add_notifi_like_p(request):
    return redirect('store:home')

def add_notifi_like_rp(request):
    return redirect('store:home')


# ==================== DASHBOARD BÁO CÁO & THỐNG KÊ ====================

@staff_member_required
def dashboard_home(request):
    """Dashboard tổng quan - Trang chủ báo cáo"""
    
    # Lấy ngày hiện tại
    ngay_hom_nay = datetime.now().date()
    dau_thang = ngay_hom_nay.replace(day=1)
    
    # KPI - Doanh thu hôm nay
    doanh_thu_hom_nay = DonHang.objects.filter(
        trang_thai_don_hang='delivered',
        ngay_dat__date=ngay_hom_nay
    ).aggregate(
        tong=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
        so_don=Count('id')
    )
    
    # KPI - Doanh thu tháng này
    doanh_thu_thang_nay = DonHang.objects.filter(
        trang_thai_don_hang='delivered',
        ngay_dat__date__gte=dau_thang
    ).aggregate(
        tong=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
        so_don=Count('id')
    )
    
    # KPI - Đơn hàng chờ xử lý
    don_hang_cho_xu_ly = DonHang.objects.filter(
        trang_thai_don_hang='pending'
    ).count()
    
    # KPI - Khách hàng mới (7 ngày)
    khach_hang_moi = Profile.objects.filter(
        ngay_tao__gte=ngay_hom_nay - timedelta(days=7)
    ).count()
    
    # Doanh thu 7 ngày gần nhất
    doanh_thu_7_ngay = list(BaoCaoDoanThu.objects.filter(
        ngay__gte=ngay_hom_nay - timedelta(days=7)
    ).order_by('ngay').values('ngay', 'doanh_thu', 'so_don_hang'))
    
    # Top 5 sản phẩm bán chạy
    top_san_pham = ChiTietDonHang.objects.filter(
        don_hang__trang_thai_don_hang='delivered',
        don_hang__ngay_dat__gte=ngay_hom_nay - timedelta(days=30)
    ).values(
        'san_pham__ten_san_pham',
        'san_pham__ma_san_pham'
    ).annotate(
        so_luong_ban=Sum('so_luong'),
        doanh_thu=Sum(F('so_luong') * F('gia'))
    ).order_by('-so_luong_ban')[:5]
    
    # Phân bố khách hàng theo phân khúc
    phan_khuc_stats = PhanKhucKhachHang.objects.values('segment').annotate(
        so_luong=Count('id')
    ).order_by('-so_luong')
    
    context = {
        'doanh_thu_hom_nay': doanh_thu_hom_nay['tong'] or 0,
        'so_don_hom_nay': doanh_thu_hom_nay['so_don'] or 0,
        'doanh_thu_thang_nay': doanh_thu_thang_nay['tong'] or 0,
        'so_don_thang_nay': doanh_thu_thang_nay['so_don'] or 0,
        'don_hang_cho_xu_ly': don_hang_cho_xu_ly,
        'khach_hang_moi': khach_hang_moi,
        'doanh_thu_7_ngay': doanh_thu_7_ngay,
        'top_san_pham': list(top_san_pham),
        'phan_khuc_stats': list(phan_khuc_stats),
    }
    
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def dashboard_doanh_thu(request):
    """Dashboard doanh thu chi tiết"""
    
    # Lấy tham số thời gian từ query string
    ngay_bat_dau = request.GET.get('tu_ngay')
    ngay_ket_thuc = request.GET.get('den_ngay')
    
    ngay_hom_nay = datetime.now().date()
    
    # Mặc định: 30 ngày gần nhất
    if not ngay_bat_dau:
        ngay_bat_dau = ngay_hom_nay - timedelta(days=30)
    else:
        ngay_bat_dau = datetime.strptime(ngay_bat_dau, '%Y-%m-%d').date()
    
    if not ngay_ket_thuc:
        ngay_ket_thuc = ngay_hom_nay
    else:
        ngay_ket_thuc = datetime.strptime(ngay_ket_thuc, '%Y-%m-%d').date()
    
    # Báo cáo doanh thu theo ngày
    bao_cao_theo_ngay = BaoCaoDoanThu.objects.filter(
        ngay__gte=ngay_bat_dau,
        ngay__lte=ngay_ket_thuc
    ).order_by('ngay')
    
    # Thống kê tổng hợp
    tong_hop = bao_cao_theo_ngay.aggregate(
        tong_doanh_thu=Sum('doanh_thu'),
        tong_don_hang=Sum('so_don_hang'),
        tong_san_pham=Sum('so_san_pham_ban'),
        gia_tri_tb=Avg('gia_tri_trung_binh')
    )
    
    # Doanh thu theo tháng (12 tháng)
    doanh_thu_thang = DonHang.objects.filter(
        trang_thai_don_hang='delivered',
        ngay_dat__gte=datetime.now() - timedelta(days=365)
    ).annotate(
        thang=TruncMonth('ngay_dat')
    ).values('thang').annotate(
        doanh_thu=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
        so_don=Count('id')
    ).order_by('thang')
    
    context = {
        'ngay_bat_dau': ngay_bat_dau,
        'ngay_ket_thuc': ngay_ket_thuc,
        'bao_cao_theo_ngay': bao_cao_theo_ngay,
        'tong_hop': tong_hop,
        'doanh_thu_thang': list(doanh_thu_thang),
    }
    
    return render(request, 'dashboard/doanh_thu.html', context)


@staff_member_required
def dashboard_san_pham(request):
    """Dashboard sản phẩm bán chạy"""
    
    ngay_hom_nay = datetime.now().date()
    
    # Top sản phẩm bán chạy 30 ngày
    top_san_pham_30_ngay = ChiTietDonHang.objects.filter(
        don_hang__trang_thai_don_hang='delivered',
        don_hang__ngay_dat__gte=ngay_hom_nay - timedelta(days=30)
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
    
    # Sản phẩm bán chậm
    san_pham_ban_cham = SanPham.objects.annotate(
        da_ban_30_ngay=Sum(
            'chitietdonhang__so_luong',
            filter=Q(
                chitietdonhang__don_hang__trang_thai_don_hang='delivered',
                chitietdonhang__don_hang__ngay_dat__gte=ngay_hom_nay - timedelta(days=30)
            )
        )
    ).filter(
        trang_thai='active',
        so_luong_ton__gt=0
    ).order_by('da_ban_30_ngay')[:20]
    
    # Doanh thu theo danh mục
    doanh_thu_danh_muc = ChiTietDonHang.objects.filter(
        don_hang__trang_thai_don_hang='delivered',
        don_hang__ngay_dat__gte=ngay_hom_nay - timedelta(days=30)
    ).values(
        'san_pham__danh_muc__ten_danh_muc'
    ).annotate(
        doanh_thu=Sum(F('so_luong') * F('gia')),
        so_luong=Sum('so_luong')
    ).order_by('-doanh_thu')
    
    # Sản phẩm sắp hết hàng
    san_pham_sap_het = SanPham.objects.filter(
        trang_thai='active',
        so_luong_ton__lte=F('so_luong_canh_bao')
    ).order_by('so_luong_ton')[:10]
    
    context = {
        'top_san_pham': list(top_san_pham_30_ngay),
        'san_pham_ban_cham': san_pham_ban_cham,
        'doanh_thu_danh_muc': list(doanh_thu_danh_muc),
        'san_pham_sap_het': san_pham_sap_het,
    }
    
    return render(request, 'dashboard/san_pham.html', context)


@staff_member_required
def dashboard_khach_hang(request):
    """Dashboard phân tích khách hàng"""
    
    # Phân khúc RFM
    phan_khuc_rfm = PhanKhucKhachHang.objects.select_related('nguoi_dung').order_by(
        '-tong_chi_tieu'
    )
    
    # Thống kê theo segment
    segment_stats_raw = PhanKhucKhachHang.objects.values('segment').annotate(
        so_luong=Count('id'),
        tong_chi_tieu=Sum('tong_chi_tieu')
    ).order_by('-tong_chi_tieu')
    
    # Tính trung bình chi tiêu
    segment_stats = []
    for stat in segment_stats_raw:
        stat['trung_binh_chi_tieu'] = stat['tong_chi_tieu'] / stat['so_luong'] if stat['so_luong'] > 0 else 0
        segment_stats.append(stat)
    
    # Top 20 khách hàng VIP
    top_khach_hang = phan_khuc_rfm.filter(
        segment__in=['vip', 'loyal']
    )[:20]
    
    # Khách hàng nguy cơ rời bỏ
    khach_hang_at_risk = phan_khuc_rfm.filter(
        segment__in=['at_risk', 'need_attention']
    )[:20]
    
    context = {
        'segment_stats': list(segment_stats),
        'top_khach_hang': top_khach_hang,
        'khach_hang_at_risk': khach_hang_at_risk,
        'phan_khuc_rfm': phan_khuc_rfm[:50],  # 50 khách hàng đầu
    }
    
    return render(request, 'dashboard/khach_hang.html', context)


@staff_member_required
def dashboard_voucher(request):
    """Dashboard hiệu quả mã giảm giá"""
    
    # Thống kê voucher
    thong_ke_voucher = ThongKeVoucher.objects.select_related(
        'ma_giam_gia'
    ).order_by('-thang', '-roi')
    
    # Voucher đang hoạt động
    voucher_active = MaGiamGia.objects.filter(
        trang_thai=True,
        ngay_bat_dau__lte=datetime.now(),
        ngay_ket_thuc__gte=datetime.now()
    ).annotate(
        ti_le_su_dung=F('da_su_dung') * 100.0 / F('so_luong')
    ).order_by('-da_su_dung')
    
    # Top voucher ROI cao nhất
    top_voucher_roi = thong_ke_voucher.order_by('-roi')[:10]
    
    # Voucher hiệu quả thấp
    voucher_hieu_qua_thap = thong_ke_voucher.filter(
        roi__lt=100
    ).order_by('roi')[:10]
    
    context = {
        'thong_ke_voucher': thong_ke_voucher[:30],
        'voucher_active': voucher_active,
        'top_voucher_roi': top_voucher_roi,
        'voucher_hieu_qua_thap': voucher_hieu_qua_thap,
    }
    
    return render(request, 'dashboard/voucher.html', context)


# ==================== API ENDPOINTS CHO CHARTS ====================

@staff_member_required
def api_doanh_thu_chart(request):
    """API trả về dữ liệu doanh thu cho chart"""
    
    so_ngay = int(request.GET.get('days', 30))
    ngay_hom_nay = datetime.now().date()
    ngay_bat_dau = ngay_hom_nay - timedelta(days=so_ngay)
    
    data = list(BaoCaoDoanThu.objects.filter(
        ngay__gte=ngay_bat_dau
    ).order_by('ngay').values('ngay', 'doanh_thu', 'so_don_hang'))
    
    # Format cho Chart.js
    labels = [item['ngay'].strftime('%d/%m') for item in data]
    doanh_thu = [float(item['doanh_thu']) for item in data]
    don_hang = [item['so_don_hang'] for item in data]
    
    return JsonResponse({
        'labels': labels,
        'datasets': [
            {
                'label': 'Doanh thu (VND)',
                'data': doanh_thu,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'yAxisID': 'y',
            },
            {
                'label': 'Số đơn hàng',
                'data': don_hang,
                'borderColor': 'rgb(255, 99, 132)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'yAxisID': 'y1',
            }
        ]
    })


@staff_member_required
def api_top_san_pham(request):
    """API trả về top sản phẩm bán chạy"""
    
    limit = int(request.GET.get('limit', 10))
    ngay_hom_nay = datetime.now().date()
    
    data = list(ChiTietDonHang.objects.filter(
        don_hang__trang_thai_don_hang='delivered',
        don_hang__ngay_dat__gte=ngay_hom_nay - timedelta(days=30)
    ).values(
        'san_pham__ten_san_pham'
    ).annotate(
        so_luong=Sum('so_luong')
    ).order_by('-so_luong')[:limit])
    
    labels = [item['san_pham__ten_san_pham'] for item in data]
    values = [item['so_luong'] for item in data]
    
    return JsonResponse({
        'labels': labels,
        'data': values
    })


@staff_member_required
def api_phan_khuc_khach_hang(request):
    """API trả về phân bố phân khúc khách hàng"""
    
    data = list(PhanKhucKhachHang.objects.values('segment').annotate(
        so_luong=Count('id')
    ).order_by('-so_luong'))
    
    segment_names = {
        'vip': 'VIP',
        'loyal': 'Trung thành',
        'at_risk': 'Nguy cơ rời bỏ',
        'lost': 'Đã mất',
        'new': 'Mới',
        'regular': 'Thường xuyên',
        'promising': 'Tiềm năng',
        'need_attention': 'Cần chăm sóc'
    }
    
    labels = [segment_names.get(item['segment'], item['segment']) for item in data]
    values = [item['so_luong'] for item in data]
    
    colors = [
        '#FF6B6B', '#4ECDC4', '#FFD93D', '#95A5A6',
        '#A8E6CF', '#74B9FF', '#FD79A8', '#FDCB6E'
    ]
    
    return JsonResponse({
        'labels': labels,
        'data': values,
        'backgroundColor': colors[:len(labels)]
    })

class SearchView(View):
    def get(self, request):
        return render(request, 'store/search.html', {})
