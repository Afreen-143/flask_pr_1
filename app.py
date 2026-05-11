from flask import Flask ,render_template , request , jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model) :
        id =  db.Column(db.Integer, primary_key=True)
        book = db.Column(db.String(100), nullable=False)
        author = db.Column(db.String(100), nullable=False)
        price = db.Column(db.Float, nullable=False)
        
        def to_dict(self) :
                return {
                        "id" : self.id,
                        "book" : self.book,
                        "author" : self.author,
                        "price" : self.price
                }

with app.app_context() :
        db.create_all()


        
 
@app.route('/home' )
def home() :
        return render_template("homepage.html" )

@app.route('/about' )
def about() :
        return render_template("aboutus.html" )

@app.route('/contact' )
def contact() :
        return render_template("contact.html" )

# API Endpoints

@app.route('/api/books/<int:id>')
def get_single_book(id):
        book=Book.query.get(id) #got data in object format
        book_dict=book.to_dict()  #object-->dict
        book_json=jsonify(book_dict) #Dict-->json

        return book_json
          #data sent through api
        



@app.route('/api/books', methods=['POST',])
def add_book():

    data = request.get_json()

    new_book = Book(
        book=data['book'],
        author=data['author'],
        price=data['price']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dict()), 201
        
@app.route('/api/books/<int:id>', methods=['PATCH'])
def update_book(id):

    data_to_update = request.get_json()

    old_data = Book.query.get(id)
    old_data.book = data_to_update.get('book', old_data.book)
    old_data.author = data_to_update.get('author', old_data.author)
    old_data.price = data_to_update.get('price', old_data.price)
    db.session.commit()

    return jsonify(old_data.to_dict()), 200



@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):

    book = Book.query.get(id)

    if not book:
        return jsonify({
            "message": "Book not found"
        }), 404

    db.session.delete(book)

    db.session.commit()

    return jsonify({
        "message": "Book deleted successfully"
    }), 200

        


if __name__ == "__main__" :                                                                                                           
        app.run(debug=True)