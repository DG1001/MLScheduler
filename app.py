from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data to store meeting schedules
meeting_schedules = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    user = data.get('user')

    if date and time and user:
        if date not in meeting_schedules:
            meeting_schedules[date] = []
        meeting_schedules[date].append({'time': time, 'user': user})
        return jsonify(success=True, message="Meeting scheduled successfully!")
    else:
        return jsonify(success=False, message="Invalid input"), 400

@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    return jsonify(meeting_schedules)

if __name__ == '__main__':
    app.run(debug=True)
