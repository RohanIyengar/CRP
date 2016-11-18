import socket
import CRP_Packet
from CRP_Socket_State import CRP_Socket_State

class CRP_Socket:

	def __init__(self, ipVersion, packetType, protocolNumber):
		# Use this_socket to not collide with socket class namespace
		if ipVersion == "IPv6":
			self.this_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		else:
			self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		#Todo - Figure out what to do with the rest of the input parameters
		self.src_addr = None
		self.dst_addr = None
		self.seq_num = 0
		self.ack_num = 0
		self.send_window_size = 5
		self.rcv_window_size = 5
		self.state = CRP_Socket_State.CREATED
		self.this_socket.settimeout(5.0)

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

	def listen(self, numConenctions):
		# This seems hard
		return 0

	def send(self, message, flags = None):
		# Todo - pack the packet in the line below
		packedPacket = packet
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
		self.this_socket.close()

	def shutdown(self):
		self.state = CRP_Socket_State.CLOSED
		self.this_socket.shutdown()

	def accept(self):
		#Todo - finish this method
		if (self.this_socket.state != CRP_Socket_State.BOUND):
			raise Exception()
		
		return 0

	def recv(self, bufferSize, flags):
		return 0