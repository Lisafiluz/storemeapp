from http import HTTPStatus
import pytest
import re

from store_me import models


PAGES = ['/', '/home', '/signIn', '/signUp', f'/product/{models.Products.get_random_product_number()}']

SIGNIN_PAGE = '/signIn'

VALIDATION_MESSAGES = {
    'empty_required_field': b'This field is required',
    'required_page': b'Please log in to access this page',
    'aleady_signed_in': b'You are already signed In'
}

SIGNIN_REQUIRED_PAGES = [
    '/MyProfile'
]

FORBIDDEN_FOR_AUTHENTICATED_PAGES = [
    '/signIn',
    '/signUp'
]


class TestOverPages:

    @staticmethod
    @pytest.mark.parametrize('url', PAGES)
    def test_pages_returns_ok(client, url):
        assert client.get(url).status_code == HTTPStatus.OK

    @staticmethod
    @pytest.mark.parametrize('url', PAGES)
    def test_pages_search_empty_field(client, url):
        data = {
            'search_txt': '',
            'search': 'search'
        }
        response = client.post(url, data=data)
        assert len(re.findall(VALIDATION_MESSAGES['empty_required_field'], response.data)) == 1
    
    @staticmethod
    @pytest.mark.parametrize('url', SIGNIN_REQUIRED_PAGES)
    def test_signIn_required(client, url):
        # For all the pages that require to sign in first
        response = client.get(url, follow_redirects=True)
        assert len(re.findall(VALIDATION_MESSAGES['required_page'], response.data)) == 1
    
    @staticmethod
    @pytest.mark.parametrize('url', FORBIDDEN_FOR_AUTHENTICATED_PAGES)
    def test_forbidden_for_signed_in(client, user, url):
        # For all the pages that forbidden after signed in
        data = {
            'email': '_qa_catedor@storemeapp.com',
            'password': 'The_Best_Pass',
            'submit': 'submit'
        }
        client.post(SIGNIN_PAGE, data=data, follow_redirects=True)
        response = client.get(url, follow_redirects=True)
        assert len(re.findall(VALIDATION_MESSAGES['aleady_signed_in'], response.data)) == 1
