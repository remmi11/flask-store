# Main file for Shirts4Mike

# Import statement
from flask import (
    Flask,
    render_template,
    Markup,
    url_for,
    flash,
    redirect,
    request
)

import sendgrid
import os
from datetime import date

# App setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"

# Get details for sendgrid details
sendgrid_file = "sendgrid.txt"
sendgrid_details = []

with open(sendgrid_file) as f:
    sendgrid_details = f.readlines()
    sendgrid_details = [x.strip("\n") for x in sendgrid_details]

# Global Variables
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


# Route to send email
@app.route("/send", methods=['POST'])
def send():
    """Function to send email using sendgrid API"""
    sendgrid_object = sendgrid.SendGridClient(
        sendgrid_details[0], sendgrid_details[1])
    message = sendgrid.Mail()
    sender = request.form["email"]
    subject = request.form["name"]
    body = request.form["message"]
    message.add_to("sales@sophisticatedcollector.com")
    message.set_from(sender)
    message.set_subject(subject)
    message.set_html(body)
    sendgrid_object.send(message)
    flash("Email sent.")
    return redirect(url_for("contact"))

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
