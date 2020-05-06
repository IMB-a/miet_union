from django.urls import reverse, resolve


class TestUrls:

    def test_login_page_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'
