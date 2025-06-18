from django import template

register = template.Library()

@register.filter(name='split')
def split_string(value, key):
    """
    Splits a string into a list using 'key' as the delimiter.
    """
    return value.split(key)