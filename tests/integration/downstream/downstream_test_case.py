from tests.integration.integration_test_case import IntegrationTestCase

from app.submitter.submitter import SubmitterFactory, Submitter


class MyMockSubmitter(Submitter):
    def __init__(self):
        self._message = None
        self._submitted_at = None

    def send(self, message):
        self._message = message
        return True

    def encrypt_message(self, message):
        return message

    def get_message(self):
        return self._message


class DownstreamTestCase(IntegrationTestCase):
    '''
    Overrides the application SubmitterFactory to provide our own which
    allows the message to be captured and interrogated.
    '''
    _submitter = MyMockSubmitter()

    @staticmethod
    def get_submitter():
        return DownstreamTestCase._submitter

    def setUp(self):
        super().setUp()
        self._old_method = SubmitterFactory.get_submitter
        SubmitterFactory.get_submitter = DownstreamTestCase.get_submitter

    def tearDown(self):
        DownstreamTestCase._submitter._message = None
        SubmitterFactory.get_submitter = self._old_method
