from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

def photo_path(instance, filename):
    from random import choice
    from time import strftime
    import string  # 대소문자를 다 포함한 알파벳을 불러옵니다.

    arr = [choice(string.ascii_letters) for _ in range(8)]  # 대소문자 관계없이 문자열을 불러옵니다. 0부터 8까지
    pid = ''.join(arr)  # 알파벳을 하나하나 이어 붙입니다.
    extension = filename.split('.')[-1]  # 파일이름을 . 기준으로 분리하고 맨 마지막 값을 가져옵니다. (확장자만 불러옵니다.)
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension)  # 폴더를 만들고 파일로 저장합니다.

class Post(models.Model):
    # 유저 모델의 내용을 외래키로 받아오고 author에 저장합니다.
    # 유저 모델의 유저가 삭제되면 author도 삭제됩니다.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    photo = ProcessedImageField(upload_to=photo_path,
                                processors=[ResizeToFill(600, 600)],  # 이미지 사이즈 설정
                                format='JPEG',
                                options={'quality': 90})

    content = models.CharField(max_length=140, help_text="최대길이 140자 입력이 가능합니다.")

    # auto_now_add 는 최초 생성할 때 사용합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    # update 될 때는 현재시간인 auto_now 를 사용합니다.
    updated_at = models.DateTimeField(auto_now=True)


    # 클래스 메타 태그를 사용해서 모델 전체의 옵션을 설정합니다.
    class Meta:
        # created_at 기준으로 정렬합니다.
        ordering = ['-created_at']

    # content를 외래키로 지정합니다.
    def __str__(self):
        return self.content



