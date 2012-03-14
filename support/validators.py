from django.contrib.auth.models import User

def validate_unique_email(value):
    if User.objects.filter(email=value.lower()).exists():
        return False
    return True

def validate_unique_username(value):
    if User.objects.filter(username=value.lower()).exists():
        return False
    return True
