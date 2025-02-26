from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid
import secrets
import json
import os
import atexit

app = Flask(__name__)

# File to store polls data
POLLS_FILE = 'polls_data.json'
ADMIN_TOKENS_FILE = 'admin_tokens.json'

# Data structure to store polls
polls = {}
# Map admin tokens to poll IDs for security
admin_tokens = {}

# Load data from files if they exist
def load_data():
    global polls, admin_tokens
    try:
        if os.path.exists(POLLS_FILE):
            with open(POLLS_FILE, 'r') as f:
                polls = json.load(f)
        if os.path.exists(ADMIN_TOKENS_FILE):
            with open(ADMIN_TOKENS_FILE, 'r') as f:
                admin_tokens = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")

# Save data to files
def save_data():
    try:
        with open(POLLS_FILE, 'w') as f:
            json.dump(polls, f, indent=2)
        with open(ADMIN_TOKENS_FILE, 'w') as f:
            json.dump(admin_tokens, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

# Register save_data to run when the application exits
atexit.register(save_data)

# Load data at startup
load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_poll', methods=['POST'])
def create_poll():
    poll_id = str(uuid.uuid4())
    # Generate a secure admin token that can't be guessed
    admin_token = secrets.token_urlsafe(16)
    admin_tokens[admin_token] = poll_id
    
    admin_link = url_for('admin_poll', token=admin_token)
    user_link = url_for('user_poll', poll_id=poll_id)
    
    polls[poll_id] = {'dates': {}, 'admin_link': admin_link, 'user_link': user_link}
    
    # Save data after creating a new poll
    save_data()
    
    return jsonify(admin_link=admin_link, user_link=user_link)

@app.route('/admin/<token>', methods=['GET', 'POST'])
def admin_poll(token):
    if token not in admin_tokens:
        return redirect(url_for('index'))
    
    poll_id = admin_tokens[token]
        
    if request.method == 'POST':
        data = request.get_json()
        date = data.get('date')
        time = data.get('time')
        if date and time:
            if 'dates' not in polls[poll_id]:
                polls[poll_id]['dates'] = {}
            if date not in polls[poll_id]['dates']:
                polls[poll_id]['dates'][date] = {}
            polls[poll_id]['dates'][date][time] = {'yes': 0, 'no': 0, 'maybe': 0}
            
            # Save data after adding a time slot
            save_data()
            
            return jsonify(success=True, message="Time slot added successfully!")
        else:
            return jsonify(success=False, message="Invalid input"), 400
    
    if request.headers.get('Content-Type') == 'application/json' or request.headers.get('Accept') == 'application/json':
        return jsonify(polls[poll_id])
    return render_template('admin_poll.html')

@app.route('/user/<poll_id>', methods=['GET', 'POST'])
def user_poll(poll_id):
    if poll_id not in polls:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        data = request.get_json()
        date = data.get('date')
        time = data.get('time')
        vote = data.get('vote')
        if date in polls[poll_id]['dates'] and time in polls[poll_id]['dates'][date]:
            vote_key = vote.lower()  # Convert to lowercase to match our data structure
            polls[poll_id]['dates'][date][time][vote_key] += 1
            
            # Save data after recording a vote
            save_data()
            
            return jsonify(success=True, message="Vote recorded successfully!")
        else:
            return jsonify(success=False, message="Invalid date or time"), 400
    
    if request.headers.get('Content-Type') == 'application/json' or request.headers.get('Accept') == 'application/json':
        return jsonify(polls[poll_id])
    return render_template('user_poll.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
