import paho.mqtt.client as mqtt
import time

def on_connect(client, data, flags, ret_code):
    if (ret_code == 0):
        print(f"Connected with result code {ret_code}")
    else:
        print(f"Failed to connect: {ret_code}")

run = True
def on_publish(client, userdata, mid):
    run = False;

client = mqtt.Client()
client.tls_set(tls_version=2)
client.on_connect = on_connect
client.on_publish = on_publish
uid = "dunkirk"
client.username_pw_set(uid, "dVn3s*#0f^k1rK")
client.connect(host="roamingwalrus.tk", port=8883, keepalive=60)

# don't end unless explicit socket disconnect
# client.loop_forever()

def push_data(payload, type):
    global run
    run = True
    client.publish(f"{uid}/{type}", payload=payload, qos=0, retain=True)

    client.loop_start()
    while True:
        if not run:
            break
    client.loop_stop()
    client.disconnect()

push_data("Hello, world!\n", "hello")

# import paho.mqtt.client as mqtt
# import time

# def on_connect(client, userdata, flags, rc):
#     print(f"Connected with result code {rc}")

# def on_p(client, userdata, flags):
#     print("published somthing")



# client = mqtt.Client()
# # client.username_pw_set("dunkirk", "dVn3s*#0f^k1rK")
# client.on_connect = on_connect
# client.on_publish = on_p
# print("before")
# client.connect("127.0.0.1", 1883)
# print("aft")

# # send a message to the raspberry/topic every 1 second, 5 times in a row

# client.publish('python/mutt', payload="ojojoijoh", qos=0, retain=False)

# client.disconnect()
# # client.loop_forever()
