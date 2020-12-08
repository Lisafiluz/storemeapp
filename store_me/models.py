from datetime import datetime

from store_me import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='user_default.jpg')
    birthday = db.Column(db.DateTime, nullable=True)
    orders = db.relationship('Orders', backref='orders', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.username}', '{self.email}', '{self.birthday}')"


class Products(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    base_color = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float, nullable=False)
    main_photo_path = db.Column(db.String(20), nullable=False, default='product_default.jpg')
    other_photos_path = db.Column(db.String(20), nullable=True)
    sold_count = db.Column(db.Integer, nullable=False, default=0)
    orders = db.relationship('Orders', backref='purchases', lazy=True)  # For analyze orders for a Product

    def __repr__(self):
        return f"Product('{self.id}', '{self.product_name}', '{self.gender}', '{self.base_color}', '{self.price}', '{self.main_photo_path}', '{self.other_photos_path}', '{self.sold_count}')"



class Orders(db.Model):
    id = db.Column(db.String(16), unique=True, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)  # users = table name!
    product_id = db.Column(db.String(16), db.ForeignKey('products.id'), nullable=False)  # products = table name!
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Order('{self.id}', '{self.email}', '{self.product_id}', '{self.order_date}')"


class Carts(db.Model):
    id = db.Column(db.String(16), unique=True, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('users.email'), unique=True, nullable=False)  # users = table name!
    product_id = db.Column(db.String(16), db.ForeignKey('products.id'), unique=True)  # products = table name!

    def __repr__(self):
        return f"Cart('{self.id}', '{self.email}', '{self.product_id}')"