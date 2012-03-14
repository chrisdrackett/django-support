from django.utils.importlib import import_module

def function_from_string(string):
    module, func = string.rsplit(".", 1)
    m = import_module(module)
    
    return getattr(m, func)