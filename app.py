from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_m
import config
from boto.s3.connection import S3Connection

app = Flask(__name__)
app.config["MONGO_URI"] = process.env.MONGOLAB_URI
mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars_mission=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_m.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
