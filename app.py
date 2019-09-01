#--------------------------------------------------------------------------------------------------------------------
# Flask App for rendering template for Mars Data Site
# -------------------------------------------------------------------------------------------------------------------
import scrape_mars

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# initialize flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route that renders index.html template using mongo data
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", data=mars_data)


# Route that performs scrape of mars data
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update Mongo database
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)