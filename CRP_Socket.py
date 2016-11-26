import socket
import CRP_Packet
import Queue
import pickle

from CRP_Socket_State import CRP_Socket_State

class CRP_Socket:

    def __init__(self, ipVersion = "IPv4", packetType = None, protocolNumber = None):
        # Use this_socket to not collide with socket class namespace
        if ipVersion == "IPv6":
            self.this_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else:
            self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);

        self.src_addr = None
        self.dst_addr = None
        self.seq_num = 0
        self.ack_num = 0
        self.send_window_size = 5
        self.rcv_window_size = 5
        self.max_window_size = 5
        self.state = CRP_Socket_State.CREATED
        self.this_socket.settimeout(1.0)
        self.connectionsQueue = Queue.Queue()
        self.rcvQueue = Queue.PriorityQueue()
        self.sendList = [] 
        self.MAX_PACKET_SIZE = 1024

    def bind(self, address):
        self.src_addr = address
        self.this_socket.bind(self.src_addr)
        self.state = CRP_Socket_State.BIND


    def connect(self, address):
        if self.state == CRP_Socket_State.CREATED:
            print "Socket not bound yet"
            return
        elif self.state == CRP_Socket_State.CONNECTED:
            print "Socket already connected"
            return
        elif self.state == CRP_Socket_State.CLOSED:
            print "Socket closed"
            return

        self.dst_addr = address
        self.state = CRP_Socket_State.CONNECTED

    def listen(self, numConnections):
        printed = 0
        if self.state == CRP_Socket_State.CREATED:
            raise Exception("Socket not bound.")
        try:
            message, address = self.this_socket.recvfrom(1024)
            packet = pickle.loads(message)
            if packet is not None:
                if packet.crp_header.syn_flag == 1:
                    return address
        except Exception as e:
            if printed == 0:
                print("Connection timed out")

    def send(self, packet, flags = None):
        # Todo - pack the packet in the line below
        packedPacket = None
        if packet.getHeader().getAckFlag() == 1 or packet.getHeader().getFinFlag() == 1 or packet.getHeader().getSynFlag() == 1:
            packedPacket = pickle.dumps(packet)
        else:
            if self.state != CRP_Socket_State.CONNECTED:
                raise Exception("Trying to send data without connected socket")
            if self.send_window_size > 0:
                header.window_size = self.send_window_size - 1
                self.send_window_size -= 1
                packedPacket = pickle.dumps(packet)
                self.sendList.add(packet.getHeader().getSeqNum())
            else:
                raise Exception("Window full")
            # Are flags really necessary?
        if packedPacket != None:
            if flags != None:
                self.this_socket.sendto(packedPacket, flags, self.dst_addr)
            else:
                self.this_socket.sendto(packedPacket, self.dst_addr)


    def close(self):
        self.state = CRP_Socket_State.CLOSED
        self.this_socket.close()

    # Don't need this either tbh
    def shutdown(self):
        self.state = CRP_Socket_State.CLOSED
        self.this_socket.shutdown()

    def accept(self):
        #Todo - finish this method
        if self.state != CRP_Socket_State.BIND:
            raise Exception("Socket not bound yet")
        else:
            self.seq_num = 1000
            self.ack_num = 1000
            self.state = CRP_Socket_State.CONNECTED
        return 0

    def recv(self, bufferSize, flags = None):
        received = False

        while received == False:
            try:
                message, destination_addr = self.this_socket.recvfrom(bufferSize)
                if message is None:
                    print "Packet is empty"
                else:
                    received = True
            
                    packet = pickle.loads(message)
                    if not isinstance(packet, CRP_Packet.CRP_Packet):
                        # Handle sending NACK
                        print("Received corrupted packet, got object of type: ", type(packet))
                        received = True
                    else:
                        received = True
                        if packet.getHeader().getAckFlag == 1:
                            print "Received ACK Packet"
                            self.sendList.remove(packet.getHeader().getAckNum())
                            self.ack_num += 1
                            self.send_window_size += 1
                        elif not packet.checkPacket():
                            # Send NACK
                            print("Received corrupted packet. Checksums did not match.")
                        else:
                            print "Got a good packet"
            except Exception as e:
                # print "Error receiving packet"
                raise e
        return packet

    def getTimeout(self):
        return self.this_socket.gettimeout()

    def setTimeout(self, newTimeout):
        self.this_socket.settimeout(newTimeout)
