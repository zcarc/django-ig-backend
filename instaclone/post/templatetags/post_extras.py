from django import template
import re

# 태그 라이브러리를 만들기 위한 모듈 레벨의 인스턴스 객체입니다.
register = template.Libarary()

@register.filter
def add_link(value):

    content = value.content

    # tag_set: models.py의 Post의 변수입니다.
    tags = value.tag_set.all()

    for tag in tags:

        # content의 내용을 pattern으로 검사하고 repl로 치환합니다.
        # content = re.sub(pattern, repl, content)
        content = re.sub(r'\#' + tag.name + r'\b',
                         '<a href="/post/explore/tags/' + tag.name + '">#' + tag.name + '</a>',
                         content)

    return content