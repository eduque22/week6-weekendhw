from flask import Blueprint, request, jsonify
from book_inventory.helpers import token_required
from book_inventory.models import db, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/books', methods = ['POST'])
@token_required
def create_book(our_user):

    title = request.json['title']
    author = request.json['author']
    cover = request.json['cover']
    genre = request.json['genre']
    release_date = request.json['release_date']
    user_token = our_user.token

    print(f'User Token: {our_user.token}')

    book = Book(title, author, cover, genre, release_date, user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def one_book(our_user, id):
    if id:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

@api.route('/books', methods = ['GET'])
@token_required
def all_books(our_user):
    token = our_user.token
    books = Book.query.filter_by(user_token = token).all()
    response = books_schema.dump(books)

    return jsonify(response)


@api.route('/books/<id>', methods = ['PUT'])
@token_required
def update_book(our_user, id):
    book = Book.query.get(id)

    book.title = request.json['title']
    book.author = request.json['author']
    book.cover = request.json['cover']
    book.genre = request.json['genre']
    book.release_date = request.json['release_date']

    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)

@api.route('/pokecards/<id>', methods = ['DELETE'])
@token_required
def delete_book(our_user, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)