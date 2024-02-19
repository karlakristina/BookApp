from __init__ import Session

from users import User
from books import Book
from category import Category
from cart import Cart
from __init__ import Base
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename

import os 
from flask import Flask,render_template, request,redirect, url_for,flash,session


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__, static_folder='../static', static_url_path='/static', template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
app.secret_key = 'ovo-je-moj-tajni-kljuc'
app.config['SESSION_TYPE'] = 'filesystem'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index ():
    return render_template('login.html') 

@app.route("/register")
def register ():
    return render_template('register.html') 


@app.route("/book")
def book ():
    user_id = session['user_id'] 
    categories = Session.query(Category).all()
    books = Session.query(Book).all()
    book_count = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(book_count)
    return render_template('book.html', categories = categories, books = books, number=count_cart) 

@app.route("/edit_books")
def edit_books ():
    users = Session.query(User).all()
    categories = Session.query(Category).all()
    user_id = session['user_id']
    book_count = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(book_count)
    return render_template('edit_books.html', categories = categories, users=users, number = count_cart) 


@app.route('/categories')
def categories():
    user_id = session['user_id'] 
    users = Session.query(User).all()
    categories = Session.query(Category).all()
    book_count = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(book_count)
    return render_template('categories.html', categories = categories, users=users, number=count_cart)


@app.route('/delete_kategoriju/<int:ID_category>', methods=['POST'])
def delete_category(ID_category):
    category = Session.query(Category).get(ID_category)
    
    Session.delete(category)
    Session.commit()  
        
    return redirect(url_for('categories'))


@app.route("/registerUser", methods = ['POST'])
def regUser():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    password = request.form['password']

    user = User(firstName = firstName, lastName = lastName, email = email, password = password)
    Session.add(user)
    Session.commit()

    flash('User successfully registered', 'success')
    return redirect(url_for('index'))


@app.route('/loginUser', methods=['GET', 'POST'])
def log_user():
   
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Session.query(User).filter_by(email=email, password=password).first()
       
        if user:
            session['user_name'] = user.firstName
            session['user_id'] = user.ID_user
           
            return redirect(url_for('book'))
        else:
            flash('Login failed.', 'danger')
            return redirect(url_for('index'))
        

@app.route('/logout')
def logout():
    
    session.pop('user_name', None)
   
    return redirect(url_for('index'))


@app.route('/add-category', methods=['POST'])
def addCategory():
    user_id = session['user_id'] 
    name = request.form['name']
    description = request.form['description']
    category = Category(name=name, description=description, user_id=user_id)
    Session.add(category)
    Session.commit()

   
    return redirect(url_for('categories'))


@app.route('/add-book', methods=['POST'])
def add_book():
    name = request.form['name']
    author = request.form['author']
    year = request.form['year']
    description = request.form['description']
    category_id = request.form['category_id']
    price = request.form['price']
    user_id = session['user_id'] 
    try:
        image = request.files['filename']
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('book'))

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        flash('Book added successfully!', 'success')
    else:
        flash('Invalid file format for image!', 'error')
        return redirect(url_for('book'))

    book = Book(name=name, author=author, year = year, user_id=user_id, description=description, category_id=category_id, price=price, image=filename)
    Session.add(book)
    Session.commit()

    return redirect(url_for('edit_books'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/delete_book/<int:ID_book>', methods=['POST'])
def delete_book(ID_book):
    book = Session.query(Book).get(ID_book)
    
    Session.delete(book)
    Session.commit()  
        
    return redirect(url_for('book'))


@app.route('/edit/<int:ID_book>')
def edit(ID_book):
    user_id = session['user_id']
    books = Session.query(Book).get(ID_book)
    categories = Session.query(Category).all()
    book_count = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(book_count)
    return render_template('edit.html', books=books, categories=categories, number = count_cart) 

@app.route('/book_edit/<int:ID_book>', methods=['POST'])
def book_edit(ID_book):
    book = Session.query(Book).get(ID_book)
    
    if book:
        book.name = request.form.get('name')
        book.description = request.form.get('description')
        book.price = request.form.get('price')
        book.category_id = request.form.get('category_id')
        book.author = request.form.get('author')
        book.year = request.form.get('year')

        if 'filename' in request.files:
            image = request.files['filename']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                book.image = filename
           

        try:
            Session.commit()
            flash('Book updated successfully!', 'success')
        except Exception as e:
            Session.rollback()
            
        finally:
            Session.close()

    return redirect(url_for('edit_books'))

@app.route('/add_cart/<int:ID_book>', methods=['POST'])
def add_cart(ID_book):
    category_id = Session.query(Book).get(ID_book).category_id
    user_id = session['user_id']
    exist = Session.query(Cart).filter_by(book_id=ID_book, user_id=user_id, category_id = category_id).first()
    if exist:
        flash('This book is already in the cart.  ', 'danger')
        return redirect(url_for('book'))
    else:
        user_id = session['user_id']
        cart = Cart(book_id=ID_book, user_id=user_id, category_id = category_id)
        Session.add(cart)
        Session.commit()
    
    
    return redirect(url_for('book'))

@app.route("/cart")
def cart():
    user_id = session['user_id']  
    book = Session.query(Book).all()
    user = Session.query(User).all()
    categories = Session.query(Category).all()
    book_count = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(book_count)
    return render_template('cart.html', cart=book_count, number = count_cart,books=book, users=user,categories=categories)


@app.route('/remove_cart/<int:ID_cart>', methods=['POST'])
def remove_cart(ID_cart):
    cart = Session.query(Cart).get(ID_cart)
    
    Session.delete(cart)
    Session.commit()  
        
    return redirect(url_for('cart'))



  
@app.route("/search_book", methods=["GET"])
def search_book():
   
    user_id = session['user_id']   
    book_name = request.args.get("book_name")
    
    number = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(number)
  
    books = Session.query(Book).filter(Book.name.ilike(f"%{book_name}%")).all()
    return render_template("search.html", books=books, number=count_cart)
   

   
 

app.debug = True

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5001)