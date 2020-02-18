
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request):

    # 포스트에서 모든 내용을 불러옵니다.
    post_list = Post.objects.all()

    # 사용자가 로그인 했는지 체크합니다.
    if request.user.is_authenticated:

        username = request.user

        # get_user_model(): 유저 모델을 가져옵니다.
        # username=username: 유저 네임과 같은지 확인합니다.
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile

        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': post_list,
        })

    # 로그인이 안되어있다면
    else:
        return render(request, 'post/post_list.html', {
            'posts': post_list,
        })