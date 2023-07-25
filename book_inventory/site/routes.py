from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from book_inventory.forms import BookForm
from book_inventory.models import Book, db

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    bookform = BookForm()

    try:
        if request.method =='POST' and bookform.validate_on_submit():
            title = bookform.title.data
            author = bookform.author.data
            cover = bookform.cover.data
            genre = bookform.genre.data
            release_date = bookform.release_date.data
            user_token = current_user.token

            book = Book(title, author, cover, genre, release_date, user_token)

            db.session.add(book)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Book not created, please review form and try again.')
    
    user_token = current_user.token
    books = Book.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=bookform, books=books)