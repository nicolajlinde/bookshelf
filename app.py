from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)


db.create_all()


@app.route('/')
def home():
    all_books = Book.query.all()

    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']

        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/delete/<int:id>")
def delete(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    book = Book.query.filter_by(id=id).first()
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.rating = request.form['rating']
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template('edit.html', book=book)



if __name__ == '__main__':
    app.run()
