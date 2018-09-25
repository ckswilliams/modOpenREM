# This Python file uses the following encoding: utf-8

from openremproject.settings import VIRTUAL_DIRECTORY
from django import template
register = template.Library()


@register.assignment_tag
def get_virtual_directory(*args, **kwargs):
    return VIRTUAL_DIRECTORY
