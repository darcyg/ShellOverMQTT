from configparser import ConfigParser

class BrokerConfiguration:
    def __init__(self, address=None, port=1883, login=None, password=None):
        self.Address = address
        self.Port = port
        self.Login = login
        self.Password = password

class Configuration:
    def __init__(self, configFile=None):
        self.filename = configFile
        self.parser = ConfigParser()


    def GetBrokerConfiguration(self):
        self.parser.read(self.filename)
        address = self.parser.get("MQTTBroker", "Address")
        port = self.parser.get("MQTTBroker", "Port")
        login = self.parser.get("MQTTBroker", "Login")
        password = self.parser.get("MQTTBroker", "Password")
        return BrokerConfiguration(address=address, port=port, login=login, password=password)