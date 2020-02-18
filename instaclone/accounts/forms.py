from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# User는 장고의 내장된 패키지입니다.
from django.contrib.auth.models import User

# 로그인 폼
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# 회원가입 폼
class SignupForm(UserCreationForm):
    # label: 라벨 tag에서 사용자명이라는 부분을 불러옵니다.
    # 사용자 이름과 비밀번호는 UserCreationForm 에서 자동으로 생성해줍니다.
    username = forms.CharField(label='사용자명', widget=forms.TextInput(attrs={
        'pattern': '[a-zA-Z0-9]+',
        'title': '특수문자, 공백 입력불가',
    }))

    nickname = forms.CharField(label='닉네임')
    picture = forms.ImageField(label='프로필 사진', required=False)

    # Meta 라는 부분은 데이터를 그대로 넘겨주는것으로 보시면 됩니다.
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    # 유효성 검사 (이미 존재하는 닉네임인지 확인)
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')

        # 받아온 닉네임이 있다면
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 존재하는 닉네임 입니다.')
        return nickname

    # 이메일 유효성 검사
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # 유저 모델을 통째로 가져와서 User에 담습니다.
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('사용중인 이메일 입니다.')

        # 문제가 없다면 이메일을 반환합니다.
        return email

    # 사진 유효성 검사
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')

        if not picture:
            picture = None

        return picture

    # 저장
    def save(self):
        user = super().save()

        # Profile에 내용을 생성합니다.
        # Profile: 유저의 모델을 받아서 커스텀하기 편하도록 생성한 모델입니다.
        # accounts/models.py에 정의되어 있습니다.
        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data['nickname'],
            picture=self.cleaned_data['picture'],
        )

        return user