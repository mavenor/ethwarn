# import paho.mqtt.client as mqtt
# import time

# def on_connect(client, data, flags, ret_code):
#     if (ret_code == 0):
#         print(f"Connected with result code {ret_code}")
#     else:
#         print(f"Failed to connect: {ret_code}")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.username_pw_set("dunkirk", "dVn3s*#0f^k1rK")
# print("Hellowe")
# client.connect(host="www.roamingwalrus.tk", port=8883, keepalive=60)
# print("byeee")
# # client.connect()

# # don't end unless explicit socket disconnect
# # client.loop_forever()
# foo = "abcdef12"

# run = True
# def on_publish(client, userdata, mid):
#     run = False;


# def push_data(payload, type):

#     client = mqtt.Client()
#     client.on_publish = on_publish
#     try:
#             client.connect('localhost', 4444)
#     except:
#             print("ERROR: Could not connect to MQTT.")

#     client.publish(f"{foo}/{type}", payload=payload, qos=0, retain=True)

#     while run:
#         client.loop()
#     client.disconnect()

# push_data("Hello, world!\n", "hello")

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_p(client, userdata, flags):
    print("published somthing")



client = mqtt.Client("sdfsodijf")
# client.username_pw_set("dunkirk", "dVn3s*#0f^k1rK")
client.on_connect = on_connect
client.on_publish = on_p
print("before")
client.connect("roamingwalrus.tk", 8883)
print("aft")

# send a message to the raspberry/topic every 1 second, 5 times in a row
for i in range(5):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.disconnect()
# client.loop_forever()
