from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if User.objects.filter(pk=request.user.id, groups__name='moderator').exists():
            return True
        else:
            return False