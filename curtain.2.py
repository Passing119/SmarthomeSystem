import paho.mqtt.client as mqtt
import time

# MQTT服务器地址
MQTT_BROKER = "broker.hivemq.com"  # 使用公共MQTT服务器
MQTT_PORT = 1883
# 窗帘控制主题
CURTAIN_TOPIC = "smart_home/curtain/control"
CURTAIN_STATUS_TOPIC = "smart_home/curtain/status"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(CURTAIN_TOPIC)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Received command: {command}")
    if command == "open":
        print("The curtains are opening...")
        time.sleep(2)  # 模拟窗帘打开时间
        print("The curtains have been opened")
        client.publish(CURTAIN_STATUS_TOPIC, "open")
    elif command == "close":
        print("The curtain is closing....")
        time.sleep(2)  # 模拟窗帘关闭时间
        print("The curtains have been closed.")
        client.publish(CURTAIN_STATUS_TOPIC, "close")
    elif command == "stop":
        print("The curtain stops moving")
        client.publish(CURTAIN_STATUS_TOPIC, "stop")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()