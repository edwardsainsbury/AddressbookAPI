from django.conf.urls import url
from AddressBook import views


urlpatterns = [
    url(r'^AddressBook/?$', views.AddressbookList.as_view(), name='addressbooks'),
    url(r'^AddressBook/(?P<pk>[0-9]+)/?$', views.ContactList.as_view(), name='contact-list'),
    url(r'^AddressBook/(?P<addressbook_pk>[0-9]+)/(?P<contact_pk>[0-9]+)/?$', views.ContactDetail.as_view(),
        name='contact-detail'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
