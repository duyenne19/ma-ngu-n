"""
Management command: Cập nhật phân khúc khách hàng theo RFM
Sử dụng: python manage.py cap_nhat_phan_khuc_khach_hang
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Max, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from store.models import DonHang, PhanKhucKhachHang


class Command(BaseCommand):
    help = 'Cập nhật phân khúc khách hàng theo RFM (Recency, Frequency, Monetary)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='ID người dùng cụ thể cần cập nhật'
        )
    
    def handle(self, *args, **options):
        if options['user_id']:
            # Cập nhật 1 user cụ thể
            try:
                user = User.objects.get(id=options['user_id'])
                self.cap_nhat_user(user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Không tìm thấy user ID {options["user_id"]}')
                )
        else:
            # Cập nhật tất cả users có đơn hàng
            self.cap_nhat_tat_ca()
    
    def cap_nhat_tat_ca(self):
        """Cập nhật phân khúc cho tất cả khách hàng"""
        self.stdout.write('📊 Bắt đầu phân tích RFM cho tất cả khách hàng...\n')
        
        # Lấy tất cả users có ít nhất 1 đơn hàng delivered
        users = User.objects.filter(
            don_hang_list__trang_thai_don_hang='delivered'
        ).distinct()
        
        total = users.count()
        if total == 0:
            self.stdout.write(
                self.style.WARNING('⚠️ Không có khách hàng nào có đơn hàng')
            )
            return
        
        self.stdout.write(f'Tìm thấy {total} khách hàng cần phân tích\n')
        
        # Tính RFM cho từng user
        rfm_data = []
        for user in users:
            data = self.tinh_rfm_raw(user)
            if data:
                rfm_data.append(data)
        
        # Tính quartiles để phân loại scores (1-5)
        self.gan_rfm_scores(rfm_data)
        
        # Lưu vào database
        dem_moi = 0
        dem_cap_nhat = 0
        
        for data in rfm_data:
            phan_khuc, created = PhanKhucKhachHang.objects.update_or_create(
                nguoi_dung=data['user'],
                defaults={
                    'recency_score': data['r_score'],
                    'frequency_score': data['f_score'],
                    'monetary_score': data['m_score'],
                    'ngay_mua_cuoi': data['ngay_mua_cuoi'],
                    'so_ngay_khong_mua': data['so_ngay_khong_mua'],
                    'tong_so_don_hang': data['frequency'],
                    'tong_chi_tieu': data['monetary'],
                    'gia_tri_don_hang_tb': data['gia_tri_tb'],
                }
            )
            
            if created:
                dem_moi += 1
            else:
                dem_cap_nhat += 1
            
            # Hiển thị kết quả
            segment_icons = {
                'vip': '👑',
                'loyal': '💎',
                'at_risk': '⚠️',
                'lost': '💔',
                'new': '🆕',
                'regular': '👤',
                'promising': '🌟',
                'need_attention': '🔔',
            }
            icon = segment_icons.get(phan_khuc.segment, '❓')
            
            self.stdout.write(
                f'{icon} {data["user"].username:20} | '
                f'RFM: {phan_khuc.rfm_score} | '
                f'{phan_khuc.get_segment_display():20} | '
                f'{data["monetary"]:>12,.0f}đ | '
                f'{data["frequency"]:>3} đơn'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Hoàn thành!\n'
                f'   - Tạo mới: {dem_moi}\n'
                f'   - Cập nhật: {dem_cap_nhat}\n'
                f'   - Tổng: {dem_moi + dem_cap_nhat}'
            )
        )
    
    def cap_nhat_user(self, user):
        """Cập nhật phân khúc cho 1 user"""
        self.stdout.write(f'📊 Phân tích RFM cho user: {user.username}')
        
        data = self.tinh_rfm_raw(user)
        if not data:
            self.stdout.write(
                self.style.WARNING('⚠️ User chưa có đơn hàng nào')
            )
            return
        
        # Đơn giản hóa: dùng giá trị tuyệt đối để phân score
        data['r_score'] = self.tinh_recency_score(data['so_ngay_khong_mua'])
        data['f_score'] = self.tinh_frequency_score(data['frequency'])
        data['m_score'] = self.tinh_monetary_score(data['monetary'])
        
        # Lưu vào database
        phan_khuc, created = PhanKhucKhachHang.objects.update_or_create(
            nguoi_dung=user,
            defaults={
                'recency_score': data['r_score'],
                'frequency_score': data['f_score'],
                'monetary_score': data['m_score'],
                'ngay_mua_cuoi': data['ngay_mua_cuoi'],
                'so_ngay_khong_mua': data['so_ngay_khong_mua'],
                'tong_so_don_hang': data['frequency'],
                'tong_chi_tieu': data['monetary'],
                'gia_tri_don_hang_tb': data['gia_tri_tb'],
            }
        )
        
        action = 'Tạo mới' if created else 'Cập nhật'
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ {action}:\n'
                f'   - RFM Score: {phan_khuc.rfm_score}\n'
                f'   - Phân khúc: {phan_khuc.get_segment_display()}\n'
                f'   - Recency: {data["so_ngay_khong_mua"]} ngày (Score: {data["r_score"]})\n'
                f'   - Frequency: {data["frequency"]} đơn (Score: {data["f_score"]})\n'
                f'   - Monetary: {data["monetary"]:,.0f}đ (Score: {data["m_score"]})'
            )
        )
    
    def tinh_rfm_raw(self, user):
        """Tính các giá trị RFM thô cho user"""
        # Lấy thống kê đơn hàng
        stats = DonHang.objects.filter(
            nguoi_dung=user,
            trang_thai_don_hang='delivered'
        ).aggregate(
            ngay_mua_cuoi=Max('ngay_dat'),
            so_don=Count('id'),
            tong_tien=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')),
            gia_tri_tb=Sum(F('tong_tien') - F('tien_giam') + F('phi_ship')) / Count('id')
        )
        
        if not stats['ngay_mua_cuoi']:
            return None
        
        # Tính số ngày không mua
        ngay_mua_cuoi = stats['ngay_mua_cuoi']
        if timezone.is_aware(ngay_mua_cuoi):
            ngay_mua_cuoi = ngay_mua_cuoi.date()
        
        so_ngay_khong_mua = (datetime.now().date() - ngay_mua_cuoi).days
        
        return {
            'user': user,
            'ngay_mua_cuoi': ngay_mua_cuoi,
            'so_ngay_khong_mua': so_ngay_khong_mua,
            'frequency': stats['so_don'] or 0,
            'monetary': stats['tong_tien'] or Decimal(0),
            'gia_tri_tb': stats['gia_tri_tb'] or Decimal(0),
        }
    
    def gan_rfm_scores(self, rfm_data):
        """Gán scores 1-5 dựa trên quartiles"""
        if not rfm_data:
            return
        
        # Sắp xếp để tìm quartiles
        recency_values = sorted([d['so_ngay_khong_mua'] for d in rfm_data])
        frequency_values = sorted([d['frequency'] for d in rfm_data], reverse=True)
        monetary_values = sorted([d['monetary'] for d in rfm_data], reverse=True)
        
        # Tính quartiles (chia thành 5 nhóm)
        def get_quartile_value(values, percentile):
            n = len(values)
            index = int(n * percentile / 100)
            return values[min(index, n-1)]
        
        r_quartiles = [
            get_quartile_value(recency_values, p) 
            for p in [20, 40, 60, 80]
        ]
        f_quartiles = [
            get_quartile_value(frequency_values, p) 
            for p in [20, 40, 60, 80]
        ]
        m_quartiles = [
            get_quartile_value(monetary_values, p) 
            for p in [20, 40, 60, 80]
        ]
        
        # Gán scores
        for data in rfm_data:
            # Recency: càng gần đây càng cao (đảo ngược)
            if data['so_ngay_khong_mua'] <= r_quartiles[0]:
                data['r_score'] = 5
            elif data['so_ngay_khong_mua'] <= r_quartiles[1]:
                data['r_score'] = 4
            elif data['so_ngay_khong_mua'] <= r_quartiles[2]:
                data['r_score'] = 3
            elif data['so_ngay_khong_mua'] <= r_quartiles[3]:
                data['r_score'] = 2
            else:
                data['r_score'] = 1
            
            # Frequency: càng nhiều càng cao
            if data['frequency'] >= f_quartiles[0]:
                data['f_score'] = 5
            elif data['frequency'] >= f_quartiles[1]:
                data['f_score'] = 4
            elif data['frequency'] >= f_quartiles[2]:
                data['f_score'] = 3
            elif data['frequency'] >= f_quartiles[3]:
                data['f_score'] = 2
            else:
                data['f_score'] = 1
            
            # Monetary: càng nhiều càng cao
            if data['monetary'] >= m_quartiles[0]:
                data['m_score'] = 5
            elif data['monetary'] >= m_quartiles[1]:
                data['m_score'] = 4
            elif data['monetary'] >= m_quartiles[2]:
                data['m_score'] = 3
            elif data['monetary'] >= m_quartiles[3]:
                data['m_score'] = 2
            else:
                data['m_score'] = 1
    
    def tinh_recency_score(self, so_ngay):
        """Tính recency score đơn giản"""
        if so_ngay <= 30:
            return 5
        elif so_ngay <= 60:
            return 4
        elif so_ngay <= 90:
            return 3
        elif so_ngay <= 180:
            return 2
        else:
            return 1
    
    def tinh_frequency_score(self, so_don):
        """Tính frequency score đơn giản"""
        if so_don >= 10:
            return 5
        elif so_don >= 7:
            return 4
        elif so_don >= 5:
            return 3
        elif so_don >= 3:
            return 2
        else:
            return 1
    
    def tinh_monetary_score(self, tong_tien):
        """Tính monetary score đơn giản"""
        if tong_tien >= 10000000:
            return 5
        elif tong_tien >= 5000000:
            return 4
        elif tong_tien >= 2000000:
            return 3
        elif tong_tien >= 1000000:
            return 2
        else:
            return 1
