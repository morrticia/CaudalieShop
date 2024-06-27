from extensions import db, app, login_manager
from flask_login import UserMixin
from seeddata import *
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()


class Product(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    image_url = db.Column(db.String)
    text = db.Column(db.String)

    category_id = db.Column(db.ForeignKey("product_category.id"))
    category = db.relationship("ProductCategory", back_populates="products")


class ProductCategory(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    products = db.relationship("Product", back_populates="category")


class User(BaseModel, db.Model, UserMixin):
    def __init__(self, email, password, role="user"):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("db was created")

        admin = User("admin@gmail.com", "1234", "admin")
        admin.create()
        print("admin was created")

        for category in categories:
            print(category["name"])
            new_category = ProductCategory()
            new_category.name = category["name"]

            new_category.create()

        for product in products:
            new_product = Product()

            new_product.name = product["name"]
            new_product.price = product["price"]
            new_product.text = product["text"]
            new_product.image_url = product["image_url"]
            new_product.category_id = product["category_id"]

            new_product.create()


