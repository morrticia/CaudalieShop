from flask import render_template, redirect
from forms import AddProduct, RegisterForm, LoginForm
from extensions import app
from models import Product, User, ProductCategory
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
def home():
    role = "user"
    return render_template("index.html", products=Product.query.all(), role=role)


@app.route("/about")
def about():
    return "About page"


@app.route("/welcome")
def welcome():
    names = ['Nina', 'Gio', 'Saba']
    return render_template("welcome.html", names=names)


@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html", id=product_id)

    return render_template("product.html", product=product)


@app.route("/products")
@app.route("/products/<int:category_id>")
def products(category_id=None):
    if category_id:
        category = ProductCategory.query.get(category_id)
        if category:
            products = category.products
        else:
            products = []
    else:
        products = Product.query.all()

    return render_template("products.html", products=products)


@app.route("/add_product", methods=['POST', 'GET'])
def add_product():
    form = AddProduct()

    if form.validate_on_submit():
        # image = form.image.data
        # file_path = os.path.join("static", "images", image.filename)
        new_product = Product(name=form.name.data, text=form.text.data, price=form.price.data,
                              image_url=form.image_url.data, category_id=1)

        new_product.create()
        return redirect("/")
        # image.save(os.path.join(app.root_path, file_path))
    else:
        print(form.errors)

    return render_template("add_product.html", form=form)

@app.route("/edit_product/<int:product_id>", methods=['POST', 'GET'])
@login_required
def edit_product(product_id):

    if current_user.role != 'Admin':
        return redirect("/")
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")

    form = AddProduct(name=product.name, text=product.text, image_url=product.image_url, price=product.price)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.text = form.text.data
        product.image_url = form.image_url.data

        product.save()
        return redirect("/")

    return render_template("edit_product.html", form=form)


@app.route("/delete_product/<int:product_id>", methods=['GET', 'DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")

    product.delete()

    return redirect("/")


@app.route("/register")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        new_user.create()
    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

















