import os

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from .. import db
from ..models import CartItem, CustomerOrder, OrderItem, Product, User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)


@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])
    products = Product.query.all()

    return render_template("dashboard.html", user=user, products=products)


@main.route("/add-product", methods=["GET", "POST"])
def add_product():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if user.role != "admin":
        flash("Admin access required")
        return redirect(url_for("main.home"))

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        file = request.files.get("image")

        if not name or not price:
            flash("Name and Price are required!")
            return redirect(url_for("main.add_product"))

        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            if not filename:
                flash("Invalid image filename!")
                return redirect(url_for("main.add_product"))

            # Save under app/static/uploads so Flask can serve it via url_for('static', ...)
            upload_folder = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)

            try:
                file.save(filepath)
            except Exception as e:
                flash(f"Error saving file: {str(e)}")
                return redirect(url_for("main.add_product"))

        try:
            price_float = float(price)
        except ValueError:
            flash("Price must be a valid number!")
            return redirect(url_for("main.add_product"))

        new_product = Product(
            name=name,
            price=price_float,
            description=description,
            image=filename,
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            flash("Product added successfully!")
            return redirect(url_for("main.home"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving to database: {str(e)}")
            return redirect(url_for("main.add_product"))

    return render_template("add_product.html")


@main.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    if "user_id" not in session:
        flash("Please Login First")
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash("Product added to cart!")
    return redirect(url_for("main.home"))


@main.route("/cart")
def view_cart():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return render_template("cart.html", cart_items=cart_items)


@main.route("/checkout")
def checkout():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        flash("Your cart is empty!")
        return redirect(url_for("main.home"))

    new_order = CustomerOrder(user_id=user_id)

    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.session.add(order_item)
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash("Order placed successfully!")
    return redirect(url_for("main.home"))


@main.route("/orders")
def orders():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    orders = CustomerOrder.query.filter_by(user_id=user_id).all()
    return render_template("orders.html", orders=orders)
