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

    # follow 관계를 저장해주는 field를 만듭니다.
    # symmetrical: False, 대칭 관계를 False (한쪽만 follow 할 수도 있습니다.)
    follow_set = models.ManyToManyField('self',
                                        blank=True,
                                        through='Follow',
                                        symmetrical=False,
                                        )


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


    # following의 카운트와 사용자를 확인하는 부분입니다.
    # 나를 팔로우한 유저를 반복문으로
    # self : Profile 입니다.
    # follower_user : to_user의 follower_user 입니다.
    # 이 함수가 실행되면 모든 유저가 담겨서 반환됩니다.
    @property
    def get_follower(self):
        return [i.from_user for i in self.follower_user.all()]


    # 내가 팔로잉인 사람들을 확인할 수 있습니다.
    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()]


    # 나를 팔로워한 유저의 수를 확인합니다.
    @property
    def follower_count(self):
        return len(self.get_follower)


    # 내가 팔로잉한 사람들의 수를 확인합니다.
    @property
    def following_count(self):
        return len(self.get_following)


    # 나를 팔로워한 사람을 확인합니다.
    def is_follower(self, user):
        return user in self.get_follower


    # 내가 팔로잉한 사람을 확인합니다.
    def is_following(self, user):
        return user in self.get_following



class Follow(models.Model):
    from_user = models.ForeignKey(Profile, related_name='follow_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='follower_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # 인스턴스를 추적할 때 형식을 설정합니다.
    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)

    # follow 모델 전체의 규칙을 정해줍니다.
    # 아래의 두개를 유니크한 관계를 맺습니다.
    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )