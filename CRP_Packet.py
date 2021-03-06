# Class to represent a complete CRP Packet. Uses the header class and
# additionally incorporates the payload
import zlib
from CRP_Packet_Header import CRP_Packet_Header

class CRP_Packet:

	def __init__(self, crp_header = CRP_Packet_Header(), data = None):
		self.crp_header = crp_header
		self.data = data
		#Todo check if checksum works properly

		self.crp_header.data_checksum = self.computeChecksum(str(self.data))
		# self.crp_header.header_checksum = self.crp_header.computeChecksum()

	def __str__(self):
		return str(self.crp_header) + "\nData: " + str(self.data)

	# Used crc32 converted to unsigned for consistent checksum calculation
	# Reference: http://stackoverflow.com/questions/30092226/how-to-calculate-crc32-with-python-to-match-online-results
	def computeChecksum(self, value):
		return hex(zlib.crc32(value) & 0xffffffff)

	def checkPacket(self):
		return (self.computeChecksum(self.data) == self.crp_header.data_checksum)
		
	def getHeader(self):
		return self.crp_header

	def getData(self):
		return self.data

	def insertData(self, data):
		self.data = data

	def setHeader(self, header):
		self.crp_header = header
