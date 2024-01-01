# to activate venv use - .\\flask_venv\Scripts\activate

from bson import ObjectId
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'supersecretkey'
client = MongoClient(host="mongo_container", port=27017)
db = client.BookShelf
shelf = db.bookShelf


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        operation = request.form['submitButton']
        if operation == "Add Book":
            title = request.form['title']
            author = request.form['author']
            year = request.form['year']
            if title and author and year:
                shelf.insert_one({"title" : title, "author" : author, "year" : year})
        elif operation == "Delete":
            bookId = request.form['bookId']
            shelf.delete_one({"_id": ObjectId(bookId)})
    currentShelf = shelf.find()
    return render_template('bookShelf.html', books=currentShelf)

if __name__ == "__main__":
    app.run(debug=True)