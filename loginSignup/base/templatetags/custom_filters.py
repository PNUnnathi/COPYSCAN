# custom_filters.py
from django import template

register = template.Library()

@register.filter
def starts_with_span(value):
    return value.startswith('<span')
