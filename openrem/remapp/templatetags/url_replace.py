from django import template

register = template.Library()


# From https://gist.github.com/sumitlni/4f308e5999d2d4d8cb284fea7bf0309c
@register.simple_tag
def url_replace(request, field, value):
    query_string = request.GET.copy()
    query_string[field] = value

    return query_string.urlencode()