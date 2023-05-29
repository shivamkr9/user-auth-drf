from rest_framework.permissions import BasePermission


class IsEmployeeUser(BasePermission):
    """
    Allows access only to authenticated users if it is Employee.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee)


class IsDistributerUser(BasePermission):
    """
    Allows access only to authenticated users if it is Distributer.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_distributer)


class IsDeliveryPartnerUser(BasePermission):
    """
    Allows access only to authenticated users if it is Delivery Partner.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_delivery_partner)
