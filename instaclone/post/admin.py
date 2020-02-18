from django.contrib import admin
from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 여기는 이미 정해진 옵션 값들이 있습니다. (admin action 장고 문서를 참고하시면 됩니다.)
    # id는 장고에서 생성해줍니다.
    list_display = ['id', 'author', 'nickname', 'content', 'created_at']
    list_display_links = ['author', 'nickname', 'content']
    form = PostForm

    # nickname이 Post 테이블에 없어서 정의해줍니다.
    def nickname(request, post):
        return post.author.profile.nickname