from django.template import loader
from django import template

register = template.Library()

def select_template_from_string(arg):
    """
    Select a template from a string, which can include multiple
    template paths separated by commas.
    
    """
    if ',' in arg:
        tpl = loader.select_template(
            [tn.strip() for tn in arg.split(',')])
    else:
        tpl = loader.get_template(arg)
    return tpl

@register.filter
def render(form, template_name=None):
    tpl = select_template_from_string('support/forms/base.html')
    
    return tpl.render(template.Context({'form': form}))