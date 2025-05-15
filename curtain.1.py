import paho.mqtt.client as mqtt
import time

# MQTT服务器地址
MQTT_BROKER = "broker.hivemq.com"  # 使用公共MQTT服务器
MQTT_PORT = 1883
# 窗帘控制主题
CURTAIN_TOPIC = "smart_home/curtain/control"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def send_command(command):
    client.publish(CURTAIN_TOPIC, command)

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

while True:
    command = input("请输入命令（open/close/stop）：")
    if command in ["open", "close", "stop"]:
        send_command(command)
    else:
        print("无效命令！")
