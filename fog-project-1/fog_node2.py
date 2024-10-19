import random
import time
import requests

# Simulate temperature readings
def get_temperature():
    return round(random.uniform(15, 30), 2)

def control_fan(temperature):
    if temperature > 25:
        return "Fan ON"
    elif temperature < 20:
        return "Fan OFF"
    else:
        return "Fan OFF (Idle)"

def send_data_to_flask(room, temperature, fan_status):
    url = "http://localhost:5000/update"
    data = {
        "room": room,
        "temperature": temperature,
        "fan_status": fan_status
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Data successfully sent to Flask for {room}")
        else:
            print(f"Failed to send data to Flask: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    room_name = "Bedroom"  # Change this for each fog node (e.g., "Bedroom")
    
    while True:
        temperature = get_temperature()
        fan_status = control_fan(temperature)
        
        print(f"Room: {room_name} | Temperature: {temperature}°C | {fan_status}")
        
        # Send data to Flask app
        send_data_to_flask(room_name, temperature, fan_status)
        
        time.sleep(5)
