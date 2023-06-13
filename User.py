import socket
import datetime

timestamp = datetime.datetime.now().strftime("%H:%M:%S_%d%b%Y")

def getHostIp():
    hostIp = socket.gethostname()
    print(hostIp)
    return hostIp


def getUser(hostIp):
    if hostIp == '192.168.0.175':
        return timestamp + ' SEAHAWK: '
    elif hostIp == '192.168.0.92':
        return timestamp + ' BOAT: '
    elif hostIp == '192.168.50.17':
        return timestamp + ' XJ: '
    elif hostIp == '14.100.122.130':
        return timestamp + ' Lester '
    else:
        return timestamp + ' You: '
