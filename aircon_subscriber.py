import paho.mqtt.client as mqtt
import time

# MQTT Broker配置
BROKER_ADDRESS = "10.200.10.219"  # 替换为你的MQTT Broker地址
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

def on_connect_subscriber(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber connected to MQTT Broker!")
        # 订阅所有相关主题
        client.subscribe("aircon/control/#")
        client.subscribe("aircon/mode/#")
    else:
        print(f"Subscriber failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\nReceived message on {topic}: {payload}")

    # 处理控制命令
    if topic == "aircon/control/power":
        aircon_state["power"] = payload
        print(f"The air conditioner power supply has been set to: {payload}")

    elif topic == "aircon/control/temperature":
        try:
            temp = int(payload)
            if 16 <= temp <= 30:
                aircon_state["temperature"] = temp
                print(f"The temperature has been set to: {temp}°C")
            else:
                print("Temperature value out of range(16-30)")
        except ValueError:
            print("Invalid temperature value")

    elif topic == "aircon/control/fan_speed":
        if payload in ["big", "medium", "small"]:
            aircon_state["fan_speed"] = payload
            print(f"The wind speed has been set to: {payload}")
        else:
            print("Invalid wind speed setting")

    elif topic == "aircon/control/fan_direction":
        if payload in ["left", "medium", "right"]:
            aircon_state["fan_direction"] = payload
            print(f"The wind direction has been set to: {payload}")
        else:
            print("Invalid wind direction setting")

    # 处理模式命令
    elif topic == "aircon/mode/cold":
        aircon_state.update({
            "power": "on",
            "temperature": 25,
            "fan_speed": "big",
            "fan_direction": "medium"
        })
        print("Cooling mode has been set: open, 25°C, fan_speed:big,fan_direction:medium ")

    elif topic == "aircon/mode/hot":
        aircon_state.update({
            "power": "on",
            "temperature": 28,
            "fan_speed": "big",
            "fan_direction": "medium"
        })
        print("Set to heating mode: open, 28°C,fan_speed:big,fan_direction:medium ")

    elif topic == "aircon/mode/constant":
        aircon_state.update({
            "power": "on",
            "temperature": 26,
            "fan_speed": "small",
            "fan_direction": "medium"
        })
        print("Set to constant temperature mode: open, 26°C, fan_speed:small, fan_direction:medium")

    # 打印当前状态
    print("\nCurrent air conditioning status:")
    for key, value in aircon_state.items():
        print(f"{key}: {value}")


subscriber.on_connect = on_connect_subscriber
subscriber.on_message = on_message

# 连接到MQTT Broker
subscriber.connect(BROKER_ADDRESS, PORT)

try:
    print("Subscriber started, waiting for commands...")
    subscriber.loop_forever()
except KeyboardInterrupt:
    print("Subscriber exiting...")
    subscriber.disconnect()

'''
使用说明
将两个代码分别保存为 aircon_publisher.py 和 aircon_subscriber.py

替换代码中的 your_broker_address, your_username 和 your_password 为你的MQTT Broker的实际信息

如果需要TLS加密，取消注释相关代码行

先运行subscriber代码，然后运行publisher代码发送控制命令

功能说明
Publisher:

可以发送空调的各种控制命令（开关、温度、风速、风向）

可以一键设置三种模式（制冷、制热、恒温）

提供简单的命令行交互界面

Subscriber:

订阅所有空调控制主题

接收并处理控制命令

维护空调的当前状态

打印接收到的命令和当前状态

安全设置:

包含用户名和密码认证

包含TLS加密的选项（根据需要取消注释）

注意：实际使用时，你可能需要根据你的MQTT Broker的具体配置调整连接参数和安全设置。
'''