

import paho.mqtt.client as mqtt
import json
import ssl
import time
import threading

# MQTT Broker配置
BROKER = "172.24.23.109"
PORT = 1883
USERNAME = "Team2"
PASSWORD = "123456"

# 主题配置
CONTROL_TOPIC = "light/control"
MODE_TOPIC = "light/mode"


def on_connect(client, userdata, flags, rc, properties=None):
    print("Publisher Connected with result code " + str(rc))


def on_disconnect(client, userdata, rc, properties=None):
    print("Publisher Disconnected with result code " + str(rc))
    # 自动重连
    while True:
        try:
            client.reconnect()
            print("Reconnected successfully!")
            break
        except Exception as e:
            print(f"Reconnection failed: {e}, retrying in 5 seconds...")
            time.sleep(5)


def create_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(BROKER, PORT, 60)
    return client


def control_light(client, light_ids, action):
    """控制单个或多个灯的开关"""
    if isinstance(light_ids, int):
        light_ids = [light_ids]

    payload = {
        "lights": light_ids,
        "action": action  # "on" 或 "off"
    }
    client.publish(CONTROL_TOPIC, json.dumps(payload))
    print(f"Published control message: {payload}")


def set_mode(client, mode):
    """设置灯光模式"""
    modes = ["bright", "sleep", "normal"]
    if mode not in modes:
        print(f"Invalid mode. Available modes: {modes}")
        return

    client.publish(MODE_TOPIC, mode)
    print(f"Published mode message: {mode}")


def start_mqtt_client(client):
    """启动MQTT客户端网络循环"""
    client.loop_start()


def user_interface(client):
    """用户交互界面"""
    print("\nLight Control System")
    print("---------------------")
    print("1. Turn on light(s)")
    print("2. Turn off light(s)")
    print("3. Set light mode")
    print("4. Exit")

    while True:
        try:
            choice = input("\nEnter your choice (1-4): ")

            if choice == "1":
                light_ids = input("Enter light ID(s) to turn on (comma separated): ")
                light_ids = [int(id.strip()) for id in light_ids.split(",")]
                control_light(client, light_ids, "on")

            elif choice == "2":
                light_ids = input("Enter light ID(s) to turn off (comma separated): ")
                light_ids = [int(id.strip()) for id in light_ids.split(",")]
                control_light(client, light_ids, "off")

            elif choice == "3":
                print("Available modes: bright, sleep, normal")
                mode = input("Enter mode: ").lower()
                set_mode(client, mode)

            elif choice == "4":
                print("Exiting...")
                client.disconnect()
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter numbers for light IDs.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    client = create_mqtt_client()
    start_mqtt_client(client)

    # 等待连接建立
    time.sleep(1)

    # 启动用户界面
    user_interface(client)

    # 清理
    client.loop_stop()


if __name__ == "__main__":
    main()