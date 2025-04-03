import paho.mqtt.client as mqtt
import json
import ssl
import time

# MQTT Broker配置
BROKER = "172.24.23.109"
PORT = 1883
USERNAME = "Team2"
PASSWORD = "123456"

# 主题配置
CONTROL_TOPIC = "light/control"
MODE_TOPIC = "light/mode"


def on_connect(client, userdata, flags, rc,properties=None):
    print("Publisher Connected with result code " + str(rc))


def create_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
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


if __name__ == "__main__":
    client = create_mqtt_client()
    client.loop_start()

    try:
        # 示例控制
        time.sleep(1)  # 等待连接建立

        # 控制单个灯
        control_light(client, 1, "on")
        time.sleep(2)
        control_light(client, 1, "off")

        # 控制多个灯
        control_light(client, [2, 3, 4], "on")
        time.sleep(2)
        control_light(client, [2, 3, 4], "off")

        # 设置模式
        set_mode(client, "bright")
        time.sleep(2)
        set_mode(client, "sleep")
        time.sleep(2)
        set_mode(client, "normal")

    except KeyboardInterrupt:
        print("Publisher exiting...")
    finally:
        client.loop_stop()
        client.disconnect()