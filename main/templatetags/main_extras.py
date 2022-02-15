from django import template

register = template.Library()

@register.filter
def to_percentage(value, arg):
    return round(value * 100,arg)
    