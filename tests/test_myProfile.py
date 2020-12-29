import datetime
from http import HTTPStatus
import pytest
import re
import secrets

from StoreMeApp.store_me import models


HOME_PAGE = ['/', '/home']
SIGNIN_PAGE = '/signIn'
MYFROFILE_PAGE = '/MyProfile'
SIGNOUT_PAGE = '/signOut'
VALIDATION_MESSAGES = {
    'empty_required_field': b'This field is required',
    'success_signIn': b'Sign in successful',
    'success_update_profile': b'Your acount has been updated'
}


class TestMyProfile:
    
    @staticmethod
    def get_signIn_form_data(email, password='The_Best_Pass'):
        return {
            'email': email,
            'password': password,
            'submit': 'Sign In'
        }

    @staticmethod
    def test_my_profile_returns_ok(client, user):
        data = TestMyProfile.get_signIn_form_data(user.email)
        client.post(SIGNIN_PAGE, data=data)
        response = client.get(MYFROFILE_PAGE,follow_redirects=True)
        assert response.status_code == HTTPStatus.OK
    
    @staticmethod
    def is_user_in_myprofile(user, response_data):
        return (user.firstname in response_data
                and user.lastname in response_data
                and user.username in response_data
                and user.email in response_data
                and user.birthday.strftime("%Y-%m-%d") in response_data)

    @staticmethod
    def test_my_profile_user_details_in_my_profile(client, user):
        data = TestMyProfile.get_signIn_form_data(user.email)
        client.post(SIGNIN_PAGE, data=data)
        response = client.get(MYFROFILE_PAGE, follow_redirects=True)
        print(response.data)
        assert TestMyProfile.is_user_in_myprofile(user, str(response.data))
    
    @staticmethod
    def test_my_profile_update_my_profile(client, user):
        data = TestMyProfile.get_signIn_form_data(user.email)
        client.post(SIGNIN_PAGE, data=data)
        client.get(MYFROFILE_PAGE)
        password_appendix = secrets.token_hex(2)
        new_user = models.Users(
            firstname=f'{secrets.token_hex(8)}',
            lastname=f'{secrets.token_hex(8)}',
            username=user.username,
            email=user.email,
            password=f'The_Best_Pass{password_appendix}',
            birthday=datetime.date(2007, 5, 26)
        )
        update_user_form = {
            'firstname': str(new_user.firstname),
            'lastname': str(new_user.lastname),
            # 'username': new_user.username,
            # 'email': new_user.username,
            'password': str(new_user.password),
            'confirm_password': str(new_user.password),
            'birthday': new_user.birthday,
            'save': 'Save'
        }
        response = client.post(MYFROFILE_PAGE, data=update_user_form, follow_redirects=True)
        assert (TestMyProfile.is_user_in_myprofile(new_user, str(response.data))
                and len(re.findall(VALIDATION_MESSAGES['success_update_profile'], response.data)) == 1)
        client.get(SIGNOUT_PAGE, follow_redirects=True)
        client.get(SIGNIN_PAGE, follow_redirects=True)
        response2 = client.post(SIGNIN_PAGE,
                                data=TestMyProfile.get_signIn_form_data(
                                    new_user.email,
                                    update_user_form['password']),
                                follow_redirects=True)
        print(update_user_form['password'])
        print(response2.data)
        assert (len(re.findall(VALIDATION_MESSAGES['success_signIn'], response2.data)) == 1
                and bytes(user.username, encoding='utf-8') in response.data
                and response.status_code == HTTPStatus.OK)
