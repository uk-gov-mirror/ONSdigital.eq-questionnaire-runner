import time
from uuid import uuid4

from sdc.crypto.encrypter import encrypt

from app.keys import KEY_PURPOSE_AUTHENTICATION

PAYLOAD = {
    'user_id': 'integration-test',
    'period_str': 'April 2016',
    'period_id': '201604',
    'collection_exercise_sid': '789',
    'ru_ref': '123456789012A',
    'ru_name': 'Integration Testing',
    'ref_p_start_date': '2016-04-01',
    'ref_p_end_date': '2016-04-30',
    'return_by': '2016-05-06',
    'trad_as': 'Integration Tests',
    'employment_date': '1983-06-02',
    'region_code': 'GB-ENG',
    'language_code': 'en',
    'roles': [],
}


class TokenGenerator:

    def __init__(self, key_store, upstream_kid, sr_public_kid):
        self._key_store = key_store
        self._upstream_kid = upstream_kid
        self._sr_public_kid = sr_public_kid

    @staticmethod
    def _get_payload_with_params(form_type_id, eq_id, survey_url=None, **extra_payload):
        payload_vars = PAYLOAD.copy()
        payload_vars['tx_id'] = str(uuid4())
        payload_vars['eq_id'] = eq_id
        payload_vars['form_type'] = form_type_id
        if survey_url:
            payload_vars['survey_url'] = survey_url

        payload_vars['iat'] = time.time()
        payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now
        payload_vars['jti'] = str(uuid4())

        for key, value in extra_payload.items():
            payload_vars[key] = value

        return payload_vars

    def create_token(self, form_type_id, eq_id, **extra_payload):
        payload_vars = self._get_payload_with_params(form_type_id, eq_id, None, **extra_payload)

        return self.generate_token(payload_vars)

    def create_token_without_jti(self, form_type_id, eq_id, **extra_payload):
        payload_vars = self._get_payload_with_params(form_type_id, eq_id, None, **extra_payload)
        del payload_vars['jti']

        return self.generate_token(payload_vars)

    def create_token_with_survey_url(self, form_type_id, eq_id, survey_url, **extra_payload):
        payload_vars = self._get_payload_with_params(form_type_id, eq_id, survey_url, **extra_payload)

        return self.generate_token(payload_vars)

    def generate_token(self, payload):
        return encrypt(payload, self._key_store, KEY_PURPOSE_AUTHENTICATION)
