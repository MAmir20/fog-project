from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulated data store for temperature and fan status from multiple nodes
data_store = {
    "Living Room": {"temperature": None, "fan_status": "Unknown"},
    "Bedroom": {"temperature": None, "fan_status": "Unknown"}
}

@app.route('/')
def index():
    return render_template('index.html', data=data_store)

# Route to provide the data for the AJAX requests
@app.route('/get_data')
def get_data():
    return jsonify(data_store)

@app.route('/update', methods=['POST'])
def update():
    # Receiving updates from fog nodes
    room = request.form.get('room')
    temperature = request.form.get('temperature')
    fan_status = request.form.get('fan_status')
    
    if room in data_store:
        data_store[room]['temperature'] = temperature
        data_store[room]['fan_status'] = fan_status
    else:
        data_store[room] = {"temperature": temperature, "fan_status": fan_status}
    
    return "Update received", 200

if __name__ == "__main__":
    app.run(debug=True)
