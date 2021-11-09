from flask import Flask, render_template, request, redirect, url_for, session, g
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from user.models import User


client = MongoClient()
db = client.CharityTracker
# class User:
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def __repr__(self):
#         return f'<User: {self.username}>'

users = db.users
user1 = {
    'id': '1',
    'username': 'Malia',
    'password': 'password'
}
user2 = {
    'id': '2',
    'username': 'Luke',
    'password': 'secret'
}
users.insert_one(user1)
users.insert_one(user2)


donations = db.donations


app = Flask(__name__)
app.secret_key = '9a5c0aaf287745d3b21371fb097bb5a22e6da0e9c8fb3bc39e34474f2f400f57'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [user for user in list(users) if user.id == session['user_id']][0]
        g.user = user

@app.route('/')
def index():
    """Landing page (index.html)"""
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            print(user.id)
            return redirect(url_for('dashboard'))

        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# @app.route('/signup', methods=['GET'])
# def signup():
#     return User().signup()

# ————————————————————————————————————————————————————————————————————————

@app.route('/dashboard/<user_id>')
def home(user_id):
    """Home page (home.html) Show a single user"""
    user = users.find_one({'_id': ObjectId(user_id)})
    print(user)
    return render_template('home.html', user=user)

@app.route('/dashboard', methods=['POST'])
def user_submit():
    """Submit a new user"""
    user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }
    user = users.insert_one(user)
    print(user)
    print(request.form.to_dict())
    return redirect(url_for('home'))

# ————————————————————————————————————————————————————————————————————————

@app.route('/user/donations')
def donations_index():
    """Show all donations"""
    return render_template('donations_index.html', donations=donations.find())

@app.route('/user/donations/new')
def donations_new():
    """Create new donation"""
    return render_template('donations_new.html', donation={}, title='New Donation')

@app.route('/user/donations', methods=['POST'])
def submit_donation():
    """Submit a new donation"""
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    donation = {
        'user_id': request.form.get('user_id'),
        'charity': request.form.get('charity'),
        'donation_amnt': request.form.get('donation-amnt'),
        'created_at': dt_string
    }
    print(request.form.to_dict())
    donations.insert_one(donation)
    return redirect(url_for('donations_index', user_id=request.form.get('user_id')))

if __name__ == '__main__':
    app.run(debug=True)