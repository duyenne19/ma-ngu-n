"""
Management command: Cập nhật thống kê hiệu quả voucher
Sử dụng: python manage.py cap_nhat_thong_ke_voucher
"""

from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Avg, F
from datetime import datetime, timedelta
from decimal import Decimal
from store.models import MaGiamGia, ThongKeVoucher, DonHang, DonHang_MaGiamGia


class Command(BaseCommand):
    help = 'Cập nhật thống kê hiệu quả mã giảm giá'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--thang',
            type=str,
            help='Tháng cần thống kê (YYYY-MM). Mặc định: tháng trước'
        )
        parser.add_argument(
            '--tat-ca',
            action='store_true',
            help='Thống kê tất cả mã giảm giá đang hoạt động'
        )
    
    def handle(self, *args, **options):
        if options['tat_ca']:
            self.thong_ke_tat_ca()
        elif options['thang']:
            thang = datetime.strptime(options['thang'], '%Y-%m').date()
            self.thong_ke_thang(thang)
        else:
            # Mặc định: tháng trước
            ngay_hien_tai = datetime.now().date()
            thang_truoc = (ngay_hien_tai.replace(day=1) - timedelta(days=1)).replace(day=1)
            self.thong_ke_thang(thang_truoc)
    
    def thong_ke_thang(self, thang):
        """Thống kê voucher cho một tháng cụ thể"""
        self.stdout.write(f'📊 Thống kê voucher tháng {thang.strftime("%m/%Y")}...')
        
        # Tính ngày đầu và cuối tháng
        ngay_dau = thang
        if thang.month == 12:
            ngay_cuoi = datetime(thang.year + 1, 1, 1).date() - timedelta(days=1)
        else:
            ngay_cuoi = datetime(thang.year, thang.month + 1, 1).date() - timedelta(days=1)
        
        # Lấy tất cả voucher đang/đã hoạt động trong tháng
        vouchers = MaGiamGia.objects.filter(
            ngay_bat_dau__lte=ngay_cuoi,
            ngay_ket_thuc__gte=ngay_dau
        )
        
        if not vouchers.exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️ Không có voucher nào trong tháng {thang.strftime("%m/%Y")}')
            )
            return
        
        dem = 0
        for voucher in vouchers:
            self.thong_ke_voucher(voucher, thang)
            dem += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Hoàn thành thống kê {dem} voucher!')
        )
    
    def thong_ke_voucher(self, voucher, thang):
        """Thống kê chi tiết cho một voucher trong tháng"""
        # Tính ngày đầu và cuối tháng
        ngay_dau = thang
        if thang.month == 12:
            ngay_cuoi = datetime(thang.year + 1, 1, 1).date() - timedelta(days=1)
        else:
            ngay_cuoi = datetime(thang.year, thang.month + 1, 1).date() - timedelta(days=1)
        
        # Lấy các đơn hàng sử dụng voucher trong tháng
        don_hang_voucher = DonHang_MaGiamGia.objects.filter(
            ma_giam_gia=voucher,
            don_hang__ngay_dat__date__gte=ngay_dau,
            don_hang__ngay_dat__date__lte=ngay_cuoi,
            don_hang__trang_thai_don_hang='delivered'
        )
        
        if not don_hang_voucher.exists():
            # Không có đơn hàng nào
            return
        
        # Tính toán các chỉ số
        stats = don_hang_voucher.aggregate(
            so_don=Count('don_hang', distinct=True),
            tong_giam=Sum('so_tien_giam'),
            tong_doanh_thu=Sum(
                F('don_hang__tong_tien') - 
                F('don_hang__tien_giam') + 
                F('don_hang__phi_ship')
            ),
            gia_tri_tb=Avg(F('don_hang__tong_tien'))
        )
        
        # Tính ROI
        tong_giam = stats['tong_giam'] or Decimal(0)
        tong_doanh_thu = stats['tong_doanh_thu'] or Decimal(0)
        
        if tong_giam > 0:
            roi = ((tong_doanh_thu - tong_giam) / tong_giam) * 100
        else:
            roi = Decimal(0)
        
        # Tính tỷ lệ sử dụng
        if voucher.so_luong > 0:
            ti_le_su_dung = (voucher.da_su_dung * 100) / voucher.so_luong
        else:
            ti_le_su_dung = Decimal(0)
        
        # Lưu hoặc cập nhật thống kê
        thong_ke, created = ThongKeVoucher.objects.update_or_create(
            ma_giam_gia=voucher,
            thang=thang,
            defaults={
                'so_don_su_dung': stats['so_don'] or 0,
                'tong_giam': tong_giam,
                'tong_doanh_thu': tong_doanh_thu,
                'gia_tri_don_hang_tb': stats['gia_tri_tb'] or Decimal(0),
                'roi': roi,
                'ti_le_su_dung': ti_le_su_dung,
            }
        )
        
        action = '🆕' if created else '🔄'
        self.stdout.write(
            f'{action} {voucher.ma_code}: '
            f'{stats["so_don"]} đơn, '
            f'{tong_doanh_thu:,.0f}đ, '
            f'ROI: {roi:.1f}%'
        )
    
    def thong_ke_tat_ca(self):
        """Thống kê tất cả voucher đang hoạt động"""
        self.stdout.write('📊 Thống kê tất cả voucher đang hoạt động...')
        
        # Lấy tháng hiện tại và 3 tháng trước
        ngay_hien_tai = datetime.now().date().replace(day=1)
        
        for i in range(4):  # 4 tháng (hiện tại + 3 tháng trước)
            if i == 0:
                thang = ngay_hien_tai
            else:
                # Lùi về tháng trước
                if ngay_hien_tai.month == 1:
                    thang = ngay_hien_tai.replace(year=ngay_hien_tai.year - 1, month=12)
                else:
                    thang = ngay_hien_tai.replace(month=ngay_hien_tai.month - 1)
                ngay_hien_tai = thang
            
            self.thong_ke_thang(thang)
            self.stdout.write('')
