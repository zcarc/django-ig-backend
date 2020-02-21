from django.contrib import admin
from .models import Profile, Follow

# Register your models here.

# 팔로우 내용을 표 형식으로 확인합니다.
class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user'


# 데코레이트 라는 기법
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # 여기는 이미 정해진 옵션 값들이 있습니다. (admin action 장고 문서를 참고하시면 됩니다.)
    # id는 장고에서 생성해줍니다.
    list_display = ['id', 'nickname', 'user']
    list_display_links = ['nickname', 'user']
    search_fields = ['nickname']
    inlines = [FollowInline,]

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at']
    list_display_links = ['from_user', 'to_user', 'created_at']
