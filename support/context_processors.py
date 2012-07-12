from .settings import APP_NAME, COMPILE_MEDIA

def app_name(request):
    return {'APP_NAME': APP_NAME}

def compile_media(request):
    return {'COMPILE_MEDIA': COMPILE_MEDIA}