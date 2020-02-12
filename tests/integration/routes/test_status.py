from newrelic import agent

from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestStatus(IntegrationTestCase):
    def setUp(self):
        settings.EQ_NEW_RELIC_ENABLED = True
        super().setUp()

    def test_status_page(self):
        self.get("/status")
        self.assertStatusOK()
        self.assertTrue("version" in self.getResponseData())
