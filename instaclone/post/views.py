from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment, Tag
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json # 이 부분을 불러오지 않으면 ajax 통신에서 error가 발생합니다.
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count


# Create your views here.

# 카운트를 검색할 때 태그를 통해서 검색할 수 있습니다.
# 태그를 처음에는 없음으로 설정해줘야 포스트들이 문제없이 뜹니다.
def post_list(request, tag=None):

    print('views.py... tag: ', tag);

    # annotate : 엑셀에서 컬럼을 하나 더 추가한다고 보시면 됩니다.
    # -num_psot : '-'는 역순입니다.
    # Count(): 포스트의 레코드 수를 셉니다.
    tag_all = Tag.objects.annotate(num_post=Count('post')).order_by('-num_post')

    # 포스트에서 모든 내용을 불러옵니다.
    # tag_set__name__ : name을 foreign Key로 지정합니다.
    # iexact : 대소문자 구분없이 name으로 검색합니다.
    # prefetch_related() : 1:1, N:N 관계입니다.
    # select_related() : 1:1 관계에서만 사용합니다.
    # select_related('author__profile') 에서 한번 불러와서
    # prefetch_related() 에서 author__profile 를 한번 더 줄일 수 있습니다.
    if tag:
        post_list = Post.objects.filter(tag_set__name__iexact=tag) \
            .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                              'author__profile__follower_user', 'author__profile__follower_user__from_user') \
            .select_related('author__profile')
    else:
        post_list = Post.objects.all() \
            .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                              'author__profile__follower_user', 'author__profile__follower_user__from_user') \
            .select_related('author__profile')




    # 3개씩 Paginator에 넣습니다.
    paginator = Paginator(post_list, 3)
    page_num = request.POST.get('page')

    # 예외 상황에 서버가 종료되지 않게해줍니다.
    # 1. 페이지가 integer가 아니라면 페이지를 '1'로 바꿉니다.
    # 2. 최대 페이지 수를 넘어서면 마지막 페이지를 보여줍니다.
    try:
        posts = paginator.page(page_num)

    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    comment_form = CommentForm()


    # post_list.html에서 ajax 요청이 들어왔다면
    if request.is_ajax():
        return render(request, 'post/post_list_ajax.html', {
            'posts': posts,
            'comment_form': comment_form,
        })


    if request.method == 'POST':
        # isalnum() : 문자인지 숫자인지 확인합니다.
        tag = request.POST.get('tag')
        tag_clean = ''.join(e for e in tag if e.isalnum())

        return redirect('post:post_search', tag_clean)

    # 사용자가 로그인 했는지 체크합니다.
    # 로그인이 되어있다면
    if request.user.is_authenticated:

        username = request.user

        # get_user_model(): 유저 모델을 가져옵니다.
        # username=username: 유저 네임과 같은지 확인합니다.
        user = get_object_or_404(get_user_model(), username=username)

        user_profile = user.profile

        # 팔로잉한 사람들을 찾습니다.
        following_set = request.user.profile.get_following

        # 포스트에서 팔로잉한 사람들이 있는것만 가져옵니다.
        following_post_list = Post.objects.filter(author__profile__in=following_set)


        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': posts,
            'comment_form': comment_form,
            'following_post_list': following_post_list,
            'tag': tag,
            'tag_all': tag_all,
        })

    # 로그인이 안되어있다면
    else:
        return render(request, 'post/post_list.html', {
            'posts': posts,
            'comment_form': comment_form,
            'tag': tag,
            'tag_all': tag_all,
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
            post.tag_save() # 포스트의 태그를 저장합니다.
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


@login_required # 로그인 되어있을 경우만 받습니다.
@require_POST # POST 방식으로만 내용을 받습니다.
# request에 ajax 통신으로 보낸 pk 값이 들어있습니다.
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)

    # like 중계 모델을 사용해서 사용자 끼리 일종의 스위치를 만드는 것입니다.
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    # like가 만들어지지 않은 상태라면
    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
               'message:': message}

    return HttpResponse(json.dumps(context), content_type="application/json")


def post_bookmark(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)

    # like 중계 모델을 사용해서 사용자 끼리 일종의 스위치를 만드는 것입니다.
    post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(user=request.user)

    # like가 만들어지지 않은 상태라면
    if not post_bookmark_created:
        post_bookmark.delete()
        message = "북마크 취소"
    else:
        message = "북마크"

    context = {'bookmark_count': post.bookmark_count,
               'message:': message}

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            return render(request, 'post/comment_new_ajax.html', {
                'comment': comment,
            })

    return redirect('post:post_list')


@login_required
def comment_delete(request):
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1

    else:
        message = '잘못된 접근입니다.'
        status = 0

    return HttpResponse(json.dumps({'message': message, 'status': status}),
                        content_type='application/json')
