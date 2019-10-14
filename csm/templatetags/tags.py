from django.template.defaultfilters import floatformat
from django.template import Library

register = Library()



@register.filter('formatted_float')
def formatted_float(value):
    value = floatformat(value, arg=4)
    return str(value).replace(',','.')

@register.filter('get_main_image')
def get_main_image(value):
    return value.name.split('/')[-1]