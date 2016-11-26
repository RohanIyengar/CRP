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
        #Todo - Figure out what to do with the rest of the input parameters
        # self.this_socket.socketblocking(0);
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
        if self.state == CRP_Socket_State.CREATED:
            raise Exception("Socket not bound.")
        try:
            #Insert buffer size
            message, address = self.this_socket.recvfrom(1024)
            # print "Listen"
            packet = pickle.loads(message)
            # print "INstance " + type(message)
            # print str(packet)
            # print "SYNFLAG: " + str(packet.crp_header.syn_flag)
            if packet is not None:
                print "Picked up Packet"
                # print "SYN FLAG: " + packet.getHeader().getSynFlag()
                if packet.crp_header.syn_flag == 1:
                    return address
                    # print "qsize: " + str(self.connectionsQueue.qsize())
                    # if self.connectionsQueue.qsize() < numConnections:
                    #     print str(address)
                    #     self.connectionsQueue.put(address)
                    #     print "Queue: " + connectionsQueue.qsize()
                    #     return True
        except Exception as e:
            print("timed out")

    def send(self, packet, flags = None):
        # Todo - pack the packet in the line below
        packedPacket = None
        if packet.getHeader().getAckFlag() == 1 or packet.getHeader().getFinFlag() == 1 or packet.getHeader().getSynFlag() == 1:
            # print str(packet)
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
        # print str(packedPacket)
        # self.this_socket.sendto(packedPacket, self.dst_addr)

    # # Don't think we need this method anymore - as only TCP sockets support it
    # def sendAll(self, message, flags):
    #   return 0

    def close(self):
        #Might need to send a close packet?
        # Need to make the close packet with fin flag
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
            self.seq_num = 0
            self.ack_num = 1000
            self.state = CRP_Socket_State.CONNECTED
        return 0

    def recv(self, bufferSize, flags = None):
        received = False

        while received == False:
            try:
                # print self.dst_addr
                # print self.src_addr
                message, destination_addr = self.this_socket.recvfrom(bufferSize)
                # print str(message)
                if message is None:
                    print "Packet is None"
                else:
                    received = True
                    print "Packet received"
                    packet = pickle.loads(message)
                    print str(packet)
                    sleep(1)
                    if not isinstance(packet, CRP_Packet.CRP_Packet):
                        # Handle sending NACK
                        print("Received corrupted packet, got object of type: ", type(packet))
                        received = True
                    else:
                        received = True
                        if packet.getHeader().getAckFlag == 1:
                            print "Receive ACK Packet"
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

        #return (destination_addr, packet)
        return packet

        '''
        pQueueNum, packet = rcvQueue.get()
        if pQueueNum == self.seq_num:
            if (len(packet) > bufferSize):
                sio = StringIO.StringIO(packet)
                retValue = sio.read(bufferSize)
                rcvQueue.put((pQueueNum, sio.getValue()))
                return retValue
            return packet
            self.seq_num += 1
            self.rcv_window_size += 1
        '''


        
    # def recvHelper(self, bufferSize):
    #   packetString, address = self.this_socket.recvfrom(bufferSize)
    #   packet = pickle.load(packetString)
    #   if self.state == CRP_Socket_State.CONNECTED and self.dst_addr == address:
    #       if packet.getHeader().getFinFlag() == 1:
    #           close(self)
    #       elif packet.getHeader().getAckFlag() == 1:
    #           sendList.remove(packet.getHeader().getAckNum())
    #       else:
    #           if self.rcvQueue.qsize() < (2 * self.rcv_window_size):
    #               rcvQueue.put((packet.getHeader().getSeqNum(), packet.getData()))
    #               sendPacket = CRP_Packet(crp_header = CRP_Packet_Header(ack_num = packet.getHeader().getSeqNum(), ack_flag = 1, window_size = self.rcv_window_size-1))
    #               send(self, sendPacket)

    def getTimeout(self):
        return self.this_socket.gettimeout()

    def setTimeout(self, newTimeout):
        self.this_socket.settimeout(newTimeout)
