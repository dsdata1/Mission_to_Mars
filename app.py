from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_m
import os


is_prod = os.environ.get('MONGODB_URI', None)

app = Flask(__name__)
app.config["MONGO_URI"] = is_prod
mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars_mission=mars)

#testing
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
