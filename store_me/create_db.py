import random

from faker import Faker
import pandas
from store_me import bcrypt
import secrets
from store_me.models import Users, Products, Orders

class Create_DB:
    users = []
    products = []
    orders = []

    def __init__(self, db):
        self.db = db
        db.create_all()
        self.create_users()
        self.create_products()
        self.create_orders()
        print(self)

    def create_users(self):
        #create users
        faker = Faker()

        for _ in range(2):
            user = Users(firstname=faker.first_name(),
                            lastname=faker.last_name(),
                            username=faker.user_name(),
                            email=faker.email(),
                            password=bcrypt.generate_password_hash("test_pass").decode('utf-8'))
            self.users.append(user)
            self.db.session.add(user)
        self.db.session.commit()


    def create_products(self):
        DB_PATH = "styles.csv"
        index = 0
        products_df = pandas.read_csv(DB_PATH)
        for _, product in products_df[['id', 'gender', 'productDisplayName', 'baseColour']].iterrows():
            if product.productDisplayName == "":
                product_name_to_add = "No Name"
            else:
                product_name_to_add = product.productDisplayName
            product_to_add = Products(id=product.id,
                            product_name=product_name_to_add,
                            gender=product.gender,
                            base_color=product.baseColour,
                            main_photo_path=f"{product.id}.jpg",
                            price=round(random.uniform(10, 100), 2),
                            sold_count=0)
            print(index)
            index += 1
            self.products.append(product_to_add)
            self.db.session.add(product_to_add)
            if(index % 1000 == 0):
                self.db.session.commit()

    def get_random_mail(self):
        return random.choice(self.users).email
    
    def get_random_product_id(self):
        return random.choice(self.products).id

    def create_orders(self):
        for i in range(2):
            order = Orders(id=secrets.token_hex(8),
                            email=self.get_random_mail(),
                            product_id=self.get_random_product_id())
            self.orders.append(order)
            self.db.session.add(order)
        self.db.session.commit()

    def remove_DB(self):
        self.db.drop_all()

    def __str__(self):
        return f"""Users: {len(self.users)}
                Products: {len(self.products)}
                Orders: {len(self.orders)}"""

# creator = Create_DB()
# creator.create_users()
# creator.create_products()
# creator.create_orders()
#print(creator)



