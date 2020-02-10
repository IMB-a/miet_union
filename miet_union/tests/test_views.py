import pytest

from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from miet_union.views import my_account
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        mixer.blend('miet_union.News')
        cls.factory = RequestFactory()

    def test_my_account_authenticated(self):
        path = reverse('my_account')
        request = self.factory.get(path)
        request.user = mixer.blend(User)

        response = my_account(request)
        assert response.status_code == 200

    def test_my_account_unauthenticated(self):
        path = reverse('my_account')
        request = self.factory.get(path)
        request.user = AnonymousUser()

        response = my_account(request)
        assert 'accounts/login' in response.url
