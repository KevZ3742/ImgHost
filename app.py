# app.py

from flask import Flask, request, render_template, Response
import sqlite3

app = Flask(__name__)

# Create SQLite database and table
conn = sqlite3.connect('images.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM images')
    # Fetch list of uploaded image ids
    image_list = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', image_list=image_list)

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image'].read()

    if not image:
        return "The selected image file is empty."

    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO images (image) VALUES (?)', (sqlite3.Binary(image),))
    conn.commit()
    conn.close()

    return "Image uploaded and saved to the database."

@app.route('/view/<int:image_id>')
def view_image(image_id):
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute('SELECT image FROM images WHERE id = ?', (image_id,))
    image_data = cursor.fetchone()
    conn.close()

    if image_data:
        image_binary = image_data[0]
        return Response(image_binary, content_type="image/jpeg")

    return "Image not found."

if __name__ == '__main__':
    app.run()
