from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

# Lấy User Model hiện tại (auth.User)
User = get_user_model()

# Định nghĩa Form đăng ký tùy chỉnh của bạn


class CustomUserCreationForm(UserCreationForm):
    # Thêm trường 'email' vào Form
    email = forms.EmailField(
        required=True,  # Bắt buộc phải nhập
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        # Kế thừa các trường username, password, password2 từ UserCreationForm
        model = User
        fields = ("username", "email") + UserCreationForm.Meta.fields[1:]
        # Kết quả: fields = ('username', 'email', 'password', 'password2')

    # Bạn có thể thêm các phương thức clean() nếu muốn xác thực email đặc biệt
