import paho.mqtt.client as mqtt
import time

# MQTT Configuration
BROKER = "172.24.23.109"
PORT = 1883
USERNAME = "Team2"
PASSWORD = "123456"
TOPIC = "lock/control"
CLIENT_ID = "door_lock_publisher"

# MQTT connection callback
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker successfully")
    else:
        print(f"Connection failed with code: {rc}")

# Create MQTT client (using correct API version)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

# Connect to MQTT Broker
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
    exit(1)

# Command publishing loop
try:
    while True:
        command = input("Enter command (1 = unlock door, 0 = lock door, q = quit): ").strip()
        if command.lower() == 'q':
            break
        elif command in ['0', '1']:
            client.publish(TOPIC, command, qos=1)
            print(f"Sent command: {'Unlock door' if command == '1' else 'Lock door'}")
        else:
            print("Invalid input. Please enter 0, 1, or q.")

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")

finally:
    client.disconnect()
    client.loop_stop()
