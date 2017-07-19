from rest_framework import status
from django.urls import reverse
from AddressBook.models import AddressBook
from django.contrib.auth.models import User
from AddressBook.serializers import AddressBookSerializer
from rest_framework.test import APITestCase


# Test can read addressbooks
class GetAllAddressbooks(APITestCase):

    def setUp(self):
        User.objects.create_user(username='ed', password='edpassword')
        self.client.login(username='ed', password='edpassword')

    def test_can_read_all_addressbooks(self):
        response = self.client.get(reverse('addressbooks'))
        addressbooks = AddressBook.objects.all()
        serializer = AddressBookSerializer(addressbooks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Test can create read update and delete entries owner by authenticated user
class CRUDContactAuthorisedTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ed', password='edpassword')
        self.client.login(username='ed', password='edpassword')
        self.data = {'first_name': 'Ed', "last_name": 'Sainsbury', 'address': '123 New Street',
                     'phone_number': '0123456789', 'email_address': 'edwardsainsbury@test.com'}
        self.client.post(reverse('addressbooks'), {'contacts': []})

    def test_can_create_read_update_and_delete_contacts(self):
        # create
        response = self.client.post(reverse('contact-list', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # read
        response = self.client.get(reverse('contact-list', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # update
        self.data = {'first_name': 'Ed', "last_name": 'Sainsbury', 'address': '123 New Street',
                     'phone_number': '0123456789', 'email_address': 'edwardsainsbury@test.com'}
        response = self.client.put(reverse('contact-detail', args=[self.user.id, 1]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # delete
        response = self.client.delete(reverse('contact-detail', args=[self.user.id, 1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Test can only perform operations on addressbook or entries that user owns
class CRUDContactUnauthorisedTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ed', password='edpassword')
        self.client.login(username='ed', password='edpassword')
        self.data = {'first_name': 'Ed', "last_name": 'Sainsbury', 'phone_number': '0123456789',
                     'email_address': 'edwardsainsbury@test.com'}
        self.client.post(reverse('addressbooks'), {'contacts': []})
        self.client.logout()
        self.userTwo = self.user = User.objects.create_user(username='john', password='johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_cant_create_cread_update_and_delete_contacts(self):
        # create
        response = self.client.post(reverse('contact-list', args=[self.user.id]), self.data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        # read
        response = self.client.get(reverse('contact-list', args=[self.user.id]))
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        # update
        self.data = {'first_name': 'Ed', "last_name": 'Sainsbury', 'address': '123 New Street',
                     'phone_number': '0123456789', 'email_address': 'edwardsainsbury@test.com'}
        response = self.client.put(reverse('contact-detail', args=[self.user.id, 1]), self.data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        # delete
        response = self.client.delete(reverse('contact-detail', args=[self.user.id, 1]))
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Test can perform searches by name, address, mobile number or email address
class SearchTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ed', password='edpassword')
        self.client.login(username='ed', password='edpassword')
        self.data = {'first_name': 'Ed', "last_name": 'Sainsbury', 'address': '123 New Street',
                     'phone_number': '0123456789', 'email_address': 'edwardsainsbury@test.com'}
        self.client.post(reverse('addressbooks'), {'contacts': []})
        response = self.client.post(reverse('contact-list', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_serch_by_first_name(self):
        # Check no contacts returned when false search is made
        response = self.client.get(reverse('contact-list', args=[self.user.id])+'?search=consuela')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        response = self.client.get(reverse('contact-list', args=[self.user.id]) + '?search=ed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data), 0)

    def test_serch_by_last_name(self):
        response = self.client.get(reverse('contact-list', args=[self.user.id])+'?search=sainsbury')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serch_by_phone_number(self):
        response = self.client.get(reverse('contact-list', args=[self.user.id])+'?search=0123456789')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serch_by_email_address(self):
        response = self.client.get(reverse('contact-list', args=[self.user.id]) + '?search=edwardsainsbury@test.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Test cant have more than one addresbook per user
class SingularAddressbookTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ed', password='edpassword')
        self.client.login(username='ed', password='edpassword')
        self.data = {'first_name': 'Ed', "last_name": 'Sainsbury', 'address': '123 New Street',
                     'phone_number': '0123456789', 'email_address': 'edwardsainsbury@test.com'}
        self.client.post(reverse('addressbooks'), {'contacts': []})

    def test_cannot_create_multiple_addressbooks(self):
        response = self.client.post(reverse('addressbooks'), {'contacts': []})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
