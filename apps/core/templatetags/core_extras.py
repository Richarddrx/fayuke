from django import template

register = template.Library()

@register.filter
def dictkey(d, key):
    """Look up a dictionary key by variable value."""
    return d.get(key, '')
