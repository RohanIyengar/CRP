class CRP_Packet_Header:
# This class has all the necessary header fields to be incorporated in a CRP packet

	def __init__(self):
		self.src_port = 1337
		self.dst_port = 1338
		self.seq_num = 0
		self.ack_num = 0
		self.ack_flag = 0
		self.rst_flag = 0 # might not need this flag
		self.syn_flag = 0
		self.fin_flag = 0
		self.window_size = 5
		self.header_checksum = 0
		self.data_checksum = 0

	def __str__(self):
		return ("\nPacket information\n" + "Source port: "
		+ str(self.src_port) + "\nDestination port: " + str(self.dst_port)
		+ "\nSequence Number: " + str(self.seq_num) + "\nACK Number: "
		+ str(self.ack_num) + "\nACK Flag: " + str(self.ack_flag) + "RST Flag: "
		+ str(self.rst_flag) + "\nSYN Flag: " + str(self.syn_flag) + "\nFIN Flag: "
		+ str(self.fin_flag) + "\nWindow Size: " + str(self.window_size)
		+ "\nHeader Checksum: " + str(self.header_checksum) + "\nData Checksum: "
		+ str(self.data_checksum))