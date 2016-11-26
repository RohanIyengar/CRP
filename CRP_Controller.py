from CRP_Socket import CRP_Socket
from CRP_Packet import CRP_Packet
from CRP_Packet_Header import CRP_Packet_Header
import sys

from collections import deque
import Queue    

class CRP_Controller:

    def __init__(self):
        print "Controller Initialized"

    def createAndBindSocket(self, ip_addr, port_num):
        newSocket = CRP_Socket()
        src_addr = (ip_addr, port_num)
        newSocket.bind(src_addr)
        return newSocket

    def clientSideConnect(self, clientSocket, dst_addr):
        clientSocket.connect(dst_addr)

        syn_ack = self.sendSYN(clientSocket)
        clientSocket.seq_num = 1000
        clientSocket.ack_num = 0

        self.sendACK(clientSocket)

    def listenForConnection(self, serverSocket, numConnections):
        listenTries = 15

        while listenTries > 0:
            try:
                return serverSocket.listen(numConnections)
            except Exception as e:
                if str(e) == "timed out":
                    listenTries -= 1
                else:
                    #print(str(e))
                    print("Waiting for client to connect, still have %s tries" % str(listenTries))
                    listenTries-= 1
                    if listenTries == 0:
                        print (str(e))
                        sys.exit()

    def serverSideAccept(self, serverSocket, addr_tuple):
        serverSocket.accept()
        serverSocket.dst_addr = addr_tuple
        response = self.sendSYNACK(serverSocket) #Use helper method
        # print("Server accepted connection : " + str(addr_tuple[0]) + str(addr_tuple[1]))

    def closeSocket(self, a_socket):
        # Initiate from the client side
        fin_header = CRP_Packet_Header()
        fin_header.src_port = a_socket.src_addr[1]
        fin_header.dst_port = a_socket.dst_addr[1]
        fin_header.fin_flag = 1
        fin_packet = CRP_Packet(fin_header)
        
        sendTries = 0
        #stage = 0
        # Send fin expect to receive back ack
        while sendTries < 50:
            a_socket.send(fin_packet)

            try:
                packet = a_socket.recv(1024) #Need to define max size

                if not packet.checkPacket():
                    sendTries+=1
                elif packet.crp_header.syn_flag != 0 or packet.crp_header.ack_flag != 1 or packet.crp_header.fin_flag != 0:
                    # Wrong type of packet
                    sendTries += 1
                else:
                    #Successful ACK Received
                    a_socket.close()
                    return
            except Exception as e:
                if str(e) == "timed out":
                    sendTries += 1
                else:
                    raise e

        #Should never get here
        raise Exception("Closing socket failed")

    def closeServer(self, a_socket):
        a_socket.close()
        print "Server has been terminated."

    def setWindowSize(a_socket, size):
        a_socket.max_window_size = size

    def sendACK(self, a_socket):
        print "Send ACK packet"
        ack_header = CRP_Packet_Header()
        ack_header.src_port = a_socket.src_addr[1]
        ack_header.dst_port = a_socket.dst_addr[1]
        ack_header.ack_flag = 1
        ack_header.ack_num = a_socket.ack_num
        ack_packet = CRP_Packet(ack_header)
        a_socket.send(ack_packet)
        a_socket.ack_num += 1

    def sendSYN(self, a_socket):
        print("Send SYN packet")
        syn_header = CRP_Packet_Header()
        syn_header.src_port = a_socket.src_addr[1]
        syn_header.dst_port = a_socket.dst_addr[1]
        syn_header.syn_flag = 1
        syn_packet = CRP_Packet(syn_header)

        sendTries = 0
        while sendTries < 50:
            a_socket.send(syn_packet)
            try:
                packet, address = a_socket.recv(1024) #Need to define max size
                sendTries = 50
                print("Received SYN")

                if not packet.checkPacket():
                    sendTries+=1
                elif packet.crp_header.syn_flag != 1 or packet.crp_header.ack_flag != 1 or packet.crp_header.fin_flag != 0:
                    # Wrong type of packet
                    sendTries += 1
                else:
                    #Successful SYNACK Received
                    return packet
            except Exception as e:
                if str(e) == "timed out":
                    sendTries += 1
                elif sendTries < 50:
                    sendTries += 1
                else:
                    raise e

        #Should never get here
        return None


    def sendSYNACK(self, a_socket):
        print("Send SYNACK packet")

        synack_header = CRP_Packet_Header()
        synack_header.src_port = a_socket.src_addr[1]
        synack_header.dst_port = a_socket.dst_addr[1]
        synack_header.ack_flag = 1
        synack_header.syn_flag = 1
        synack_packet = CRP_Packet(synack_header)

        sendTries = 0
        while sendTries < 50:
            a_socket.send(synack_packet)
            try:
                packet, address = a_socket.recv(1024) #Need to define max size
                sendTries = 50
                print("Received SYN/ACK")

                if not packet.checkPacket():
                    sendTries+=1
                elif packet.crp_header.syn_flag != 0 or packet.crp_header.ack_flag != 1 or packet.crp_header.fin_flag != 0:
                    # Wrong type of packet
                    sendTries += 1
                else:
                    #Successful ACK Received
                    return packet
            except Exception as e:
                if str(e) == "timed out":
                    sendTries += 1
                elif sendTries < 50:
                    sendTries += 1
                else:
                    raise e

        #Should never get here
        return None

    def sendDataPacket(self, a_socket, message):
        #Edit for window size
        numPackets = math.ceil(len(message) / a_socket.MAX_PACKET_SIZE)
        sendQueue = Queue.queue()
        ackQueue = list.list()
        for i in range(1,numPackets-1):
            header = CRP_Packet_Header()
            header.src_port = a_socket.src_addr[1]
            header.dst_port = a_socket.dst_addr[1]
            header.seq_num = a_socket.seq_num
            a_socket.seq_num += 1
            if i != numPackets - 1:
                data = message[(i - 1)*a_socket.MAX_PACKET_SIZE:(a_socket.MAX_PACKET_SIZE*i)-1]
            else:
                data = message[(i - 1)*a_socket.MAX_PACKET_SIZE:end]
            packet = CRP_Packet(header, data)
            sendQueue.put(packet)
        for j in range(sendQueue.qsize()):
            sendTries = 0
            sent = False
            currPacket = queue.get()
            while sendTries < 50:
                try:
                    a_socket.send(currPacket)
                    sent = True
                except Exception as e:
                    if str(e) == "timed out":
                        sendTries += 1
                    else:
                        raise e
            if sent is True:
                ackQueue.add((currPacket.getHeader().getSeqNum(),currPacket))
        while ackQueue.qsize() > 0:
            try:
                packet, address = a_socket.recv(a_socket.MAX_PACKET_SIZE)
                ackQueue.remove(packet.getHeader().getSeqNum())
            except Exception as e:
                raise e

    def recvDataPacket(self, a_socket, buf_size):
        buff = ""
        recvTries = 0
        packet = None
        while recvTries < 50:
            try:
                packet, address = a_socket.recv(int(buf_size))
            except Exception as e:
                if str(e) == "timed out":
                    recvTries += 1
                #else:
                #    raise e
            if packet is not None:
                print str(packet.getData())
                if packet.getHeader().getSeqNum() == a_socket.ack_num:
                    a_socket.ack_num += 1
                    sendACK(a_socket)
                    buff += str(packet.getData())
                elif packet.getHeader().getSeqNum() > a_socket.ack_num:
                    finished = False
                    while not finished:
                        curr = a_socket.rcvQueue.get()
                        if curr[0] == a_socket.ack_num:
                            #Handle data sending
                            sendACK(a_socket)
                            buff += str(curr[1].getData())
                        else:
                            if a_socket.ack_num != packet.getHeader().getSeqNum():
                                a_socket.rcvQueue.put((packet.getHeader().getSeqNum(), packet))
                            else:
                                sendACK(a_socket)
                                buff += str(packet.getData())
                            finished = True

        return buff