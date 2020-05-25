#import flask
from flask import Flask, render_template
import json

#import my libraries
from scrape_mars import scrape
from nasa_pymongo import insert_mars_data, get_mars_data

app = Flask(__name__)

@app.route("/scrape")
def scrape_data():
    mars_data = scrape()
    insert_mars_data(mars_data)
    return "Mars data updated to nasa database"

@app.route("/")
def home():
    mars_data = get_mars_data()
    return render_template("mars.html", mars_data = mars_data)