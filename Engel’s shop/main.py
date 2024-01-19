from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
import sqlite3
import uuid
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = sqlite3.connect('products.db')
cursor = db.cursor()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    db = sqlite3.connect('products.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    db.close()

    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'GET':
        return render_template('add_products.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        photo1 = request.form.get('photo1')
        photo2 = request.form.get('photo2')
        photo3 = request.form.get('photo3')

        # Сохранение данных в базе данных
        db = sqlite3.connect('products.db')
        cursor = db.cursor()

        cursor.execute('''
            INSERT INTO products (name, description, price, photo1, photo2, photo3)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, photo1, photo2, photo3))

        db.commit()
        db.close()

        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)