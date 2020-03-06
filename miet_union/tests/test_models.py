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

    def test_commissions_of_profcom_have_first_name(self):
        commissions_of_profcom = mixer.blend(
            'miet_union.CommissionsOfProfcom',
            title='test_title',
            file=None,
        )
        assert commissions_of_profcom
        assert commissions_of_profcom.__str__()

    def test_email_subscription_have_first_name(self):
        email_subscription = mixer.blend(
            'miet_union.EmailSubscription',
            email='test@example.com',
            created=timezone.now,
        )
        assert email_subscription
        assert email_subscription.__str__()

    def test_help_for_proforg_have_first_name(self):
        help_for_proforg = mixer.blend(
            'miet_union.HelpForProforg',
            title='test_title',
            file=None,
        )
        assert help_for_proforg
        assert help_for_proforg.__str__()

    def test_help_for_student_proforg_have_first_name(self):
        help_for_student_proforg = mixer.blend(
            'miet_union.HelpForStudentProforg',
            title='test_title',
            file=None,
        )
        assert help_for_student_proforg
        assert help_for_student_proforg.__str__()

    def test_the_main_activities_of_proforg_have_first_name(self):
        the_main_activities_of_proforg = mixer.blend(
            'miet_union.TheMainActivitiesOfProforg',
            title='test_title',
            file=None,
        )
        assert the_main_activities_of_proforg
        assert the_main_activities_of_proforg.__str__()

    def test_normative_documents_have_first_name(self):
        normative_documents = mixer.blend(
            'miet_union.NormativeDocuments',
            title='test_title',
            file=None,
        )
        assert normative_documents
        assert normative_documents.__str__()

    def test_useful_links_have_first_name(self):
        useful_links = mixer.blend(
            'miet_union.UsefulLinks',
            title='test_title',
            file=None,
        )
        assert useful_links
        assert useful_links.__str__()
