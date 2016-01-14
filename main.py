import socket

def main():
    Hostname = socket.gethostname()
    print(Hostname)
    return 0

if(__name__ == '__main__'):
    main()