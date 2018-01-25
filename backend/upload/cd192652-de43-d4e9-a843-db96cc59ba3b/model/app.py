# -*- coding:utf-8 -*-

import random 

from tornado.web import Application,RequestHandler 
from tornado.options import options,parse_command_line
from tornado.gen import coroutine,IOLoop
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
import paho.mqtt.client as mqtt


client = mqtt.Client()

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("chinasws")
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):

    #print(msg.topic + " " + str(msg.payload))
    def on_response(response):
        print("on_response running result:{} message:{}".format(response.code,msg.payload))
    http_client=AsyncHTTPClient()
    http_request=HTTPRequest('https://www.baidu.com?body={}'.format(random.randint(1,100000)))
    http_client.fetch(request=http_request,callback=on_response)


class PubMessageHandler(RequestHandler):
    
    @coroutine
    def get(self):
        topic=self.get_argument('topic')
        body=self.get_argument('body')
        print(topic)
        print(body)
        info=client.publish(topic,payload=body)
        while info.is_published():
            break

        self.write(str(info.mid))


@coroutine
def mqtt_subscribe():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async("192.168.199.174", 1883, 60)
    #client.connect("192.168.2.40", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.

    #client.loop_forever()
    client.loop_start()

def main():
    parse_command_line()
    handlers=[
        (r'/pub',PubMessageHandler),
    ]
    setting={
        'debug':True
    }
    app=Application(handlers=handlers,**setting)
    app.listen(11108)
    ioloop=IOLoop.current()
    ioloop.add_callback(mqtt_subscribe)
    print('server running at 11108')
    ioloop.start()

if __name__ == '__main__':
    main()
