from django import template
from django.template.defaultfilters import stringfilter
from django.core.files import File

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by the given delimiter and return a list."""
    return value.split(delimiter)

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using the given key."""
    return dictionary.get(key)

@register.filter
def getattr(obj, attr):
    """Filtre personnalisé pour accéder aux attributs d'un objet dans un template"""
    try:
        return getattr(obj, attr)
    except AttributeError:
        return None

@register.filter
def get_field(obj, field_name):
    """Get a field value from an object."""
    try:
        # Try to get the attribute directly
        value = getattr(obj, field_name)
        # If it's a callable (method), call it
        if callable(value):
            value = value()
        return value
    except (AttributeError, TypeError):
        return ''

@register.filter
def is_file(value):
    """Check if the value is a File object."""
    return isinstance(value, File) or (hasattr(value, 'url') and hasattr(value, 'name')) 