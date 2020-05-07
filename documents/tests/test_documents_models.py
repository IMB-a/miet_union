import pytest

from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels():

    def test_help_for_proforg_have_first_name(self):
        help_for_proforg = mixer.blend(
            'documents.HelpForProforg',
            title='test_title',
            file=None,
        )
        assert help_for_proforg
        assert help_for_proforg.__str__()

    def test_help_for_student_proforg_have_first_name(self):
        help_for_student_proforg = mixer.blend(
            'documents.HelpForStudentProforg',
            title='test_title',
            file=None,
        )
        assert help_for_student_proforg
        assert help_for_student_proforg.__str__()

    def test_the_main_activities_of_proforg_have_first_name(self):
        the_main_activities_of_proforg = mixer.blend(
            'documents.TheMainActivitiesOfProforg',
            title='test_title',
            file=None,
        )
        assert the_main_activities_of_proforg
        assert the_main_activities_of_proforg.__str__()

    def test_normative_documents_have_first_name(self):
        normative_documents = mixer.blend(
            'documents.NormativeDocuments',
            title='test_title',
            file=None,
        )
        assert normative_documents
        assert normative_documents.__str__()

    def test_useful_links_have_first_name(self):
        useful_links = mixer.blend(
            'documents.UsefulLinks',
            title='test_title',
            file=None,
        )
        assert useful_links
        assert useful_links.__str__()

    def test_commissions_of_profcom_have_first_name(self):
        commissions_of_profcom = mixer.blend(
            'documents.CommissionsOfProfcom',
            title='test_title',
            file=None,
        )
        assert commissions_of_profcom
        assert commissions_of_profcom.__str__()
