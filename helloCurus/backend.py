from django.conf import settings
from django.contrib.auth.hashers import check_password
from core.models import UserProfile, Manager, Employee

class CurusBackend:
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = Employee.objects.get(email=username)
        except Employee.DoesNotExist:
            try:
                user = Manager.objects.get(email=username)
            except Manager.DoesNotExist: 
                try:
                    return UserProfile.objects.get(email=username)
                except UserProfile.DoesNotExist:
                    return None
        return user if user.agency.enabled else None

    def get_user(self, user_id):
        try:
            user = Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            try:
                user = Manager.objects.get(pk=user_id)
            except Manager.DoesNotExist: 
                try:
                    return UserProfile.objects.get(pk=user_id)
                except UserProfile.DoesNotExist:
                    return None
        return user if user.agency.enabled else None
