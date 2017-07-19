from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AddressBook(models.Model):
    owner = models.ForeignKey(User, related_name='addressbook', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return "%s's address book" % self.owner


class Contact(models.Model):
    addressbook = models.ForeignKey(AddressBook, related_name='contacts', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email_address = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name
