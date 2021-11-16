from flask import Flask, render_template, request, redirect, url_for, session, Response
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

#setting up DB
client = MongoClient()
db = client.CharityTracker
users = db.users
donations = db.donations

app = Flask(__name__)
app.secret_key = '9a5c0aaf287745d3b21371fb097bb5a22e6da0e9c8fb3bc39e34474f2f400f57'



#landing page
@app.route('/')
def index():
    """Landing page (index.html)"""
    return render_template('index.html')

# ————————————————————————————————————————————————————————————————————————
"""USER INFO"""
#takes username from form and lodges into session
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        session['username']=request.form['username']
        return render_template('dashboard.html')
    elif request.method=='POST':
        user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
        }
        user = users.insert_one(user)
        session['username']=request.form['username']
        print(user)
        user_obj = users.find_one({'username': session['username']})
        return render_template('dashboard.html', user_obj=user_obj, user=user_obj)

#logout removes username from session, returns to index
@app.route('/logout')
def logout():
    session['username']=None
    return redirect(url_for('index'))

# ————————————————————————————————————————————————————————————————————————
@app.route('/dashboard')
def dashboard():
    user_obj = users.find_one({'username': session['username']})
    return render_template('dashboard.html', user_obj=user_obj, user=user_obj)

# ————————————————————————————————————————————————————————————————————————
"""USER CRUD"""
@app.route('/user')
def user_settings():
    """View user settings"""
    user_obj = users.find_one({'username': session['username']})
    return render_template('user.html', user_obj=user_obj, user=user_obj)

@app.route('/user/<user_id>/edit')
def user_edit(user_id):
    user=users.find_one({'_id': ObjectId(user_id)})
    return render_template('user_edit.html', user=user)

@app.route('/user/<user_id>/update', methods=['POST'])
def user_update(user_id):
    user_obj = users.find_one({'username': session['username']})
    updated_user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
        }
    users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_user}
    )
    session['username']=request.form['username']
    return redirect(url_for('user_settings', user=user_obj, user_obj=user_obj))

@app.route('/user/<user_id>/delete')
def user_delete(user_id):
    users.delete_one({'_id': ObjectId(user_id)})
    print({'_id': ObjectId(user_id)})
    session['username']=None
    return redirect(url_for('index'))

# ————————————————————————————————————————————————————————————————————————

"""DONATIONS"""
@app.route('/donations/<user_id>')
def donations_index(user_id):
    """Show all donations for user"""
    donation = donations.find({'_id': ObjectId(user_id)})
    user_obj = users.find_one({'username': session['username']})
    # print(list(donations.find()))
    return render_template('donations_index.html', donations=donation, user_obj=user_obj)

@app.route('/donations/new')
def donations_new():
    user_obj = users.find_one({'username': session['username']})
    """Create new donation"""
    return render_template('donations_new.html', donation={}, title='New Donation', user_obj=user_obj, user=user_obj)

@app.route('/donations/<user_id>', methods=['POST'])
def submit_donation():
    """Submit a new donation"""
    user_obj = users.find_one({'username': session['username']})
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    donation = {
        'obj_id': request.form.get('user_obj_id'),
        'charity': request.form.get('charity'),
        'donation_amnt': request.form.get('donation-amnt'),
        'created_at': dt_string
    }
    print(request.form.to_dict())
    donations.insert_one(donation)
    return redirect(url_for('donations_index', user_obj=user_obj, user=user_obj))

@app.route('/donations/<donation_id>/edit')
def donations_edit(donation_id):
    """Edit a donation"""
    donation=donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_edit.html', donation=donation, title='Edit Donation')

@app.route('/donations/<donation_id>/update', methods=['POST'])
def donations_update(donation_id):
    """Submit edited donation"""
    user_obj = users.find_one({'username': session['username']})
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    updated_donation = {
        'username': user_obj.get('username'),
        'charity': request.form.get('charity'),
        'donation_amnt': request.form.get('donation-amnt'),
        'created_at': dt_string
    }
    donations.update_one(
        {'_id': ObjectId(donation_id)},
        {'$set': updated_donation}
    )
    
    return redirect(url_for('donations_index', donation_id=donation_id, user_obj=user_obj))

@app.route('/donations/<donation_id>/delete', methods=['POST'])
def donations_delete(donation_id):
    """Delete a playlist"""
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('donations_index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)