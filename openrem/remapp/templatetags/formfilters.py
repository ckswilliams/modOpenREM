from django import template
register = template.Library()


def label_with_classes(value, arg):

    return value.label_tag(attrs={'class': arg})

register.filter('label_with_classes',label_with_classes)