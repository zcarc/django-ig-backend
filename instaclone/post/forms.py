from django import forms

# 모델과 통신을 해야 값을 넣어줄 수 있습니다.
from .models import Post


# 글작성 폼
class PostForm(forms.ModelForm):
    photo = forms.ImageField(label='', required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'post-new-content',
        'rows': 5,
        'cols': 50,
        'placeholder': '140자 까지 등록 가능합니다.'
    }))

    # Meta 라는 부분은 데이터를 그대로 넘겨주는것으로 보시면 됩니다.
    class Meta:
        model = Post
        fields = ['photo', 'content']
