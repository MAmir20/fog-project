from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Data for Room 1 and Room 2
room_data = {
    'room1': {'temperature': 0, 'fan_state': 'OFF'},
    'room2': {'temperature': 0, 'fan_state': 'OFF'}
}

@app.route('/')
def index():
    return render_template('index.html')

# Route to provide the data for the AJAX requests
@app.route('/get_data')
def get_data():
    return jsonify(room_data)

# Route to simulate data update for Room 1 and Room 2
@app.route('/update_data/<room_id>', methods=['GET'])
def update_data(room_id):
    if room_id in room_data:
        temperature = random.randint(20, 40)
        fan_state = 'ON' if temperature > 30 else 'OFF'
        room_data[room_id] = {'temperature': temperature, 'fan_state': fan_state}
        return jsonify(room_data[room_id])
    return jsonify({'error': 'Invalid room ID'}), 400

# Route for Node 3 to fetch data from both rooms
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    return jsonify(room_data)

if __name__ == '__main__':
    app.run(debug=True)
