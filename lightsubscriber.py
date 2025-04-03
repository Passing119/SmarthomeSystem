import paho.mqtt.client as mqtt
import json
import ssl
import time

# MQTT Broker配置
BROKER = "172.24.23.109"
PORT = 1883
USERNAME = "Team2"
PASSWORD = "123456"
CLIENT_ID = "smart-light-controller"

# 主题配置
CONTROL_TOPIC = "light/control"
MODE_TOPIC = "light/mode"

# 灯光状态
lights = {
    1: False,  # 1号灯
    2: False,  # 2号灯
    3: False,  # 3号灯
    4: False,  # 4号灯
    5: False  # 5号灯
}


class LightController:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(USERNAME, PASSWORD)
        #self.client.tls_set(ca_certs=CA_CERT, cert_reqs=ssl.CERT_REQUIRED)
        #self.client.tls_insecure_set(False)  # 生产环境应设为False

        # 设置回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc,properties=None):
        print("Connected with result code " + str(rc))
        # 订阅主题
        client.subscribe([(CONTROL_TOPIC, 0), (MODE_TOPIC, 0)])
        print(f"Subscribed to topics: {CONTROL_TOPIC}, {MODE_TOPIC}")

    def on_message(self, client, userdata, msg):
        print(f"Received message on {msg.topic}: {msg.payload.decode()}")

        try:
            if msg.topic == CONTROL_TOPIC:
                self.handle_control_message(msg.payload)
            elif msg.topic == MODE_TOPIC:
                self.handle_mode_message(msg.payload)
        except Exception as e:
            print(f"Error processing message: {e}")

    def handle_control_message(self, payload):
        """处理控制单个/多个灯的消息"""
        data = json.loads(payload)
        light_ids = data["lights"]
        action = data["action"]

        if not isinstance(light_ids, list):
            light_ids = [light_ids]

        for light_id in light_ids:
            if light_id in lights:
                lights[light_id] = (action == "on")
                self.update_light(light_id, lights[light_id])
            else:
                print(f"Invalid light ID: {light_id}")

    def handle_mode_message(self, payload):
        """处理灯光模式设置消息"""
        mode = payload.decode().lower()

        if mode == "bright":
            # 明亮模式: 所有灯全开
            for light_id in lights:
                lights[light_id] = True
                self.update_light(light_id, True)
            print("All lights turned ON (bright mode)")

        elif mode == "sleep":
            # 睡眠模式: 只开1号灯
            for light_id in lights:
                lights[light_id] = (light_id == 1)
                self.update_light(light_id, lights[light_id])
            print("Only light 1 turned ON (sleep mode)")

        elif mode == "normal":
            # 普通模式: 开1、2、3号灯
            for light_id in lights:
                lights[light_id] = (light_id in [1, 2, 3])
                self.update_light(light_id, lights[light_id])
            print("Lights 1, 2, 3 turned ON (normal mode)")

        else:
            print(f"Unknown mode: {mode}")

    def update_light(self, light_id, state):
        """实际控制灯的硬件"""
        # 这里应该替换为实际的硬件控制代码
        action = "ON" if state else "OFF"
        print(f"Light {light_id} turned {action}")
        # GPIO控制代码示例:
        # GPIO.output(light_pins[light_id], GPIO.HIGH if state else GPIO.LOW)

    def start(self):
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_forever()


if __name__ == "__main__":
    controller = LightController()
    print("Smart Light Controller started. Waiting for commands...")
    try:
        controller.start()
    except KeyboardInterrupt:
        print("Controller exiting...")
    finally:
        controller.client.disconnect()