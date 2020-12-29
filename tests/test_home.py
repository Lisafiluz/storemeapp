from http import HTTPStatus
import pytest
import re


HOME_PAGE = ['/', '/home']

VALIDATION_MESSAGES = {
    'empty_required_field': b'This field is required',
}


class TestHomePage:
    pass