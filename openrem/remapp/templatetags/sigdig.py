# This Python file uses the following encoding: utf-8

"""
..  module:: sigdig
    :synopsis: template filter for returning number with three or specified number of significant digits

    Modified from Django Snippet at https://djangosnippets.org/snippets/1372/
"""

from django import template
from decimal import Decimal
import math

register = template.Library()


@register.filter
def sigdig(value, digits=3):
    """ Template filter to return number with specified number of significant figures

    :param value: number to consider
    :param digits: number of significant figures, default 3
    :return: number to specified number of significant figures
    """

    if value is None:
        return ''
    if value != Decimal(0):
        order = int(math.floor(math.log10(math.fabs(value))))
        places = digits - order - 1
    else:
        places = 2
    if places > 0:
        fmtstr = "%%.%df" % (places)
    else:
        fmtstr = "%.0f"
    return Decimal(fmtstr % (round(value, places)))
