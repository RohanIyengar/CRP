from CRP_Controller import CRP_Controller
import sys
import time
import socket

#basic send. Should fail cause sockets are not connected
def test_basic_sending():
    CRP = CRP_Controller()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 2016))
    ipaddress = s.getsockname()[0]
    print "Testing basic connection as a server"
    #client = CRP.createAndBindSocket("127.0.0.1", 5000)
    server = CRP.createAndBindSocket(ipaddress, 5001)
    client_info = None
    while client_info is None:
        print "Server is listening"
        CRP.listenForConnection(server, 1)
        client_info = serverSocket.connectionsQueue.get()
        print("Here1")

    print "Server receiving data"
    response = RxP.receiveData(server, 999999)
    print "Received data: ", response
    CRP.closeSocket(server)

test_basic_sending()