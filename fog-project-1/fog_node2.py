import requests
import time
import random

# URL of the central server
SERVER_URL = "http://localhost:5000"

# Function to simulate temperature and fan control in Room 1
def simulate_room1():
    while True:
        # Simulate temperature between 20 and 40 degrees
        temperature = random.randint(20, 40)
        
        # Determine fan state based on the temperature
        fan_state = 'ON' if temperature > 30 else 'OFF'
        
        # Send the data to the central server
        try:
            response = requests.get(f"{SERVER_URL}/update_data/room2")
            if response.status_code == 200:
                print(f"Room 2 - Temperature: {temperature}, Fan: {fan_state}")
            else:
                print(f"Failed to update data for Room 2: {response.status_code}")
        except Exception as e:
            print(f"Error sending data for Room 2: {e}")
        
        # Wait for 5 seconds before sending the next update
        time.sleep(5)

if __name__ == "__main__":
    simulate_room1()
