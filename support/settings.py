from django.conf import settings

GET_CREATE_LOCATION_FUNCTION = getattr(settings, 'GET_CREATE_LOCATION_FUNCTION', None)

APP_NAME = getattr(settings, 'APP_NAME', 'Untitled')
COMPILE_CSS = getattr(settings, 'COMPILE_CSS', False)