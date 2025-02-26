from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
    data = request.get_json()
    # Here you would save the drawing data to a file or database
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
