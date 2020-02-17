from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# instance: photo의 모델
# filename: 사용자가 업로드한 파일이름
def user_path(instance, filename):
    from random import choice  # 난수를 생성
    import string  # 대소문자를 다 포함한 알파벳을 불러옵니다.
    arr = [choice(string.ascii_letters) for _ in range(8)]  # 대소문자 관계없이 문자열을 불러옵니다. 0부터 8까지
    pid = ''.join(arr)  # 알파벳을 하나하나 이어 붙입니다.
    extension = filename.split('.')[-1]  # 파일이름을 . 기준으로 분리하고 맨 마지막 값을 가져옵니다. (확장자만 불러옵니다.)
    return 'accounts/{}/{}.{}'.format(instance.user.username, pid, extension)  # 폴더를 만들고 파일로 저장합니다.


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField('별명', max_length=20, unique=True)

    # 저장위치와와 처리과정을 설정하는게 update_to=user_path 라는 함수입니다.
    about = models.CharField(max_length=300, blank=True)

    picture = ProcessedImageField(upload_to=user_path,
                                  processors=[ResizeToFill(150, 150)],  # 이미지 사이즈 설정
                                  format='JPEG',
                                  options={'quality': 90},
                                  blank=True)

    GENDER_C = (
        ('선택안함', '선택안함'),
        ('여성', '여성'),
        ('남성', '남성'),
    )

    gender = models.CharField('성별(선택사항)',
                              max_length=10,
                              choices=GENDER_C,
                              default='N')


# 외래키 설정
def __str__(self):
    return self.nickname
