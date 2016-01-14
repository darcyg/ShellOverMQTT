import socket
from configuration import Configuration

def main():
    Hostname = socket.gethostname()
    print(Hostname)
    configuration = Configuration(".config")
    brokerCfg = configuration.GetBrokerConfiguration()
    print(brokerCfg.Address)
    print(brokerCfg.Port)
    print(brokerCfg.Login)
    print(brokerCfg.Password)

    return 0

if(__name__ == '__main__'):
    main()