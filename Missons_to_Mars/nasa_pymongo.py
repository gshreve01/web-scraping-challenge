import pymongo

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.nasa


def insert_mars_data(mars_data):
    db.mars.drop()
    db.mars.insert(mars_data)
    print("Mars Data Uploaded!")

def get_mars_data():
    mars_data = db.mars.find_one()
    return mars_data
