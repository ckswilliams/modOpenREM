# This Python file uses the following encoding: utf-8

from django import template

register = template.Library()


def naturalduration(seconds):
    if not seconds:
        return ''

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    hplural = ''
    mplural = ''
    splural = ''
    
    if not h == 1:
        hplural = u's'
    if not m == 1:
        mplural = u's'
    if not s == 1:
        splural = u's'


    if h:
        duration = u"{0:.0f} hour{1} and {2:.0f} minute{3}".format(h, hplural, m, mplural)
    elif m:
        duration = u"{0:.0f} minute{1} and {2:.0f} second{3}".format(m, mplural, s, splural)
    else:
        duration = u"{0:.1f} second{1}".format(s, splural)

    return duration


register.filter('naturalduration', naturalduration)
