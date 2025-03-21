import paho.mqtt.client as mqtt


# 定义回调函数，当连接成功时调用
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅主题
    client.subscribe("sd")


# 定义回调函数，当接收到消息时调用
def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")


# 创建 MQTT 客户端实例
client = mqtt.Client()

# 设置连接成功和接收到消息时的回调函数
client.on_connect = on_connect
client.on_message = on_message

# 连接到 MQTT Broker
try:
    client.connect("10.200.10.219", 1883, 60)
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
else:
    # 开始循环处理网络流量
    client.loop_forever()
