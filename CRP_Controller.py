from CRP_Socket import CRP_Socket
from CRP_Packet import CRP_Packet
from CRP_Packet_Header import CRP_Packet_Header

from collections import deque
import Queue

class CRP_Controller:

	def createAndBindSocket(ip_addr, port_num):
		newSocket = CRP_Socket()
		src_addr = (ip_addr, port_num)
		newSocket.bind(src_addr)
		return newSocket