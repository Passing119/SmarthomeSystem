import paho.mqtt.client as mqtt
import time

# MQTT Broker 配置
BROKER_HOST = "172.24.22.164"  # Broker 地址
BROKER_PORT = 1883  # Broker 端口
CLIENT_ID = "Team2_Class1"  # 客户端 ID


# 定义回调函数
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("连接成功！")
    else:
        print(f"连接失败，错误码：{rc}")


def on_disconnect(client, userdata, rc, properties=None):
    print("断开连接！")


# 创建 MQTT 客户端，指定 callback_api_version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)

# 设置回调函数
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# 连接到 Broker
'''try:
    print("正在连接 Broker...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()  # 启动网络循环
    time.sleep(1)  # 等待连接完成
except Exception as e:
    print(f"连接失败: {e}")
    exit(1)'''
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

# 发布控制指令
def control_aircon(power=None, temperature=None, fan_speed=None, fan_direction=None):
    if power is not None:
        client.publish("aircon/control/power", power)
        print(f"发布开关指令: {power}")

    if temperature is not None:
        client.publish("aircon/control/temperature", temperature)
        print(f"发布温度指令: {temperature}°C")

    if fan_speed is not None:
        client.publish("aircon/control/fan_speed", fan_speed)
        print(f"发布风速指令: {fan_speed}")

    if fan_direction is not None:
        client.publish("aircon/control/fan_direction", fan_direction)
        print(f"发布风向指令: {fan_direction}")


# 示例：控制空调
#control_aircon(power="on", temperature=25, fan_speed="high", fan_direction="auto")

# 保持连接
client.loop_forever()