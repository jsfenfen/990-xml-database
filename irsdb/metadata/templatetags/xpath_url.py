from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def xpath_url(value):
    return "/metadata/xpath/" + value.replace("/","-") + ".html"

