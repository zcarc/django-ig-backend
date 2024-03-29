from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# 정규표현식을 사용합니다.
import re

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

    tag_set = models.ManyToManyField('Tag', blank=True)

    # 다대다 관계
    # like_user_set을 통해서 Post.like_set으로 접근이 가능합니다.
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='like_user_set',
                                           through='Like') # post.like_set 으로 접근가능해집니다.

    bookmark_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='bookmark_user_set',
                                           through='Bookmark') # post.bookmark_set 으로 접근가능해집니다.

    # auto_now_add 는 최초 생성할 때 사용합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    # update 될 때는 현재시간인 auto_now 를 사용합니다.
    updated_at = models.DateTimeField(auto_now=True)


    # 클래스 메타 태그를 사용해서 모델 전체의 옵션을 설정합니다.
    class Meta:
        # created_at 기준으로 정렬합니다.
        ordering = ['-created_at']


    def tag_save(self):
        # 매칭되는 모든 경우를 리턴합니다.
        tags = re.findall(r'#(\w+)\b', self.content)

        # 들어온 태그가 없다면면
        if not tags:
            return

        for t in tags:
            # 'name'에 새로운 'tag'가 추가되었을 때 't'를 'name'에 넣습니다.
            tag, tag_created = Tag.objects.get_or_create(name=t)

            # ManyToMany 필드에 인스턴스를 추가합니다.
            self.tag_set.add(tag)





    # 좋아요를 카운팅하는 함수
    @property
    def like_count(self):
        return self.like_user_set.count()

    @property
    def bookmark_count(self):
        return self.bookmark_user_set.count()


    # content를 외래키로 지정합니다.
    def __str__(self):
        return self.content


# Like와 Bookmark는 중계 모델입니다.
# Post에서 이것을 담아줄 필드가 필요합니다.

class Like(models.Model):
    # AUTH_USER_MODEL는 장고 기본 유저모델입니다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # user와 post는 unique한 관계를 갖게 됩니다.
        unique_together = (
            ('user', 'post')
        )

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content


# 중계 모델입니다.
class Tag(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name