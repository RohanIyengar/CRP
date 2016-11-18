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

	def bind(self, address):
		return 0

	def connect(self, address):
		return 0

	def listen(self, numConenctions):
		return 0

	def send(self, message, flags):
		return 0

	def sendAll(self, message, flags):
		return 0

	def close(self):
		return 0

	def shutdown(self):
		return 0

	def accept(self):
		return 0

	def recv(self, bufferSize, flags):
		return 0