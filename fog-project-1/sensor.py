import random
import time

def get_temperature():
    # Simulates temperature sensor data (random value between 15°C and 30°C)
    return round(random.uniform(15, 30), 2)

if __name__ == "__main__":
    while True:
        temperature = get_temperature()
        print(f"Temperature: {temperature}°C")
        time.sleep(5)  # Wait 5 seconds before generating next reading
