from http import HTTPStatus
import re
import secrets


SIGNIN_PAGE = '/signIn'
WRONG_USER = {
    'email': '_qa_catedor@' + str(secrets.token_hex(8)) + '.com',
    'password': str(secrets.token_hex(4)),
    'submit': 'submit'
}
VALIDATION_MESSAGES = {
    'empty_required_field': b'This field is required',
    'empty_password': b'This field is required',
    'invalid_email': b'Invalid email address',
    'invalid_password': b'Field must be between 6 and 20 characters long',
    'success_signIn': b'Sign in successful',
    'required_page': b'Please log in to access this page'
}


class TestSignIn:
    @staticmethod
    def get_signIn_form_data(email, password='The_Best_Pass'):
        return {
            'email': email,
            'password': password,
            'submit': 'Sign In'
        }

    @staticmethod
    def test_signIn_wrong_username_or_password(client):
        assert client.post(SIGNIN_PAGE, data=WRONG_USER).status_code == HTTPStatus.UNAUTHORIZED
    
    @staticmethod
    def test_signIn_empty_email(client):
        data = TestSignIn.get_signIn_form_data('', WRONG_USER['password'])
        response = client.post(SIGNIN_PAGE, data=data)
        assert (len(re.findall(VALIDATION_MESSAGES['empty_required_field'], response.data)) == 1
                and response.status_code == HTTPStatus.OK)
    
    @staticmethod
    def test_signIn_empty_password(client):
        data = TestSignIn.get_signIn_form_data(WRONG_USER['email'], '')
        response = client.post(SIGNIN_PAGE, data=data)
        assert (len(re.findall(VALIDATION_MESSAGES['empty_required_field'], response.data)) == 1
                and response.status_code == HTTPStatus.OK)
    
    @staticmethod
    def test_signIn_invalid_email(client):
        data = TestSignIn.get_signIn_form_data('_Qa_catedor', WRONG_USER['password'])
        response = client.post(SIGNIN_PAGE, data=data)
        print(data)
        print(response.data)
        assert (len(re.findall(VALIDATION_MESSAGES['invalid_email'], response.data)) == 1
                and response.status_code == HTTPStatus.OK)
    
    @staticmethod
    def test_signIn_invalid_password(client):
        data = TestSignIn.get_signIn_form_data(WRONG_USER['email'], '123')
        response = client.post(SIGNIN_PAGE, data=data)
        assert (len(re.findall(VALIDATION_MESSAGES['invalid_password'], response.data)) == 1
                and response.status_code == HTTPStatus.OK)

    @staticmethod
    def test_signIn_success(client, user):
        data = TestSignIn.get_signIn_form_data(user.email)
        response = client.post(SIGNIN_PAGE, data=data, follow_redirects=True)
        assert (len(re.findall(VALIDATION_MESSAGES['success_signIn'], response.data)) == 1
                and bytes(user.username, encoding='utf-8') in response.data
                and response.status_code == HTTPStatus.OK)
    
    @staticmethod
    def test_signIn_case_sensetive_success(client, user):
        data = TestSignIn.get_signIn_form_data(user.email.upper())
        response = client.post(SIGNIN_PAGE, data=data, follow_redirects=True)
        assert (len(re.findall(VALIDATION_MESSAGES['success_signIn'], response.data)) == 1
                and bytes(user.username, encoding='utf-8') in response.data
                and response.status_code == HTTPStatus.OK)