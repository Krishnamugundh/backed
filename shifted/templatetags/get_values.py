from django import template

register = template.Library()
@register.filter
def dict_value(dictionary, key)->str:
    """Retrieve the value from a dictionary given a key."""
    value = dictionary.get(key, None)
    if value:
        return value[4:]  # Adjust the slicing as needed
    return "Unknown Disease"