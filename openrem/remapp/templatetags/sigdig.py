# This Python file uses the following encoding: utf-8

from django import template
from decimal import Decimal
import math

register = template.Library()


@register.filter
def sigdig(value, digits=3):
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
