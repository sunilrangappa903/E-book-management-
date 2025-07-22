from flask import render_template, url_for, flash, redirect, request, Blueprint
from forms import RegistrationForm, LoginForm, UploadForm, ReviewForm
from models import User, Book, Review
from app import db  # Import db, but NOT app
from flask_login import login_user, current_user, logout_user, login_required
import os
from werkzeug.utils import secure_filename

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/")
@routes_bp.route("/home")
def home():
    # ...existing code...
    return render_template('home.html', books=books)

@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    # ...existing code...
    return render_template('register.html', title='Register', form=form)

@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    # ...existing code...
    return render_template('login.html', title='Login', form=form)

@routes_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes_bp.route("/dashboard")
@login_required
def dashboard():
    read_books = Book.query.join(Review).filter(Review.user_id == user_id).all()
    # Example: Recommend books from the same genre as previously read books
    user_id = current_user.id
    # Fetch user's reading history (replace with actual logic)
    read_books = Book.query.join(Review).filter(Review.user_id == user_id).all()
    recommended_books = []
    if read_books:
        genres = [book.genre for book in read_books if book.genre]
        if genres:
            most_common_genre = max(set(genres), key=genres.count)
            recommended_books = Book.query.filter(Book.genre == most_common_genre).limit(5).all()

    return render_template('dashboard.html', recommended_books=recommended_books)

@routes_bp.route("/books")
def book_list():
    books = Book.query.all()
    # Add filtering and sorting logic here
    return render_template('book_list.html', books=books)

@routes_bp.route("/book/<int:book_id>")
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()
    return render_template('book_details.html', book=book, form=form)

@routes_bp.route("/book/<int:book_id>/review", methods=['POST'])
@login_required
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(rating=form.rating.data, comment=form.comment.data, user_id=current_user.id, book_id=book.id)
        db.session.commit()
        flash('Your review has been added!', 'success')
        return redirect(url_for('routes.book_details', book_id=book.id))
    return render_template('book_details.html', book=book, form=form)

@routes_bp.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.book_file.data
        filename = secure_filename(f.filename)
        upload_folder = os.path.join(app.root_path, 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, filename)
        f.save(file_path)

        cover = form.cover_image.data
        cover_filename = None
        cover_path = None

        if cover:
            cover_filename = secure_filename(cover.filename)
            cover_path = os.path.join(app.root_path, 'static/covers', cover_filename)
            cover.save(cover_path)

        book = Book(title=form.title.data, author=form.author.data, genre=form.genre.data,
                    description=form.description.data, file_path=file_path,
                    cover_image=cover_filename)
        db.session.add(book)
        db.session.commit()
        flash('Book uploaded successfully!', 'success')
        return redirect(url_for('routes.book_list'))
    return render_template('upload.html', form=form)

@routes_bp.route("/admin")
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('routes.home'))
    users = User.query.all()
    books = Book.query.all()
    return render_template('admin_panel.html', users=users, books=books)

@routes_bp.route("/profile")
@login_required
def user_profile():
    return render_template('user_profile.html')