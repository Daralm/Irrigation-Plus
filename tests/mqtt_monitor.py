from paho.mqtt.client import Client

def on_connect(client, userdata, flags, rc) -> None:
    print("Connected with result code "+str(rc))
    return

def on_message(client, userdata, msg) -> None:
    print(msg.topic, msg.payload)

client = Client('100')
client.connect('192.168.2.10', port=1883)
client.subscribe('valve_1')
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()