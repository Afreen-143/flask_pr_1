# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# MODEL
class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    book = db.Column(db.String(100), nullable=False)

    author = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)


# CREATE DATABASE
with app.app_context():
    db.create_all()


# MAIN HOME PAGE
@app.route('/')
def homepage():

    name = "Shaik Afreen"

    return render_template(
        'homepage.html',
        name=name
    )


# ABOUT PAGE
@app.route('/about')
def about():

    about = "Library Management Project"

    return render_template(
        'about.html',
        about=about
    )


# CONTACT PAGE
@app.route('/contact')
def contact():

    contact = "9030523441"

    return render_template(
        'contact.html',
        contact=contact
    )


# CRUD HOME PAGE
@app.route('/crud-home')
def home():

    books = Book.query.all()

    return render_template(
        'home.html',
        books=books
    )


# BOOK DETAILS PAGE
@app.route('/book-details')
def book_details():

    books = Book.query.all()

    return render_template(
        'book_details.html',
        books=books
    )


# ADD BOOK
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        id = request.form['id']
        book = request.form['book']
        author = request.form['author']
        price = request.form['price']

        new_book = Book(
            id=id,
            book=book,
            author=author,
            price=price
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_book.html')


# UPDATE BOOK
@app.route('/update-book/<int:id>', methods=['GET', 'POST'])
def update_book(id):

    old_book = Book.query.get(id)

    if request.method == 'POST':

        old_book.book = request.form['book']
        old_book.author = request.form['author']
        old_book.price = request.form['price']

        db.session.commit()

        return redirect(url_for('home'))

    return render_template(
        'update_book.html',
        book=old_book
    )
# DELETE BOOK
@app.route('/delete-book/<int:id>')
def delete_book(id):

    book = Book.query.get(id)

    db.session.delete(book)

    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)