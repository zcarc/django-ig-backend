from django import template
import re

# 태그 라이브러리를 만들기 위한 모듈 레벨의 인스턴스 객체입니다.
# register는 유효한 tag library를 만들기 위한 모듈 레벨의 인스턴스 객체입니다.
register = template.Library()


@register.filter
def add_link(value):
    print('value.tag_set: ', value.tag_set)

    # 전달된 value 객체의 content 멤버변수를 가져옵니다.
    content = value.content

    # tag_set: models.py의 Post의 변수입니다.
    # 전달된 value 객체의 tag_set 전체를 가져오는 queryset을 리턴합니다.
    tags = value.tag_set.all()

    # tags의 각각의 인스턴스를 (tag)를 순회하며, content 내에서 해당 문자열을 => 링크를 포함한 문자열로 replace 합니다.
    for tag in tags:
        # content의 내용을 pattern으로 검사하고 repl로 치환합니다.
        # content = re.sub(pattern, repl, content)
        content = re.sub(r'\#' + tag.name + r'\b',
                         '<a href="/post/explore/tags/' + tag.name + '">#' + tag.name + '</a>', content)

    # 원하는 문자열로 치환이 완료된 content를 리턴합니다.
    return content
