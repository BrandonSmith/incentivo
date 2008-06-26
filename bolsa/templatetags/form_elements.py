from django.template import Library

register = Library()

def extract_errors(form, element):
    try:
        return form.errors[element]
    except KeyError:
        return None

@register.inclusion_tag('bolsa/templates/text_input.html')
def text_input(form, element, size=None):
    return {'element': form[element], 'errors': extract_errors(form, element), 'size': size}

@register.inclusion_tag('bolsa/templates/calendar_input.html')
def calendar_input(form, element, value):
    return {'element': form[element], 'errors': extract_errors(form, element), 'value': value}

@register.inclusion_tag('bolsa/templates/check_input.html')
def check_input(form, element):
    return {'element': form[element], 'errors': extract_errors(form, element)}

@register.inclusion_tag('bolsa/templates/disable_on_submit.html')
def disable_on_submit():
    return {}

