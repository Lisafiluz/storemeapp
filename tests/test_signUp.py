from copy import deepcopy
import datetime
import re
import secrets

import pytest

from StoreMeApp.store_me import models


def get_dict_without_key(SIGNUP_DETAILS, k):
    copy_d = deepcopy(SIGNUP_DETAILS)
    copy_d[k] = ''
    return copy_d


SIGNUP_PAGE = '/signUp'

VALIDATION_MESSAGES = {
    'empty_required_field': b'This field is required',
    'invalid_name_field': b'Field must be between 2 and 20 characters long',
    'invalid_email': b'Invalid email address',
    'invalid_password': b'Field must be between 6 and 20 characters long',
    'unmatch_passwords': b'Field must be equal to password',
    'invalid_birthday': b'A birthday cannot be in the future',
    'username_is_alredy_exist': b'That username is already exist',
    'email_is_alredy_exist': b'That email is already exist',
    'success_signUp': b'Your acount has been created!',
    'required_page': b'Please log in to access this page'
}

SIGNUP_DETAILS = {
    'firstname': '_qa_catedor',
    'lastname': '_qa_catedor',
    'username': str(secrets.token_hex(8)),
    'email': '_qa_catedor@' + str(secrets.token_hex(8)) + '.com',
    'password': '123456',
    'confirm_password': '123456',
    'birthday': datetime.date(1997, 5, 26)
}
POSSIBLE_SIGNUP_OPTIONS = [get_dict_without_key(SIGNUP_DETAILS, k)
                            for k, v in SIGNUP_DETAILS.items()]


class TestSignUp:

    @staticmethod
    @pytest.mark.parametrize('form_details', POSSIBLE_SIGNUP_OPTIONS)
    def test_signUp_one_detail_missing(client, form_details):
        # Checks that the 'empty_required_field' msg apeears only once
        form_details['submit'] = 'submit'  # for post on the relevant form
        response = client.post(SIGNUP_PAGE, data=form_details)
        assert len(re.findall(VALIDATION_MESSAGES['empty_required_field'], response.data)) == 1
    
    @staticmethod
    @pytest.mark.parametrize('field_to_check', ['firstname', 'lastname', 'username'])
    def test_signUp_invalid_name_fields(client, field_to_check):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data[field_to_check] = 'a'
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['invalid_name_field'], response.data)) == 1
        data[field_to_check] = 'a' * 21
        assert len(re.findall(VALIDATION_MESSAGES['invalid_name_field'], response.data)) == 1
    
    @staticmethod
    @pytest.mark.parametrize('invalid_email', ['aaaaaa', 'aaa@sss.com@', 'aaa.co.il'])
    def test_signUp_invalid_email(client, invalid_email):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data['email'] = invalid_email
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['invalid_email'], response.data)) == 1
    
    @staticmethod
    @pytest.mark.parametrize('invalid_password', ['aaaaa', 'a' * 21])
    def test_signUp_invalid_password(client, invalid_password):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data['password'] = invalid_password
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['invalid_password'], response.data)) == 1
    
    @staticmethod
    def test_signUp_unmatch_passwords(client):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data['confirm_password'] = secrets.token_hex(8)
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['unmatch_passwords'], response.data)) == 1
    
    @staticmethod
    def test_signUp_invalid_birthday(client):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data['birthday'] = datetime.date.today() + datetime.timedelta(days=1)
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['invalid_birthday'], response.data)) == 1

    @staticmethod
    def test_signUp_username_is_exist(client, user):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data['username'] = user.username
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['username_is_alredy_exist'], response.data)) == 1
    
    @staticmethod
    def test_signUp_email_is_exist(client, user):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        data['email'] = user.email
        response = client.post(SIGNUP_PAGE, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['email_is_alredy_exist'], response.data)) == 1

    @staticmethod
    def test_signUp_success(client):
        data = deepcopy(SIGNUP_DETAILS)
        data['submit'] = 'submit'
        response = client.post(SIGNUP_PAGE, data=data, follow_redirects=True)
        assert len(re.findall(VALIDATION_MESSAGES['success_signUp'], response.data)) == 1
        models.Users.delete_user(data['username'])
