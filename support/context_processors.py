from .settings import APP_NAME, COMPILE_CSS

def app_name(request):
    return {'APP_NAME': APP_NAME}

def COMPILE_CSS(request):
    return {'COMPILE_CSS': COMPILE_CSS}