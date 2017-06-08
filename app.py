# Import statement
from flask import Flask, render_template, Markup, url_for, flash, redirect, request
import os
from datetime import date
from flask_mail import Mail, Message

app =Flask(__name__)
mail=Mail(app)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'wtgeographer@gmail.com'
app.config['MAIL_PASSWORD'] = 'Carroll@17'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Route to send email
@app.route("/send", methods=['GET','POST'])
def send():
    """Function to send email using flask_mail"""

    sender = str(request.form['email'])
    subject = str(request.form['name'])
    content = str(request.form['comments'])

    msg = Message(subject, sender = sender, recipients = ['sales@sophisticatedcollector.com'])
    msg.body = content
    mail.send(msg)
    return redirect(url_for("contact"))

products_info = [
    {
        "id": "101",
        "name": "Cradleboards",
        "description": "Collection of (3) Full Size Beaded Cradleboards",
        "img": "craddle-boards.jpg",
        "price": 100000,
        "item": "VWNZ5Z44A8WPG"
    },

    {
        "id": "102",
        "name":"Dolls",
        "description": "Collection of Southwest Dolls",
        "img": "dolls.jpg",
        "price": 1500,
        "item": "VHPACXWJTPNLC"
    },

    {
        "id": "103",
        "name": "Doll",
        "description": "Native American Beaded Doll w/ Horse Hair",
        "img": "doll.jpg",
        "price": 5000,
        "item": "3YY454Z9ZECEN"
    },

    {
        "id": "104",
        "name": "Chair",
        "description": "Elk Skin Chair and Ottoman w/ Painted Buckskin Throw Pillow",
        "img": "chair.jpg",
        "price": 15000,
        "item": "45U6TDNUC9F9Q"
    },

    {
        "id": "105",
        "name": "Ottoman",
        "description": "Southwest Painted Buckskin Ottoman",
        "img": "otto.jpg",
        "price": 2000,
        "item": "FEWJGHYDYTN4J"
    },

    {
        "id": "106",
        "name": "Tommy Macaione",
        "description": "Santa Fe Artist Tommy Macaione - Verified, Unsigned",
        "img": "painting.jpg",
        "price": 10000,
        "item": "V2PWSCNDSX59C"
    }
]

# Routes
# All functions should have a page_title variables if they render templates

@app.route("/")
def index():
    """Function for homepage"""
    
    items = []

    for product in products_info[:4]:
        item = {
        'img': url_for("static", filename=product["img"]),
        'name': product["name"],
        'description':product['description'],
        'page_url': url_for("item", product_id=product["id"])
        }
        items.append(item)

    return render_template("index.html", page_title="Sophisticated", current_year=date.today().year, items=items)


@app.route("/all")
def all():
    """Function for the all Listing Page"""
    items = []

    for product in products_info:
        item = {
        'img': url_for("static", filename=product["img"]),
        'name': product["name"],
        'description':product['description'],
        'page_url': url_for("item", product_id=product["id"])
        }
        items.append(item)

    return render_template("all.html", page_title="Sophisticated", current_year=date.today().year, items=items)


@app.route("/item/<product_id>")
def item(product_id):
    """Function for Individual Item Page"""
    context = {"page_title": "Sophisticated Collector", "current_year": date.today().year}
    my_product = ""
    for product in products_info:
        if product["id"] == product_id:
            my_product = product
    context["product"] = my_product
    flash("This site is a demo do not buy anything")
    return render_template("item.html", **context)


@app.route("/receipt")
def receipt():
    """Function to display receipt after purchase"""
    context = {"page_title": "Sophisticated Collector", "current_year": date.today().year}
    return render_template("receipt.html", **context)


@app.route("/contact")
def contact():
    """Function for contact page"""
    context = {"page_title": "Sophisticated Collector", "current_year": date.today().year}
    return render_template("contact.html", **context)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

    
# Run application
if __name__ == "__main__":
    app.run(debug=True)
