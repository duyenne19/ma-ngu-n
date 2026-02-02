"""
Management command: Cập nhật báo cáo doanh thu hàng ngày
Sử dụng: python manage.py cap_nhat_bao_cao_doanh_thu
"""

from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Avg, F, Q
from datetime import datetime, timedelta
from store.models import DonHang, BaoCaoDoanThu, ChiTietDonHang


class Command(BaseCommand):
    help = 'Cập nhật báo cáo doanh thu hàng ngày'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--ngay',
            type=str,
            help='Ngày cần cập nhật (YYYY-MM-DD). Mặc định: hôm qua'
        )
        parser.add_argument(
            '--thang',
            type=str,
            help='Cập nhật cả tháng (YYYY-MM)'
        )
    
    def handle(self, *args, **options):
        if options['thang']:
            # Cập nhật cả tháng
            self.cap_nhat_thang(options['thang'])
        elif options['ngay']:
            # Cập nhật ngày cụ thể
            ngay = datetime.strptime(options['ngay'], '%Y-%m-%d').date()
            self.cap_nhat_ngay(ngay)
        else:
            # Mặc định: cập nhật hôm qua
            ngay_hom_qua = datetime.now().date() - timedelta(days=1)
            self.cap_nhat_ngay(ngay_hom_qua)
    
    def cap_nhat_ngay(self, ngay):
        """Cập nhật báo cáo cho một ngày"""
        self.stdout.write(f'📊 Đang cập nhật báo cáo ngày {ngay}...')
        
        # Lấy các đơn hàng đã giao trong ngày
        don_hang_list = DonHang.objects.filter(
            trang_thai_don_hang='delivered',
            ngay_dat__date=ngay
        )
        
        if not don_hang_list.exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️ Không có đơn hàng nào trong ngày {ngay}')
            )
            return
        
        # Tính toán các chỉ số
        stats = don_hang_list.aggregate(
            so_don=Count('id'),
            doanh_thu=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
            tien_giam=Sum('tien_giam'),
            phi_ship=Sum('phi_ship'),
            gia_tri_tb=Avg(F('tong_tien') - F('tien_giam') + F('phi_ship')),
            so_khach=Count('nguoi_dung', distinct=True)
        )
        
        # Tính số sản phẩm đã bán
        so_san_pham_ban = ChiTietDonHang.objects.filter(
            don_hang__in=don_hang_list
        ).aggregate(
            tong=Sum('so_luong')
        )['tong'] or 0
        
        # Lưu hoặc cập nhật báo cáo
        bao_cao, created = BaoCaoDoanThu.objects.update_or_create(
            ngay=ngay,
            defaults={
                'so_don_hang': stats['so_don'] or 0,
                'doanh_thu': stats['doanh_thu'] or 0,
                'tien_giam': stats['tien_giam'] or 0,
                'phi_ship': stats['phi_ship'] or 0,
                'gia_tri_trung_binh': stats['gia_tri_tb'] or 0,
                'so_khach_hang': stats['so_khach'] or 0,
                'so_san_pham_ban': so_san_pham_ban,
            }
        )
        
        action = 'Tạo mới' if created else 'Cập nhật'
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ {action} báo cáo {ngay}:\n'
                f'   - Đơn hàng: {stats["so_don"]}\n'
                f'   - Doanh thu: {stats["doanh_thu"]:,.0f} đ\n'
                f'   - Khách hàng: {stats["so_khach"]}\n'
                f'   - Sản phẩm bán: {so_san_pham_ban}'
            )
        )
    
    def cap_nhat_thang(self, thang_str):
        """Cập nhật báo cáo cho cả tháng"""
        try:
            nam, thang = map(int, thang_str.split('-'))
            ngay_dau_thang = datetime(nam, thang, 1).date()
            
            # Tính ngày cuối tháng
            if thang == 12:
                ngay_dau_thang_sau = datetime(nam + 1, 1, 1).date()
            else:
                ngay_dau_thang_sau = datetime(nam, thang + 1, 1).date()
            
            ngay_cuoi_thang = ngay_dau_thang_sau - timedelta(days=1)
            
            self.stdout.write(
                f'📊 Cập nhật báo cáo từ {ngay_dau_thang} đến {ngay_cuoi_thang}'
            )
            
            # Cập nhật từng ngày
            ngay_hien_tai = ngay_dau_thang
            dem = 0
            
            while ngay_hien_tai <= ngay_cuoi_thang:
                self.cap_nhat_ngay(ngay_hien_tai)
                ngay_hien_tai += timedelta(days=1)
                dem += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Hoàn thành cập nhật {dem} ngày!')
            )
            
        except ValueError:
            self.stdout.write(
                self.style.ERROR('❌ Định dạng tháng không đúng. Sử dụng: YYYY-MM')
            )
