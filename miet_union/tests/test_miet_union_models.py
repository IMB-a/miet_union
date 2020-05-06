import pytest

from django.utils import timezone
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:

    def test_news_have_title(self):
        news = mixer.blend('miet_union.News',
                           title='test_title',
                           main_text='test_main_text',
                           image=None,
                           created=timezone.now,
                           )
        assert news
        assert news.__str__()

    def test_search_news(self):
        news = mixer.blend('miet_union.News',
                           title='test title',
                           main_text='test main text',
                           image=None,
                           created=timezone.now,
                           )
        assert news.search_news('test')

    def test_worker_have_first_name(self):
        worker = mixer.blend('miet_union.Worker',
                             first_name='test_title',
                             )
        assert worker
        assert worker.__str__()

    def test_email_subscription_have_first_name(self):
        email_subscription = mixer.blend(
            'miet_union.EmailSubscription',
            email='test@example.com',
            created=timezone.now,
        )
        assert email_subscription
        assert email_subscription.__str__()
