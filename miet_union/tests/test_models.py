import pytest

from django.utils import timezone
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:

    def test_news_have_title(self):
        news = mixer.blend('news.News',
                           title='test_title',
                           main_text='test_main_text',
                           image=None,
                           created=timezone.now,
                           )
        assert news
        assert news.__str__()

    def test_worket_have_first_name(self):
        worker = mixer.blend('miet_union.Worker',
                             first_name='test_title',
                             )
        assert worker
        assert worker.__str__()
