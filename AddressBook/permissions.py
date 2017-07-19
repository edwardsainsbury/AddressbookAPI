from rest_framework import permissions
from AddressBook.models import AddressBook


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # can write custom code
        if 'addressbook_pk' in view.kwargs:
            try:
                user_addressbook = AddressBook.objects.get(pk=view.kwargs['addressbook_pk']).owner
            except:
                return False
        else:
            try:
                user_addressbook = AddressBook.objects.get(pk=view.kwargs['pk']).owner
            except:
                return False

        if request.user == user_addressbook:
            return True
        return False
