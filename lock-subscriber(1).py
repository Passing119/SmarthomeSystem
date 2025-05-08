import paho.mqtt.client as mqtt
import time
import cv2
from playsound import playsound
import threading

# MQTT Configuration
BROKER = "172.24.23.109"
PORT = 1883
TOPIC = "lock/control"
CLIENT_ID = "door_lock_controller"

# Current door lock state
door_locked = True  # Initial state: locked

# MQTT connection callback
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker successfully")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Connection failed with code: {rc}")

# MQTT message callback
def on_message(client, userdata, msg):
    global door_locked
    command = msg.payload.decode()

    if command == '1':
        door_locked = False
        print("Door is now unlocked")
    elif command == '0':
        door_locked = True
        print("Door is now locked")
    else:
        print(f"Unknown command: {command}")

# Video monitoring thread function
def monitor_video():
    cap = cv2.VideoCapture(0)  # Use default camera
    time.sleep(2)  # Wait for camera to stabilize
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    if not ret:
        print("Failed to access the camera")
        return

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            print("Motion detected in video feed")
            threading.Thread(target=playsound, args=("alarm.mp3",), daemon=True).start()

        frame1 = frame2
        ret, frame2 = cap.read()

        # Display video frame (optional)
        cv2.imshow("Live Monitoring", frame2)
        if cv2.waitKey(10) == 27:  # ESC key to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

# Main program
try:
    client.connect(BROKER, PORT, 60)
    print("Waiting for commands...")
    print(f"Initial door state: {'Locked' if door_locked else 'Unlocked'}")

    # Start monitoring thread
    threading.Thread(target=monitor_video, daemon=True).start()

    # Start MQTT loop
    client.loop_forever()

except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
finally:
    client.disconnect()
