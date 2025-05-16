from flask import Flask, render_template, request, redirect
import sqlite3
from weather import get_weather

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('crop_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('crop_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM crops")
    crops = c.fetchall()
    conn.close()
    return render_template('index.html', crops=crops)

@app.route('/add', methods=['GET', 'POST'])
def add_crop():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        status = request.form['status']

        conn = sqlite3.connect('crop_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO crops (name, location, status) VALUES (?, ?, ?)", (name, location, status))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_crop.html')

@app.route('/weather/<city>')
def weather(city):
    weather_data = get_weather(city)
    return weather_data or {"error": "City not found"}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
