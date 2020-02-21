from django.contrib import admin
from django import forms

from .models import Post, Like, Bookmark, Comment, Tag

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'


# 표 형식으로 어드민 페이지 구성
class LikeInline(admin.TabularInline):
    model = Like

class CommentInline(admin.TabularInline):
    model = Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 여기는 이미 정해진 옵션 값들이 있습니다. (admin action 장고 문서를 참고하시면 됩니다.)
    # id는 장고에서 생성해줍니다.
    list_display = ['id', 'author', 'nickname', 'content', 'created_at']
    list_display_links = ['author', 'nickname', 'content']
    form = PostForm
    inlines = [LikeInline, CommentInline]

    # nickname이 Post 테이블에 없어서 정의해줍니다.
    def nickname(request, post):
        return post.author.profile.nickname


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_display_links = ['post', 'user']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_display_links = ['post', 'user']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content', 'author', 'created_at']
    list_display_links = ['post', 'content', 'author']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
