from CRP_Socket import CRP_Socket
from CRP_Packet import CRP_Packet
from CRP_Packet_Header import CRP_Packet_Header

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

	def clientSideConnect(self, clientSocket, ip_addr, port_num):
		dst_addr = (ip_addr, port_num)
		clientSocket.connect(dst_addr)

		syn_ack = sendSYN(clientSocket)
		client_socket.seq_num = 1000
		client_socket.ack_num = 0

		sendACK(clientSocket)

	def listenForConnection(self, serverSocket, numConnections):
		listenTries = 50
		while listenTries > 0:
			try:
				serverSocket.listen(numConnections)
			except Exception as e:
				if str(e) == "timed out":
					listenTries += 1
				else:
					raise e

	def serverSideAccept(self, serverSocket, addr_tuple):
		serverSocket.accept()
		serverSocket.dst_addr = addr_tuple
		response = sendSYNACK(serverSocket) #Use helper method

		print("Server accepted connection : " + str(addr_tuple))

	def closeSocket(self, a_socket):
		# Initiate from the client side
		fin_header = CRP_Packet_Header()
		fin_header.src_port = a_socket.src_addr[1]
		fin_header.dst_port = a_socket.dst_addr[1]
		fin_header.fin_flag = 1
		fin_packet = CRP_Packet(fin_header)
		
		sendTries = 0
		#stage = 0
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

	def setWindowSize(a_socket, size):
		a_socket.max_window_size = size

	def sendACK(a_socket):
		ack_header = CRP_Packet_Header()
		ack_header.src_port = a_socket.src_addr[1]
		ack_header.dst_port = a_socket.dst_addr[1]
		ack_header.ack_flag = 1
		ack_header.ack_num = a_socket.ack_num
		ack_packet = CRP_Packet(ack_header)
		a_socket.send(ack_packet)

	def sendSYN(a_socket):
		syn_header = CRP_Packet_Header()
		syn_header.src_port = a_socket.src_addr[1]
		syn_header.dst_port = a_socket.dst_addr[1]
		syn_header.syn_flag = 1
		syn_packet = CRP_Packet(syn_header)

		sendTries = 0
		while sendTries < 50:
			a_socket.send(syn_packet)

			try:
				packet = a_socket.recv(1024) #Need to define max size

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
				else:
					raise e

		#Should never get here
		return None


	def sendSYNACK(a_socket):
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
				packet = a_socket.recv(1024) #Need to define max size

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
				else:
					raise e

		#Should never get here
		return None

	def sendDataPacket(self, a_socket, message):
		header = CRP_Packet_Header()
		header.src_port = a_socket.src_addr[1]
		header.dst_port = a_socket.dst_addr[1]
		header.seq_num = a_socket.seq_num
		a_socket.seq_num += 1
		packet = CRP_Packet(header, message)
		sendTries = 0
		while sendTries < 50:
			try:
				a_socket.send(packet)
			except Exception as e:
				if str(e) == "timed out":
					sendTries += 1
				else:
					raise e

