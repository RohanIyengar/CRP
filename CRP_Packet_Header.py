class CRP_Packet_Header:
# This class has all the necessary header fields to be incorporated in a CRP packet

	def __init__(self, src_port = 1337, dst_port = 1338, seq_num = 0, ack_num = 0, ack_flag = 0, rst_flag = 0, syn_flag = 0, fin_flag = 0, window_size = 5, header_checksum = 0, data_checksum = 0):
		self.src_port = src_port
		self.dst_port = dst_port
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack_flag = ack_flag
		self.rst_flag = rst_flag # might not need this flag
		self.syn_flag = syn_flag
		self.fin_flag = fin_flag
		self.window_size = window_size
		self.header_checksum = header_checksum
		self.data_checksum = data_checksum

	def __str__(self):
		return ("\nPacket information\n" + "Source port: "
		+ str(self.src_port) + "\nDestination port: " + str(self.dst_port)
		+ "\nSequence Number: " + str(self.seq_num) + "\nACK Number: "
		+ str(self.ack_num) + "\nACK Flag: " + str(self.ack_flag) + "RST Flag: "
		+ str(self.rst_flag) + "\nSYN Flag: " + str(self.syn_flag) + "\nFIN Flag: "
		+ str(self.fin_flag) + "\nWindow Size: " + str(self.window_size)
		+ "\nHeader Checksum: " + str(self.header_checksum) + "\nData Checksum: "
		+ str(self.data_checksum))

	def getAckFlag(self):
		return self.ack_flag
		
	def getSynFlag(self):
		return self.syn_flag
	
	def getFinFlag(self):
		return self.fin_flag
		
	def getSeqNum(self):
		return self.seq_num

