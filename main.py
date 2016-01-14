import socket
from configuration import Configuration
import mqtt.client as mqtt

Hostname = socket.gethostname()


class MQTTClass:
    def __init__(self, clientId=None, config=None):
        self._mqttc = mqtt.Client(clientId)
        self._config = config
        self._mqttc.on_connect = self.OnConnectCallback
        self._mqttc.on_message = self.OnMessageCallback
        self._mqttc.on_subscribe = self.OnSubscribeCallback
        self._mqttc.on_log = self.OnLog

    def OnConnectCallback(self, mqttc, obj, flags, rc):
        print("Connected to broker")

    def OnMessageCallback(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def OnSubscribeCallback(self, mqttc, obj, mid, grantedQoS):
        print("Subscribed: " + str(mid) + " " + str(grantedQoS))

    def OnLog(self, mqttc, obj, level, string):
        print(str(level) + ": " + string)

    def run(self):
        self._mqttc.connect(self._config.Address, self._config.Port, 60)
        self._mqttc.subscribe(self._mqttc._client_id, 0)

        rc = 0
        while rc == 0:
            rc = self._mqttc.loop( )
        return rc


def main():
    configuration = Configuration(".config")
    brokerConfig = configuration.GetBrokerConfiguration()
    clientConfig = configuration.GetClientConfiguration()

    mqttc = MQTTClass(clientConfig.ClientId, brokerConfig)
    rc = mqttc.run()
    print("rc: "+str(rc))

    return 0

if(__name__ == '__main__'):
    main()