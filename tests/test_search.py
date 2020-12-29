from http import HTTPStatus
import pytest
import re

from StoreMeApp.store_me import models


PAGES = ['/', '/home', '/signIn', '/signUp', f'/product/{models.Products.get_random_product_number()}']

HOME_PAGE = '/'
VALIDATION_MESSAGES = {
    'empty_required_field': b'This field is required',
    'required_page': b'Please log in to access this page',
    'aleady_signed_in': b'You are already signed In'
}


class TestSearch:
    @staticmethod
    def test_search_product(client, product):
        data = {
            'search_txt': product.product_name,
            'search': 'Search'
        }
        response = client.post(HOME_PAGE, data=data, follow_redirects=True)
        assert product.product_name in str(response.data)    