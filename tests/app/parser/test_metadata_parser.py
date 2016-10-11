import unittest

from app.authentication.invalid_token_exception import InvalidTokenException
from app.parser.metadata_parser import MetadataParser, serialise_metadata, deserialise_metadata
from tests.app.framework.sr_unittest import SurveyRunnerTestCase

import dateutil.parser

class TestMetadataParser(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07",
            "tx_id": "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }
        with self.application.test_request_context():
            self.metadata = MetadataParser.parse(self.jwt)

    def test_transaction_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get("tx_id"), self.metadata['tx_id'])

    def test_form_type(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("form_type"), self.metadata['form_type'])

    def test_collection_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("collection_exercise_sid"), self.metadata['collection_exercise_sid'])

    def test_get_eq_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("eq_id"), self.metadata['eq_id'])

    def test_get_period_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("period_id"), self.metadata['period_id'])

    def test_get_period_str(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("period_str"), self.metadata['period_str'])

    def test_ref_p_start_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("ref_p_start_date"), self.metadata['ref_p_start_date'].strftime('%Y-%m-%d'))

    def test_ref_p_end_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("ref_p_end_date"), self.metadata['ref_p_end_date'].strftime('%Y-%m-%d'))

    def test_ru_ref(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get("ref_p_end_date"), self.metadata['ref_p_end_date'].strftime('%Y-%m-%d'))

    def test_is_valid(self):
        with self.application.test_request_context():
            self.assertTrue(MetadataParser.is_valid(self.jwt))

    def test_is_valid_fails_missing_user_id(self):
        jwt = {
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("user_id", reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("form_type", reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            "user_id": "1",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("form_type", reason)

    def test_is_valid_fails_missing_collection_exercise_sid(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("collection_exercise_sid", reason)

    def test_is_valid_fails_missing_eq_id(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("eq_id", reason)

    def test_is_valid_fails_missing_period_id(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("period_id", reason)

    def test_is_valid_fails_missing_period_str(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("period_str", reason)

    def test_is_valid_fails_missing_ref_p_start_date(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("ref_p_start_date", reason)

    def test_is_valid_fails_invalid_ref_p_start_date(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-13-31",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.parse(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_invalid_ref_p_end_date(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-12-31",
            "ref_p_end_date": "2016-04-31",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.parse(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_invalid_return_by(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-12-31",
            "ref_p_end_date": "2016-03-31",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-09-31"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.parse(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_missing_ref_p_end_date(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("ref_p_end_date", reason)

    def test_is_valid_fails_missing_ru_ref(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("ru_ref", reason)

    def test_is_valid_fails_missing_ru_name(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("ru_name", reason)

    def test_is_valid_fails_missing_return_by(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals("return_by", reason)

    def test_is_valid_does_not_fail_missing_optional_value_in_token(self):
        # tx_id, trad_as and employment_date are optional and might not be in the token
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)

    def test_invalid_tx_id(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07",
            # invalid
            "tx_id": "12121"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.parse(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_malformed_tx_id(self):
        jwt = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07",
            # one character short
            "tx_id": "83a3db82-bea7-403c-a411-6357ff70f2f"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.parse(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_serialise_metadata(self):
        metadata = MetadataParser.parse(self.jwt)
        serialised = serialise_metadata(metadata)

        expected = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02",
            "ref_p_end_date": "2016-03-03",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07",
            "tx_id": "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }

        self.assertEquals(expected, serialised)

    def test_deserialise_metadata(self):
        serialised = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": "2016-02-02T00:00:00",
            "ref_p_end_date": "2016-03-03T00:00:00",
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": "2016-07-07T00:00:00",
            "tx_id": "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f",
            "trad_as": None,
            "employment_date": None
        }

        expected = {
            "user_id": "1",
            "form_type": "a",
            "collection_exercise_sid": "test-sid",
            "eq_id": "2",
            "period_id": "3",
            "period_str": "2016-01-01",
            "ref_p_start_date": dateutil.parser.parse("2016-02-02T00:00:00"),
            "ref_p_end_date": dateutil.parser.parse("2016-03-03T00:00:00"),
            "ru_ref": "2016-04-04",
            "ru_name": "Apple",
            "return_by": dateutil.parser.parse("2016-07-07T00:00:00"),
            "tx_id": "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }

        deserialised = deserialise_metadata(serialised)

        self.assertEquals(expected, deserialised)

if __name__ == '__main__':
    unittest.main()
