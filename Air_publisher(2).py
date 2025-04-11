import paho.mqtt.client as mqtt
import time
import random

# MQTT Broker配置
BROKER_ADDRESS = "172.24.22.9"  # 替换为你的MQTT Broker地址
PORT = 1883  # 通常MQTT默认端口
USERNAME = "Team2"  # 替换为你的用户名
PASSWORD = "123456"  # 替换为你的密码

# 创建MQTT客户端
publisher = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "AirConSubscriber")
publisher.username_pw_set(USERNAME, PASSWORD)


# 设置TLS加密（如果需要）
# publisher.tls_set()  # 取消注释以启用TLS
# publisher.tls_insecure_set(True)  # 如果需要忽略证书验证

def on_connect_publisher(client, userdata, flags, rc, properties=None):
    if rc != 0:
        print(f"Publisher failed to connect, return code {rc}")


publisher.on_connect = on_connect_publisher

# 连接到MQTT Broker
publisher.connect(BROKER_ADDRESS, PORT)
publisher.loop_start()


def send_control_command(topic_suffix, payload):
    topic = f"aircon/control/{topic_suffix}"
    publisher.publish(topic, payload)
    print(f"Sent command to {topic}: {payload}")


def send_mode_command(mode):
    topic = f"aircon/mode/{mode}"
    publisher.publish(topic, "1")  # 发送任意值表示触发
    print(f"Sent mode command: {topic}")


def generate_temperature_data():
    # 模拟温度数据（16.0°C - 30.0°C）
    temperature = round(random.uniform(16.0, 30.0), 1)
    return temperature


# 示例控制命令
try:
    last_temperature_print_time = 0  # 用于记录上次打印温度的时间
    while True:
        current_time = time.time()

        # 每5秒生成并打印一次随机温度
        if current_time - last_temperature_print_time >= 5:
            temperature = generate_temperature_data()
            print(f"Generated temperature: {temperature}°C")
            last_temperature_print_time = current_time

        print("\nWhat you want to do:")
        print("1. on/off")
        print("2. temperature")
        print("3. fan_speed")
        print("4. fan_direction")
        print("5. mode control")
        print("6. exit")

        choice = input("chose(1-6): ")

        if choice == "1":
            state = input("on/off: ")
            send_control_command("power", state)
        elif choice == "2":
            temp = input("temperature(16-30): ")
            send_control_command("temperature", temp)
        elif choice == "3":
            speed = input("fan_speed(big/medium/small): ")
            send_control_command("fan_speed", speed)
        elif choice == "4":
            direction = input("fan_direction(left/medium/right): ")
            send_control_command("fan_direction", direction)
        elif choice == "5":
            print("chose the mode:")
            print("1. cooling mode")
            print("2. heating mode")
            print("3. constant mode")
            mode_choice = input("enter the mode options(1-3): ")
            if mode_choice == "1":
                send_mode_command("cold")
            elif mode_choice == "2":
                send_mode_command("hot")
            elif mode_choice == "3":
                send_mode_command("constant")
        elif choice == "6":
            break

        time.sleep(1)

except KeyboardInterrupt:
    print("Publisher exiting...")
    publisher.loop_stop()
    publisher.disconnect()