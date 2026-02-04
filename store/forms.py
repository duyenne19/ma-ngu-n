from django.contrib.auth import password_validation
from store.models import DiaChi, SanPham, DanhGia, Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Nhập mật khẩu'}))
    password2 = forms.CharField(label="Xác nhận mật khẩu", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Nhập lại mật khẩu'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Nhập địa chỉ email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username':'Tên tài khoản','email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tên tài khoản'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(label=_("Tên tài khoản"),widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Mật khẩu"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class AddressForm(forms.ModelForm):
    class Meta:
        model = DiaChi
        fields = ['ten_nguoi_nhan', 'so_dien_thoai', 'dia_chi_chi_tiet', 'tinh_thanh', 'quan_huyen', 'phuong_xa', 'mac_dinh']
        widgets = {
            'ten_nguoi_nhan': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tên người nhận'}),
            'so_dien_thoai': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Số điện thoại'}),
            'dia_chi_chi_tiet': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ngõ 69B, đường 169 Nguyễn Trãi'}),
            'quan_huyen': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Quận/Huyện'}),
            'phuong_xa': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phường/Xã'}),
            'tinh_thanh': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Thành Phố/Tỉnh'}),
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Mật khẩu hiện tại"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'auto-focus':True, 'class':'form-control', 'placeholder':'Nhập mật khẩu hiện tại'}))
    new_password1 = forms.CharField(label=_("Mật khẩu mới"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Nhập mật khẩu mới'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Xác nhận mật khẩu mới"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Nhập lại mật khẩu mới'}))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("Mật khẩu mới"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Xác nhận mật khậu"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class CommentForm(forms.ModelForm):
    content = forms.CharField(label=_("Đánh giá sản phẩm"),widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'bình luận ở đây ...',
        'rows': '4',
    }))

    class Meta:
        model = DanhGia
        fields = ['content']
        
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ['user']

class RatingForm(forms.ModelForm):
    review_text = forms.CharField(label=_("Đánh giá sản phẩm"),widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'đánh giá ở đây ...',
        'rows': '4',
    }))
    class Meta:
        model = DanhGia
        fields=('review_text','so_sao')
   