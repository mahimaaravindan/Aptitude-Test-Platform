from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector
from mysql.connector import Error
import random

app = Flask(__name__)
app.secret_key = 'e7f243acbcf64f5a9b6c2f4b2eaf25d4'  # Change this to a secure key

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='college_db',
            user='mahi',  # Replace with your MySQL username
            password='12345'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_login_entry(username):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO login_entries (username) VALUES (%s)", (username,))
            connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def get_questions():
    # Ideally, you would retrieve questions from a database or file
    return [
        {"question": "What is 2 + 2?", "options": ["3", "4", "5"], "answer": "4"},
        {"question": "What is 5 * 3?", "options": ["15", "10", "20"], "answer": "15"},
        # Add more questions as needed
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                insert_login_entry(username)
                session['username'] = username
                return redirect(url_for('aptitude_test'))
            else:
                return "Invalid username or password"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/aptitude_test', methods=['GET', 'POST'])
def aptitude_test():
    questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Madrid']
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6']
    },
    {
        'question': 'What is the color of the sky?',
        'options': ['Blue', 'Red', 'Green', 'Yellow']
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html', questions=questions)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    answers = []
    for i in range(len(questions)):
        selected_option = request.form.get(f'q{i}')
        answers.append(selected_option)
    flash(f'Your answers: {answers}')
    return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    return "Welcome to KSIT"

@app.errorhandler(404)
def invalid_route(e):
    return "Invalid route.", 404

if __name__ == '__main__':
    app.run(debug=True)
