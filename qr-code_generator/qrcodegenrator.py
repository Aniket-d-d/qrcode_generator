from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
import random
import string
import sqlite3
'''
conn = sqlite3.connect('links.db')
conn.execute('CREATE TABLE URL(LINKES TEXT, name TEXT)')
conn.close()
'''
PEOPLE_FOLDER = os.path.join('static')
letters = string.ascii_letters

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def student():
    return render_template('main_page01.html')


@app.route('/qrcodes',methods = ['POST', 'GET'])
def qrcodes():
    if request.method == 'POST':
        input_url = request.form['url']

        with sqlite3.connect("links.db") as conn:
            conn.cursor()

            image_name = f"{''.join(random.choice(letters) for i in range(26))}.png"
            img = qrcode.make(input_url)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
            image = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

            conn.execute('INSERT INTO URL(LINKES, NAME) VALUES (?, ?)', (input_url, image_name))
            conn.commit()

            return render_template("qrcode.html", image=image)


@app.route('/download')
def download():
    conn = sqlite3.connect('links.db')
    cursor = conn.execute("SELECT NAME from URL")
    for row in cursor:
        names = row
    names = str(names).replace(",", "")
    names = names.replace("'", "")
    names = names.replace("(", "")
    names = names.replace(")", "")
    print(names)

    return send_from_directory(app.config['UPLOAD_FOLDER'], names, as_attachment=True)


if __name__ == '__main__':
    app.run(debug = True)

conn.close()