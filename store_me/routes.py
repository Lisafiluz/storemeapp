import datetime
from http import HTTPStatus
from . import app, db, bcrypt
import secrets
from flask import abort, jsonify, render_template, redirect, url_for, request, flash, redirect
from .forms import SignUpForm, SignInForm, UpdateUserForm, SearchProductForm, AddToCartForm
from .models import Users, Products, Orders, Carts
from flask_login import login_user, current_user, logout_user, login_required


global search_limitation
search_limitation = 40


def get_searched_products(search_txt: str, limit: int) -> list:
    search = "%{}%".format(search_txt)
    top_products = Products.query.filter((Products.product_name.like(search))
                                        | (Products.gender.like(search))
                                        | (Products.base_color.like(search))).all()
    return (len(top_products), top_products[:limit])


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    search_form = SearchProductForm()
    if request.method == 'POST' and search_form.search.data:
        if search_form.validate_on_submit():
        # TODO add user results count in 
            top_products = get_searched_products(search_form.search_txt.data, search_limitation)
            return render_template('HomePage.html',
                                    search_form=search_form,
                                    search_txt=search_form.search_txt.data,
                                    search_count=top_products[0],
                                    cards=top_products[1])
    
    top_products = Products.query.order_by(Products.sold_count.desc())[:search_limitation]
    # add_to_cart_form = AddToCartForm()
    # if add_to_cart_form.validate_on_submit():
    #     print("ADD TO CART", add_to_cart_form.add)
    # TODO
    # 1. get categories for ordering -> gender, base color, price
    return render_template('HomePage.html', search_form=search_form, cards=top_products)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if current_user.is_authenticated:
        flash(f'You are already signed In.', 'info')
        return redirect(url_for('home'))
    
    search_form = SearchProductForm()
    if request.method == 'POST' and search_form.search.data:
        if search_form.validate_on_submit():
            top_products = get_searched_products(search_form.search_txt.data, search_limitation)
            return render_template('HomePage.html', search_form=search_form, search_txt=search_form.search_txt.data, search_count=top_products[0], cards=top_products[1])
    
    form = SignUpForm()
    if request.method == 'POST' and form.submit.data: 
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = Users(firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        birthday=form.birthday.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Your acount has been created! You are now able to sign in', 'success')
            return redirect(url_for('signIn'))
    return render_template('SignUp.html', title='sign up', search_form=search_form, form=form)


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        flash(f'You are already signed In.', 'info')
        return redirect(url_for('home'))

    search_form = SearchProductForm()
    if request.method == 'POST' and search_form.search.data: 
        if search_form.validate_on_submit():
            top_products = get_searched_products(search_form.search_txt.data, search_limitation)
            return render_template('HomePage.html', search_form=search_form, search_txt=search_form.search_txt.data, search_count=top_products[0], cards=top_products[1])
    
    form = SignInForm()
    if request.method == 'POST' and form.submit.data:
        if form.validate_on_submit():
            user = Users.query.filter(Users.email.ilike(form.email.data)).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'Sign in successful.', 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f'Sign in unsuccessful. Please check email or password', 'danger')
                return render_template('SignIn.html', title='sign in', search_form=search_form, form=form), HTTPStatus.UNAUTHORIZED

    return render_template('SignIn.html', title='sign in', search_form=search_form, form=form)


@app.route('/signOut')
def signOut():
    if current_user.is_authenticated:
        logout_user()
        flash(f'You are succesfuly signed out.', 'info')
        return redirect(url_for('home'))
    else:
        next_page = request.args.get('next')
        flash(f'You are not signed-in and can not signed-out', 'info')
        return redirect(url_for('home'))


@app.route('/MyProfile', methods=['GET', 'POST'])
@login_required
def myProfile():
    search_form = SearchProductForm()
    if request.method == 'POST' and search_form.search.data:
        top_products = get_searched_products(search_form.search_txt.data, search_limitation)
        return render_template('HomePage.html',
                                search_form=search_form,
                                search_txt=search_form.search_txt.data,
                                search_count=top_products[0],
                                cards=top_products[1])
    form = UpdateUserForm()
    if request.method == 'POST' and form.save.data:
        if form.validate_on_submit():
            if form.password.data:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            else:
                hashed_password = current_user.password
            user = Users(firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        username=current_user.username,
                        email=current_user.email,
                        password=hashed_password,
                        birthday=form.birthday.data)
            user_for_update = Users.query.filter_by(email=current_user.email).first()
            user_for_update.firstname = user.firstname
            user_for_update.lastname = user.lastname
            # user_for_update.username = user.username
            user_for_update.password = hashed_password
            user_for_update.birthday = user.birthday
            db.session.commit()
            flash(f'Your acount has been updated!', 'success')
            return redirect(url_for('myProfile'))
    elif form.delete.data:
        Users.query.filter_by(email=current_user.email).delete()
        db.session.commit()
        flash(f'Your acount has been deleted!', 'success')
        return redirect(url_for('signOut'))
    orders = Orders.query.join(Products).add_columns(Products.product_name, Products.price, Products.id).filter(Orders.email==current_user.email).all()
    return render_template('MyProfile.html', title=current_user.username, search_form=search_form, form=form, orders=orders)


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def get_product(product_id):
    search_form = SearchProductForm()
    if request.method == 'POST' and search_form.search.data:
        if search_form.validate_on_submit():
            top_products = get_searched_products(search_form.search_txt.data, search_limitation)
            return render_template('HomePage.html', search_form=search_form, search_txt=search_form.search_txt.data, search_count=top_products[0], cards=top_products[1])
    
    product = Products.query.filter_by(id=product_id).first()
    return render_template('Product.html', search_form=search_form, product=product)


@app.route('/buy/<product_ids>', methods=['GET', 'POST'])
@login_required
def buy(product_ids):
    for product_id in product_ids.split(','):
        product = Products.query.filter_by(id=product_id).first()
        product.sold_count += 1
        order = Orders(id=secrets.token_hex(8), email=current_user.email, product_id=product_id)
        db.session.add(order)
    db.session.commit()
    flash(f'Your order is on the way for you!', 'success') # don't work
    return redirect(url_for('myProfile'))  # don't work