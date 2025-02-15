from django import template
register = template.Library()

@register.filter
def get(dictionary, key):
    """Custom filter to retrieve dictionary values safely in templates"""
    return dictionary.get(key, None)