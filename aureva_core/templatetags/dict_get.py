# So we can access dict keys by variable in templates, something that is maddeningly not a default behavior in templates

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='get')
def get(obj, key):
    return obj.get(key, '')
