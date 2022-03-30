from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from user.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username,"username")
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            print("a")
            if user.is_staff:
                return user
        return None