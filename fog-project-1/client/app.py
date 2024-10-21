from flask import Flask, render_template, jsonify
import requests
import plotly.graph_objs as go
import time

app = Flask(__name__)

# URL of the central server Flask
SERVER_URL = "http://localhost:5000"

# Historical data for Room 1 and Room 2
room1_temperatures = []
room2_temperatures = []
room1_fan_states = []
room2_fan_states = []

@app.route('/')
def dashboard():
    return render_template('monitor_dashboard.html')

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    global room1_temperatures, room2_temperatures, room1_fan_states, room2_fan_states
    try:
        response = requests.get(f"{SERVER_URL}/get_all_data")
        if response.status_code == 200:
            data = response.json()
            # Update data for Room 1
            room1_temperatures.append(data['room1']['temperature'])
            room1_fan_states.append(data['room1']['fan_state'])
            # Update data for Room 2
            room2_temperatures.append(data['room2']['temperature'])
            room2_fan_states.append(data['room2']['fan_state'])
            return jsonify({'room1': data['room1'], 'room2': data['room2']})
        else:
            return jsonify({'error': 'Failed to fetch data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_chart_data', methods=['GET'])
def get_chart_data():
    fetch_data()
    # Prepare Room 1 data
    room1_temp_trace = go.Scatter(x=list(range(len(room1_temperatures))), y=room1_temperatures, mode='lines+markers', name='Temp Room 1')
    room1_fan_trace = go.Scatter(x=list(range(len(room1_fan_states))), y=room1_fan_states, mode='lines+markers', name='Fan Room 1')

    # Prepare Room 2 data
    room2_temp_trace = go.Scatter(x=list(range(len(room2_temperatures))), y=room2_temperatures, mode='lines+markers', name='Temp Room 2')
    room2_fan_trace = go.Scatter(x=list(range(len(room2_fan_states))), y=room2_fan_states, mode='lines+markers', name='Fan Room 2')

    # Create figures
    temp_fig = go.Figure(data=[room1_temp_trace, room2_temp_trace])
    fan_fig = go.Figure(data=[room1_fan_trace, room2_fan_trace])

    # Convert the figures to JSON for Plotly
    temp_chart = temp_fig.to_json()
    fan_chart = fan_fig.to_json()

    return jsonify({'temp_chart': temp_chart, 'fan_chart': fan_chart})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
