import network
import urequests
import time

# Replace with your WiFi credentials
WIFI_SSID = "ArpaE"
WIFI_PASSWORD = "ArpaE2019"

# Raspberry Pi IP address
PI_IP = "192.168.1.50:5000"

# Button pin 
BUTTON_PIN = 18

# Function to handle button presses
def button_pressed(pin):
    # Get current time
    from time import time
    timestamp = time()

    # Prepare data to send
    data = {"timestamp": timestamp}
    gc.enable()

    # Send POST request to Raspberry Pi
    try:
        url = "http://" + PI_IP + "/button_press"
        response = urequests.post(url, json=data)
        gc.collect()
        print(f"Button press sent: {response.text}")
    except Exception as e:
        print(f"Error sending button press: {e}")

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for connection
while not wlan.isconnected():
    pass

print("Connected to WiFi")

# Configure button interrupt
from machine import Pin
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# Main loop
print("Waiting for button press...")
while True:
    pass
