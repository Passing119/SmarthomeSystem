import paho.mqtt.client as mqtt

# MQTT 代理信息
MQTT_BROKER = "broker.hivemq.com"  # 公共 MQTT 服务器
MQTT_PORT = 1883  # MQTT 默认端口
TOPICS = [
    ("smart_ac/temperature", 0),  # 订阅温度传感器数据
    ("smart_ac/humidity", 0),  # 订阅湿度传感器数据
    ("smart_ac/power", 0),  # 订阅空调开关控制
    ("smart_ac/set_temperature", 0)  # 订阅温度设定控制
]

# 连接成功回调
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ 连接到 MQTT 服务器成功！")
        for topic in TOPICS:
            client.subscribe(topic)  # 订阅多个主题
            print(f"📡 订阅主题: {topic[0]}")
    else:
        print(f"❌ 连接失败，错误码：{rc}")

# 收到消息时的回调
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"📩 收到消息 - 主题: {msg.topic}, 内容: {payload}")

    # 控制空调电源
    if msg.topic == "smart_ac/power":
        if payload.lower() == "on":
            print("🌡 开启空调")
        elif payload.lower() == "off":
            print("❄ 关闭空调")

    # 设定空调温度
    elif msg.topic == "smart_ac/set_temperature":
        try:
            temp = float(payload)
            print(f"🔧 设置空调温度为 {temp}°C")
        except ValueError:
            print("⚠ 无效的温度设置")

# 创建 MQTT 客户端
client = mqtt.Client()

# 绑定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 连接到 MQTT 服务器
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 持续监听消息
client.loop_forever()