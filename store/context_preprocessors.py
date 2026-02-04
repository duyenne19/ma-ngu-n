from operator import le
from .models import DanhMuc, GioHang, ChiTietGioHang, ThongBao



def store_menu(request):
    categories = DanhMuc.objects.filter(hien_thi=True)
    context = {
        'categories_menu': categories,
    }
    return context

def notification_list(request):    
    if request.user.is_authenticated:
        user = request.user
        notification = ThongBao.objects.filter(nguoi_dung=user)
        t=1
        if len(notification)==0: t=0
        if len(notification)>=6:
            result = reversed(list(notification[len(notification)-6:len(notification)]))
            res = result
        else:
            res=reversed(list(notification))
        
        context = {
            'notification_list': res, 
            'length' :t,         
        }         
    else:
        context = {            
        }
    
    return context

def cart_menu(request):
    if request.user.is_authenticated:
        # Lấy hoặc tạo giỏ hàng
        gio_hang, created = GioHang.objects.get_or_create(nguoi_dung=request.user)
        cart_items = gio_hang.chi_tiet.all()
        context = {
            'cart_items': cart_items,
            'gio_hang': gio_hang,
        }
    else:
        context = {}
    return context