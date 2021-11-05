from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.CharityTracker
users = db.users
donations = db.donations

app = Flask(__name__)


@app.route('/')
def index():
    """Landing page (index.html)"""
    return render_template('index.html')

# ————————————————————————————————————————————————————————————————————————

@app.route('/home')
def home():
    """Home page (home.html)"""
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def user_submit():
    """Submit a new user"""
    user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }
    users.insert_one(user)
    print(request.form.to_dict())
    return redirect(url_for('home'))

# ————————————————————————————————————————————————————————————————————————

@app.route('/donations')
def donations_index():
    """Show all donations"""
    return render_template('donations_index.html', donations=donations.find())

@app.route('/donations/new')
def donations_new():
    """Create new donation"""
    return render_template('donations_new.html', donation={}, title='New Donation')

@app.route('/donations', methods=['POST'])
def submit_donation():
    """Submit a new donation"""
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    donation = {
        'charity': request.form.get('charity'),
        'donation_amnt': request.form.get('donation-amnt'),
        'created_at': dt_string
    }
    print(request.form.to_dict())
    donations.insert_one(donation)
    return redirect(url_for('donations_index'))

if __name__ == '__main__':
    app.run(debug=True)