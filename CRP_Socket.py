import socket
import CRP_Packet
import Queue
import pickle

from CRP_Socket_State import CRP_Socket_State

class CRP_Socket:

	def __init__(self, ipVersion, packetType, protocolNumber):
		# Use this_socket to not collide with socket class namespace
		if ipVersion == "IPv6":
			self.this_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		else:
			self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		#Todo - Figure out what to do with the rest of the input parameters
		this_socket.socketblocking(0);
		self.src_addr = None
		self.dst_addr = None
		self.seq_num = 0
		self.ack_num = 0
		self.send_window_size = 5
		self.rcv_window_size = 5
		self.state = CRP_Socket_State.CREATED
		self.this_socket.settimeout(5.0)
		self.connectionsQueue = Queue.queue()
		self.rcvQueue = Queue.PriorityQueue()
		self.sendList = list.list()

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

		self.dst_addr = address
		self.state = CRP_Socket_State.CONNECTED

	def listen(self, numConnections):
		while 1:
			# TODO: Figure out a big enough buffer size
			packetString, address = self.this_socket.recvfrom(bufferSize)
			packet = pickle.load(packetString)
			if self.state == CRP_Socket_State.CONNECTED and self.dst_addr == address:
				if packet.getHeader().getFinFlag() == 1:
					close(self)
				elif packet.getHeader().getAckFlag() == 1:
					sendList.remove(packet.getHeader().getAckNum())
				else:
					if self.rcvQueue.qsize() < (2 * self.rcv_window_size):
						rcvQueue.put((packet.getHeader().getSeqNum(), packet.getData()))
						sendPacket = CRP_Packet(crp_header = CRP_Packet_Header(ack_num = packet.getHeader().getSeqNum(), ack_flag = 1, window_size = self.rcv_window_size-1))
						send(self, sendPacket)
			elif self.state == CRP_Socket_State.BIND:
				if self.connectionsQueue.qsize() < numConnections:
					connectionsQueue.put(dst_addr)
		return 0

	def send(self, message, flags = None):
		# Todo - pack the packet in the line below
		packedPacket = packet
		packedMessage = pickle.dumps(packedPacket)
		# Are flags really necessary?
		if flags != None:
			self.this_socket.sendto(packedMessage, flags, self.dst_addr)
		else:
			self.this_socket.sendto(packedMessage, self.dst_addr)

	# Don't think we need this method anymore - as only TCP sockets support it
	def sendAll(self, message, flags):
		return 0

	def close(self):
		self.state = CRP_Socket_State.CLOSED
		#Might need to send a close packet?
		self.this_socket.close()

	def shutdown(self):
		self.state = CRP_Socket_State.CLOSED
		self.this_socket.shutdown()

	def accept(self):
		#Todo - finish this method
		if self.this_socket.state != CRP_Socket_State.BIND:
			raise Exception()
		else:

		
		return 0

	def recv(self, bufferSize, flags = None):
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


		
	# def recvHelper(self, bufferSize):
	# 	packetString, address = self.this_socket.recvfrom(bufferSize)
	# 	packet = pickle.load(packetString)
	# 	if self.state == CRP_Socket_State.CONNECTED and self.dst_addr == address:
	# 		if packet.getHeader().getFinFlag() == 1:
	# 			close(self)
	# 		elif packet.getHeader().getAckFlag() == 1:
	# 			sendList.remove(packet.getHeader().getAckNum())
	# 		else:
	# 			if self.rcvQueue.qsize() < (2 * self.rcv_window_size):
	# 				rcvQueue.put((packet.getHeader().getSeqNum(), packet.getData()))
	# 				sendPacket = CRP_Packet(crp_header = CRP_Packet_Header(ack_num = packet.getHeader().getSeqNum(), ack_flag = 1, window_size = self.rcv_window_size-1))
	# 				send(self, sendPacket)

					
