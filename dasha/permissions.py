from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        user = request.user
        if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False) or getattr(user, 'user_type', None) == 'admin':
            return True
        # Read-only methods are allowed for everyone
        if request.method in SAFE_METHODS:
            return True
        # Otherwise only the owner-related field can modify
        owner = getattr(obj, "owner", None) or getattr(obj, "shipper", None) or getattr(obj, "carrier", None)
        return owner == request.user
