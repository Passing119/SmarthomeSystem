import paho.mqtt.client as mqtt
import time
import random
import threading

# MQTT Broker配置
BROKER_ADDRESS = "172.24.22.9"  # 替换为你的MQTT Broker地址
PORT = 1883  # 通常MQTT默认端口
USERNAME = "Team2"  # 替换为你的用户名
PASSWORD = "123456"  # 替换为你的密码

# 空调状态
aircon_state = {
    "power": "off",
    "temperature": 25,
    "fan_speed": "medium",
    "fan_direction": "medium"
}

# 创建MQTT客户端
subscriber = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "AirConSubscriber")
subscriber.username_pw_set(USERNAME, PASSWORD)

# 设置TLS加密（如果需要）
# subscriber.tls_set()  # 取消注释以启用TLS
# subscriber.tls_insecure_set(True)  # 如果需要忽略证书验证

last_temperature_print_time = 0  # 用于记录上次打印温度的时间

def on_connect_subscriber(client, userdata, flags, rc, properties=None):
    if rc == 0:
        # 订阅所有相关主题
        client.subscribe("aircon/control/#")
        client.subscribe("aircon/mode/#")
        client.subscribe("aircon/sensor/temperature")  # 订阅温度主题
    else:
        print(f"Subscriber failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global last_temperature_print_time
    topic = msg.topic
    payload = msg.payload.decode()

    # 处理控制命令
    if topic == "aircon/control/power":
        aircon_state["power"] = payload
    elif topic == "aircon/control/temperature":
        try:
            temp = int(payload)
            if 16 <= temp <= 30:
                aircon_state["temperature"] = temp
        except ValueError:
            pass
    elif topic == "aircon/control/fan_speed":
        if payload in ["big", "medium", "small"]:
            aircon_state["fan_speed"] = payload
    elif topic == "aircon/control/fan_direction":
        if payload in ["left", "medium", "right"]:
            aircon_state["fan_direction"] = payload

    # 处理模式命令
    elif topic == "aircon/mode/cold":
        aircon_state.update({
            "power": "on",
            "temperature": 25,
            "fan_speed": "big",
            "fan_direction": "medium"
        })
    elif topic == "aircon/mode/hot":
        aircon_state.update({
            "power": "on",
            "temperature": 28,
            "fan_speed": "big",
            "fan_direction": "medium"
        })
    elif topic == "aircon/mode/constant":
        aircon_state.update({
            "power": "on",
            "temperature": 26,
            "fan_speed": "small",
            "fan_direction": "medium"
        })

    # 处理温度数据
    elif topic == "aircon/sensor/temperature":
        try:
            temp = float(payload)
            current_time = time.time()
            # 每5秒打印一次温度数据
            if current_time - last_temperature_print_time >= 5:
                print(f"Received temperature data: {temp}°C")
                last_temperature_print_time = current_time
        except ValueError:
            pass

subscriber.on_connect = on_connect_subscriber
subscriber.on_message = on_message

def simulate_temperature_publisher():
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, PORT)
    while True:
        temperature = round(random.uniform(16.0, 30.0), 1)
        client.publish("aircon/sensor/temperature", str(temperature))
        time.sleep(5)  # 每5秒发布一次温度数据

# 连接到MQTT Broker
subscriber.connect(BROKER_ADDRESS, PORT)

# 启动温度模拟发布线程
temperature_thread = threading.Thread(target=simulate_temperature_publisher)
temperature_thread.daemon = True
temperature_thread.start()

try:
    print("Subscriber started, waiting for commands...")
    subscriber.loop_forever()
except KeyboardInterrupt:
    print("Subscriber exiting...")
    subscriber.disconnect()