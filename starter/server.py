from flask import Flask, render_template, request, redirect, url_for, session, flash
import jinja2
from melons import get_all, get_by_id, Melon
from forms import LoginForm
import customers

app = Flask(__name__)
# for debugging purposes
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = "dev"

# flask routes for the app


@app.route("/")
def home():
    """Home page"""
    return render_template("/base.html")


@app.route("/melons")
def melons():
    """Returns a page with all melons"""
    melons_list = get_all()
    return render_template("/all_melons.html", melons_list=melons_list)


@app.route("/melon/<melon_id>")
def melon_details(melon_id):
    """Returns a page with a specific melon. Also, provides a button to buy that melon."""
    melon = get_by_id(melon_id)
    return render_template("/melon.html", melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Adds a melon to the cart. Redirects to the cart page. Redirects to login page if username not in session"""
    if 'username' not in session:
        flash('Please Log in Before Adding to Cart')
        return redirect('/login')
    # create an empty dictionary for session[“cart”] if the key “cart” doesn’t already exist in the session:
    if "cart" not in session:
        session["cart"] = {}
    # if the melon_id is already in the cart, increment the quantity by 1
    if melon_id in session["cart"]:
        session["cart"][melon_id] += 1
    # if the melon_id is not in the cart, add it to the cart with a quantity of 1
    else:
        session["cart"][melon_id] = 1
    flash(f"{melon_id} added to cart")

    print(sum(session["cart"].values()))
    

    session.modified = True # this is to tell flask that the session has been modified
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    """Returns a page with the contents of the cart. Redirects to Login page if username not in session"""
    if 'username' not in session:
        flash('Please Log in Before Adding to Cart')
        return redirect('/login')
    order_total = 0
    cart_melons = []
    #get cart dict from session (or an empty one if none exists yet)
    cart = session.get("cart", {})
    #iterate over the cart dict
    for melon_id, quantity in cart.items():
        #get the melon object for each melon_id
        melon = get_by_id(melon_id)
        melon.quantity = quantity
        #calculate the subtotal for each melon
        subtotal = quantity * melon.price
        melon.subtotal = subtotal
        #add the subtotal to the order total
        order_total += subtotal
        #add the melon object and the quantity to a list of melons
        cart_melons.append((melon))
    # if the cart is empty, redirect to the melons page
    if not cart_melons:
        flash("Your cart is empty")
        return redirect(url_for("empty_cart"))
    return render_template("/cart.html", cart_melons=cart_melons, order_total=order_total, subtotal=subtotal)

#empty cart page
@app.route("/empty_cart")
def empty_cart():
    """Resets the session['cart'] and returns a page that says the cart is empty"""
    session["cart"] = {}
    return render_template("/empty_cart.html")

# remove from cart
@app.route("/remove_from_cart/<melon_id>")
def remove_from_cart(melon_id):
    """Reduces the quantity a melon by one from the cart. Redirects to the cart page."""
    # if the melon_id is in the cart, subtract 1 from the quantity, if the quantity is 0, remove the melon_id from the cart
    if melon_id in session["cart"]:
        if session["cart"][melon_id] == 1:
            del session["cart"][melon_id]
            flash(f"{melon_id} removed from cart")
            session.modified = True
            return redirect(url_for("cart"))
        session["cart"][melon_id] -= 1
        flash(f"One {melon_id} removed from cart")
        session.modified = True
        return redirect(url_for("cart"))

# instantiate a loginForm and pass the form into a template
@app.route("/login", methods=["GET", "POST"])
def login():
    """Returns a login form and handles login"""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check to see if a registered user exists with this username
        user = customers.get_by_username(username)

        if not user or user['password'] != password:
            flash('Invalid username or password')
            return redirect('/login')

        # store username in session to keep track of logged in user
        session["username"] = user['username']
        flash('Logged In') 
        return redirect("/melons")
    #form has not been submitted or data was not validated
    return render_template("login.html", form=form)

#add a logout route
@app.route("/logout")
def logout():
    '''a logout route that removes the username from the session and redirects them to the login page'''
    del session["username"]
    flash('Logged Out')
    return redirect("/login")

# error handler
@app.errorhandler(404)
def error_handled(e):
    return render_template('/error.html')

if __name__ == "__main__":
    app.env = "development"
    app.run(debug=True, port=8000, host="localhost")
