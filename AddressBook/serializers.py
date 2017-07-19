from rest_framework import serializers
from AddressBook.models import AddressBook, Contact
from django.contrib.auth.models import User
from rest_framework import exceptions


class ContactSerializer(serializers.ModelSerializer):
    addressbook = serializers.ReadOnlyField(source='addressbook.id')

    class Meta:
        model = Contact
        fields = ['id', 'addressbook', 'first_name', 'last_name', 'address', 'phone_number', 'email_address']


class AddressBookSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AddressBook
        fields = ('id', 'owner', 'contacts')

    def create(self, validated_data):
        owner = validated_data.get('owner')
        # Validate requirement to allow only one addressbook per user
        if len(AddressBook.objects.filter(owner=owner)) > 0:
            raise exceptions.ValidationError('Cannot create more than one addressbook per user')
        contacts_data = validated_data.pop('contacts')
        addressbook = AddressBook.objects.create(**validated_data)
        for contact_data in contacts_data:
            Contact.objects.create(address_book=addressbook, **contact_data)
        return addressbook


class UserSerializer(serializers.ModelSerializer):
    addressbook = serializers.PrimaryKeyRelatedField(many=True, queryset=AddressBook.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'addressbook')
