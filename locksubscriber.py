import paho.mqtt.client as mqtt
import time
#set the MQTT information
BROKER = "172.24.23.109"
PORT = 1883
TOPIC = "lock/control"
CLIENT_ID = "door_lock_controller"

# 当前门锁状态
door_locked = True  # 初始状态为锁定 store the state of lock

# 连接回调
def on_connect(client, userdata, flags, rc,properties=None):
    if rc == 0:
        print("Link to the MQTT Broker!")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"fail: {rc}")
# 消息回调
def on_message(client, userdata, msg):
    global door_locked
    command = msg.payload.decode()

    if command == '1':
        door_locked = False
        print("door open")
    elif command == '0':
        door_locked = True
        print("door locked")
    else:
        print(f"unknown instruct: {command}")
# 创建客户端
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

# 连接Broker
try:
    client.connect(BROKER, PORT, 60)
    print("waiting for instruct...")
    print(f"initial state: {'locked' if door_locked else 'unlocked'}")
    client.loop_forever()
except Exception as e:
    print(f"fail to connect: {e}")
finally:
    client.disconnect()