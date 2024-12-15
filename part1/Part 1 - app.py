from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "Databsse.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/books', methods=['POST'])
def add_book():
    books = load_data()
    new_book = request.json

    required_fields = ['title', 'author', 'year', 'isbn']
    for field in required_fields:
        if field not in new_book:
            return jsonify({"error": f"'{field}' is required"}), 400


    if any(book['isbn'] == new_book['isbn'] for book in books):
        return jsonify({"error": "A book with this ISBN already exists."}), 400

    books.append(new_book)
    save_data(books)
    return jsonify({"message": "Book added successfully."}), 201


@app.route('/books', methods=['GET'])
def list_books():
    books = load_data()
    return jsonify(books), 200


@app.route('/books/search', methods=['GET'])
def search_books():
    books = load_data()
    author = request.args.get('author')
    year = request.args.get('year')
    genre = request.args.get('genre')

    filtered_books = books
    if author:
        filtered_books = [book for book in filtered_books if book['author'].lower() == author.lower()]
    if year:
        filtered_books = [book for book in filtered_books if str(book['year']) == year]
    if genre:
        filtered_books = [book for book in filtered_books if book.get('genre', '').lower() == genre.lower()]

    return jsonify(filtered_books), 200


@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    books = load_data()
    filtered_books = [book for book in books if book['isbn'] != isbn]

    if len(books) == len(filtered_books):
        return jsonify({"error": "Book not found."}), 404

    save_data(filtered_books)
    return jsonify({"message": "Book deleted successfully."}), 200


@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    books = load_data()
    book_to_update = next((book for book in books if book['isbn'] == isbn), None)

    if not book_to_update:
        return jsonify({"error": "Book not found."}), 404

    updated_data = request.json
    for key, value in updated_data.items():
        if key in book_to_update:
            book_to_update[key] = value

    save_data(books)
    return jsonify(book_to_update), 200

if __name__ == '__main__':

    if not os.path.exists(DATA_FILE):
        save_data([])

    app.run(debug=True, host='0.0.0.0', port=5000)
