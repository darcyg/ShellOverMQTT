import queue
from queue import Queue
from subprocess import check_output
import logging

class Shell:
    def __init__(self, name=None, mqttClient=None, config=None):
        self._logger = logging.getLogger("logger")
        if(name is None):
            raise TypeError("Shell name is None")
        if(mqttClient is None):
            raise TypeError("MQTT client is None. Proper object required.")
        if(config is None):
            raise TypeError("Configuration is None")
        self._name = name
        self._config = config
        self._listeningTopicPrefix = "Shell/"
        self._messageQueue = Queue()
        self._mqttClient = mqttClient
        self._mqttClient.on_connect = self._onConnectCallback
        self._mqttClient.on_message = self._onMessageCallback

    def _onMessageCallback(self, mqttc, obj, msg):
        try:
            self._messageQueue.put(msg, block=False)
        except queue.Full:
            self._logger.warn("Queue is full")

    def _onConnectCallback(self, mqttc, obj, flags, rc):
        self._logger.info("Connected to MQTT broker")

    def _handleNextMessage(self):
        try:
            msg = self._messageQueue.get(block=False)
            print(msg.payload)
            #self._callSystemCommand(msg.payload)
        except queue.Empty:
            self._logger.warn("Queue is empty. Returning.")

    def _callSystemCommand(self, cmd):
        output = check_output(cmd, shell=True)

    def Run(self):
        self._mqttClient.connect(self._config.Address)
        self._mqttClient.subscribe(self._buildShellListeningTopic(), 0)

        rc = 0
        while rc == 0:
            if(self._messageQueue.empty() == False):
                self._handleNextMessage()
            rc = self._mqttClient.loop()
        return rc

    def _buildShellListeningTopic(self):
        return "".join([self._listeningTopicPrefix, self._name])





