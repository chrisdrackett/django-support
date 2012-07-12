from django.conf import settings

GET_CREATE_LOCATION_FUNCTION = getattr(settings, 'GET_CREATE_LOCATION_FUNCTION', None)

APP_NAME = getattr(settings, 'APP_NAME', 'Untitled')
COMPILE_MEDIA = getattr(settings, 'COMPILE_MEDIA', False)