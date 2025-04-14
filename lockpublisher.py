import paho.mqtt.client as mqtt
import time

#set the MQTT information
BROKER = "172.24.23.109"
PORT = 1883
USERNAME = "Team2"
PASSWORD = "123456"
TOPIC = "lock/control"
CLIENT_ID = "door_lock_controller"

# 连接回调
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Link to MQTT Broker successfully!")
    else:
        print(f"fail: {rc}")

# 创建客户端（确保正确传入 callback_api_version）
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
client.on_connect = on_connect

# 连接Broker
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"fail to connect: {e}")
    exit(1)

try:
    while True:
        command = input("enter the instruct (1:open the door, 0:lock the door, q:quit): ")
        if command.lower() == 'q':
            break
        if command in ['0', '1']:
            client.publish(TOPIC, command, qos=1)
            print(f"send the massage: {'open the door' if command == '1' else 'lock the door'}")
        else:
            print("wrong input")

except KeyboardInterrupt:
    print("stop working")
finally:
    client.disconnect()
    client.loop_stop()