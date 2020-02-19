from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required


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


# 데코레이트 문법
# 로그인이 되어있을 경우에만 함수가 실행됩니다.

# 게시글 작성
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False로 중복 DB 저장을 방지합니다.
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # post.tag_save()
            messages.info(request, '새 글이 등록되었습니다.')
            return redirect('post:post_list')

    else:
        form = PostForm()
    return render(request, 'post/post_new.html', {
        'form': form,
    })


# 게시글 수정
@login_required
def post_edit(request, pk):
    # 객체가 있는지 확인 없다면 404 반환
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            # post.tag_set.clear()
            # post.tag_save()
            messages.success(request, '수정완료')
            return redirect('post:post_list')

    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {
        'post': post,
        'form': form,
    })


# 게시글 삭제
@login_required
def post_delete(request, pk):
    # 객체가 있는지 확인 없다면 404 반환
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or request.method == 'GET':
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')

    if request.method == 'POST':
        post.delete()
        messages.success(request, '삭제완료')
        return redirect('post:post_list')
