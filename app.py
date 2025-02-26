from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid

app = Flask(__name__)

# Data structure to store polls
polls = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_poll', methods=['POST'])
def create_poll():
    poll_id = str(uuid.uuid4())
    admin_link = url_for('admin_poll', poll_id=poll_id)
    user_link = url_for('user_poll', poll_id=poll_id)
    polls[poll_id] = {'dates': {}, 'admin_link': admin_link, 'user_link': user_link}
    return jsonify(admin_link=admin_link, user_link=user_link)

@app.route('/admin/<poll_id>', methods=['GET', 'POST'])
def admin_poll(poll_id):
    if poll_id not in polls:
        return redirect(url_for('index'))
        
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
            polls[poll_id]['dates'][date][time][vote] += 1
            return jsonify(success=True, message="Vote recorded successfully!")
        else:
            return jsonify(success=False, message="Invalid date or time"), 400
    
    if request.headers.get('Content-Type') == 'application/json' or request.headers.get('Accept') == 'application/json':
        return jsonify(polls[poll_id])
    return render_template('user_poll.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
