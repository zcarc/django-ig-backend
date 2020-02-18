from django.urls import path
from .views import *

app_name = 'accounts'

# 로그인 관련 기능들을 만듭니다.
# signup, login_check, logout 부분은 views.py 파일 안에 있는 함수들입니다.
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_check, name='login'),
    path('logout/', logout, name='logout'),
]