import queue
from queue import Queue
from subprocess import check_output
import logging
from mqtt.client import MQTT_LOG_DEBUG, MQTT_LOG_ERR, MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING

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
        self._shellTopicPrefix = "Shell/"
        self._shellListeningTopicSuffix = "/RXD"
        self._shellSendingTopicSuffix = "/TXD"
        self._messageQueue = Queue()
        self._mqttClient = mqttClient
        self._mqttClient.on_connect = self._onConnectCallback
        self._mqttClient.on_message = self._onMessageCallback
        self._mqttClient.on_log = self._onLogCallback

    def _onMessageCallback(self, mqttc, obj, msg):
        try:
            self._messageQueue.put(msg, block=False)
        except queue.Full:
            self._logger.warn("Queue is full")

    def _onConnectCallback(self, mqttc, obj, flags, rc):
        self._logger.info("Connected to MQTT broker")

    def _onLogCallback(self, mqttc, obj, level, string):
        switch = {
            MQTT_LOG_INFO: self._logger.info,
            MQTT_LOG_NOTICE: self._logger.info,
            MQTT_LOG_WARNING: self._logger.warn,
            MQTT_LOG_ERR: self._logger.error,
            MQTT_LOG_DEBUG: self._logger.debug
        }
        switch.get(level)(string)

    def _handleNextMessage(self):
        try:
            msg = self._messageQueue.get(block=False)
            self._mqttClient.publish(self._buildShellSendingTopic(), str(msg.payload))
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
        return "".join([self._shellTopicPrefix, self._name, self._shellListeningTopicSuffix])

    def _buildShellSendingTopic(self):
        return "".join([self._shellTopicPrefix, self._name, self._shellSendingTopicSuffix])





