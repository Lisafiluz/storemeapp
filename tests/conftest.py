import datetime
import os
import secrets
import tempfile

import pytest

from StoreMeApp.store_me import app, models


@pytest.fixture
def client():

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        yield client
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def user():
    user_details = {
        'firstname': f'_qa_first{secrets.token_hex(2)}',
        'lastname': f'_qa_last{secrets.token_hex(2)}',
        'username': f'_qa{secrets.token_hex(2)}',
        'email': '_qa_catedor@storemeapp.com',
        'password': 'The_Best_Pass',
        'birthday': datetime.date(1997, 5, 26)
    }
    qa_catedor = models.Users.create_user(**user_details)
    yield qa_catedor
    models.Users.delete_user(user_details['username'])


@pytest.fixture
def product():
    product_details = {
        'product_name': f'_qa_product{secrets.token_hex(4)}',
        'gender': 'Unisex',
        'base_color': 'green',
        'price': 100.1
    }
    product = models.Products.create_product(**product_details)
    yield product
    models.Products.delete_product(product.id)
