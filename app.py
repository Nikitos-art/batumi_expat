from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['cafesDB']
collection = db['cafes_rests_2']

client2 = MongoClient('mongodb://localhost:27017')
db2 = client2['aptDB']
collection2 = db2['apartments']


@app.route('/')
def display():
    return render_template('index.html')


# @app.route('/item/<item_id>')
# def display_item(item_id):
#     item = collection.find_one({'_id': item_id})
#     return render_template('item.html', item=item)

@app.route('/cafes')
def display_cafes():
    data = collection.find()
    return render_template('cafes.html', data=data)


@app.route('/apts')
def display_apts():
    data = collection2.find()
    return render_template('apts.html', data=data)


# @app.route('/outdoors')
# def display_outdoors():
#     return render_template('outdoors.html')


if __name__ == '__main__':
    app.run(port=5001)
