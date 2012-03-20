from .settings import APP_NAME

def app_name(request):
    return {'APP_NAME': APP_NAME}