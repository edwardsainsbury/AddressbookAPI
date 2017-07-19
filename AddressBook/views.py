from rest_framework import generics
from AddressBook.models import AddressBook, Contact
from AddressBook.serializers import AddressBookSerializer, ContactSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions, filters
from AddressBook.permissions import IsOwner


class AddressbookList(generics.ListCreateAPIView):
    # List all address books or create a new addressbook
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AddressBook.objects.all()
    serializer_class = AddressBookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactList(generics.ListCreateAPIView):
    # List all contacts in address book or create new contact
    permission_classes = (IsOwner,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', 'address', 'phone_number', 'email_address')

    def get_queryset(self):
        return Contact.objects.filter(addressbook=AddressBook.objects.filter(pk=self.kwargs.get('pk')))
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.save(addressbook=AddressBook.objects.filter(pk=self.kwargs.get('pk'))[0])


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):

    # Retrieve, update or delete an individual contact.
    lookup_url_kwarg = "contact_pk"
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Contact.objects.filter(addressbook=AddressBook.objects.filter(pk=self.kwargs.get('addressbook_pk')))\
         .filter(pk=self.kwargs.get('contact_pk'))

    serializer_class = ContactSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
