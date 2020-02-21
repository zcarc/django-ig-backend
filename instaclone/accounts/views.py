# redirect: 로그인 후 페이지를 이동할 지 설정합니다.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm
from .models import Profile, Follow

import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

# 뷰는 함수 또는 클래스로 나뉘게 됩니다.
def signup(request):
    if request.method == 'POST':
        # 폼의 프로필 사진도 들어있습니다.
        form = SignupForm(request.POST, request.FILES)

        # 값이 있다면 폼의 내용을 저장합니다.
        if form.is_valid():
            user = form.save()
            # 회원가입이 성공적으로 되었을 경우 로그인 페이지로 이동합니다.
            return redirect('accounts:login')

    # 요청이 잘못 들어왔다면
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })


# 로그인 요청
def login_check(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        # input에서 받은 값을 실제 DB와 비교합니다.
        user = authenticate(username=name, password=pwd)

        # user가 실제 DB에 있다면
        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            return render(request, 'accounts/login_fail.html')

    # 로그인 요청이 잘못 들어왔다면 다시 로그인할 수 있도록 합니다.
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


# 로그아웃
def logout(request):
    django_logout(request)
    return redirect('/')


@login_required
@require_POST
def follow(request):
    from_user = request.user.profile
    pk = request.POST.get('pk')
    to_user = get_object_or_404(Profile, pk=pk)
    follow, created = Follow.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        message = '팔로우 시작'
        status = 1

    else:
        follow.delete()
        message = '팔로우 취소'
        status = 0

    context = {
        'message': message,
        'status': status,
    }

    return HttpResponse(json.dumps(context), content_type='application/json')
