from django.urls import path
from .views import *

app_name = 'accounts'

# 로그인 관련 기능들을 만듭니다.
# signup, login_check, logout 부분은 views.py 파일 안에 있는 함수들입니다.
# signup 으로 들어오게 된다면 두번째 인자인 signup 함수가 실행됩니다.
# name='signup': url의 이름은 'signup'으로 설정합니다.
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_check, name='login'),
    path('logout/', logout, name='logout'),
]