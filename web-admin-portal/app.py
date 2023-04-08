from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, caregiver_phone_number TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS fall_detection
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, fall_detection_msgid TEXT)''')
    conn.commit()
    conn.close()


@app.route('/register')
def index():
    return render_template('register.html')


@app.route('/submit', methods=['POST'])
def submit():
    uuid = request.form['uuid']
    caregiver_phone_number = request.form['caregiver_phone_number']

    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO devices (uuid, caregiver_phone_number) VALUES (?, ?)', (uuid, caregiver_phone_number))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/fall_detection')
def fall_detection():
    return render_template('fall_detection.html')


@app.route('/submit_fall_detection', methods=['POST'])
def submit_fall_detection():
    uuid = request.form['uuid']
    fall_detection_msgid = request.form['fall_detection_msgid']

    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO fall_detection (uuid, fall_detection_msgid) VALUES (?, ?)',
                   (uuid, fall_detection_msgid))
    conn.commit()
    conn.close()

    return redirect(url_for('fall_detection'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
