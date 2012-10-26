from django.template import RequestContext
from django.shortcuts import render_to_response

def template(request, template_name, dictionary, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)

    return render_to_response(template_name, dictionary, *args, **kwargs)
