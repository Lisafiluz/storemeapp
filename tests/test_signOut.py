from http import HTTPStatus
import pytest
import re
import secrets


SIGNOUT_PAGE = '/signOut'
SIGNIN_PAGE = '/signIn'
VALIDATION_MESSAGES = {
    'signed_out_message_success': b'You are succesfuly signed out',
    'signed_out_for_not_signed_in_message': b'You are not signed-in and can not signed-out'
}


class TestSignOut:

    @staticmethod
    def test_signOut_success(client, user):
        data = {
            'email': '_qa_catedor@storemeapp.com',
            'password': 'The_Best_Pass',
            'submit': 'submit'
        }
        client.post(SIGNIN_PAGE, data=data, follow_redirects=True)
        response = client.get(SIGNOUT_PAGE, follow_redirects=True)
        assert len(re.findall(VALIDATION_MESSAGES['signed_out_message_success'], response.data)) == 1
    
    @staticmethod
    def test_signOut_for_not_signed_in(client):
        response = client.get(SIGNOUT_PAGE, follow_redirects=True)
        assert len(re.findall(VALIDATION_MESSAGES['signed_out_for_not_signed_in_message'], response.data)) == 1
    