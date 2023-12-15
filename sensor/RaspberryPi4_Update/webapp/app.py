from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    conn = sqlite3.connect("timestamps.db")
    return conn

# Define the database schema (within app.py)
def create_schema():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timestamps (
                timestamp REAL PRIMARY KEY
            );
        """)
        conn.commit()

# Create the schema if it doesn't exist (run only once)
create_schema()

# Route for handling button press
@app.route('/button_press', methods=['GET', 'POST'])
def button_press():
    if request.method == 'GET':
        return render_template('button_press.html')
    elif request.method == 'POST':
        timestamp = request.form['timestamp']
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO timestamps VALUES (?)", (timestamp,))
            conn.commit()
        return render_template('button_press.html', success_message="Button press recorded successfully!")

# Route for displaying button press history
@app.route('/button_press_data')
def button_press_data():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp FROM timestamps")
        timestamps = cursor.fetchall()
    return render_template('button_press_data.html', timestamps=timestamps)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')