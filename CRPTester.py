from CRP_Controller import CRP_Controller
import sys
import time
import socket

#basic send. Should fail cause sockets are not connected
def test_basic_sending():
    CRP = CRP_Controller()
    print "Testing basic connection as a client"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 2016))
    ipaddress = s.getsockname()[0]
    client = CRP.createAndBindSocket("127.0.0.1", 5000)
    # server = CRP.createAndBindSocket("127.0.0.1", 5001)
    print "Client connecting"
    CRP.clientSideConnect(client, (ipaddress, 5001))
    print "Client connected"
    CRP.sendDataPacket(client, "Hello, World!  This is a big test.   Test Test T")
    response = RxP.receiveData(server, 999999)
    print "Received data: ", response
    CRP.closeSocket(server)
    CRP.closeSocket(client)

test_basic_sending()