from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.CharityTracker
users = db.users
donations = db.donations

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def user_submit():
    """Submit a new user"""
    user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }
    user.insert_one(users)
    print(request.form.to_dict())
    return redirect(url_for('home'))

users = [
    { 'username': 'malia123', 'password': 'ilovedogs'},
    { 'username': 'beepboop', 'password': 'ilovecats'}
]

@app.route('/donations')
def donations_index():
    """Show all donations"""
    return render_template('donations_index.html', donations=donations.find())

if __name__ == '__main__':
    app.run(debug=True)