"""
..  module:: url_replace
    :synopsis: Adds page number as field in query string rather than replacing it

..  moduleauthor:: see https://gist.github.com/sumitlni/4f308e5999d2d4d8cb284fea7bf0309c
"""

from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """Replace query string with addition of parameter

    :param request: request object
    :param field: field to add, such as 'page'
    :param value: value to add with field, such as integer page number
    :return: new query string
    """
    query_string = request.GET.copy()
    query_string[field] = value

    return query_string.urlencode()