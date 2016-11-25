import sys
from CRP_Controller import CRP_Controller
from CRP_Socket_State import CRP_Socket_State
#import CRP

from socket import inet_aton

def connect():
	print "Connecting to CRP Server..."
	ip_addr, port = clientSocket.dst_addr
	CRP_Controller.clientSideConnect(clientSocket, ip_addr, port)

def get(file):
	print "Download file from Server named " + str(file)
	CRP_Controller.sendDataPacket(clientSocket)
	file_response = CRP_Controller.receiveDataPacket()
	print "Received file: ", file_response

def post(file):
	print "Uploading file to Server named " + str(file)

def disconnect():
	print "Disconnecting client from server"
	clientSocket.close()

def window(newSize):
	print "Changing window size to " + str(windowSize)
	clientSocket.rcv_window_size = newSize

def main():
	print "Starting FTA-Client"
	# check for number of correct command line arguments
	if len(sys.argv) != 3:
		print ('Please enter arguments in the correct format: A P' + 
			'\nA: The ip address of FTA-server'
			'\nP: The UDP port of the FTA-server')
		sys.exit()
	# port number at which the FxA-Server's UDP socket should be bound to
	try:
		portnumber = int(sys.argv[2])
	except:
		print 'Please enter a valid port number for Server (1025-65536)'
		sys.exit()

	# check for valid client port numbers
	if portnumber < 1025 or portnumber > 65536: 
		print 'Please enter a valid port number for server (1025-65536)'
		sys.exit()

	server_ip_addr = sys.argv[1]
	try:
		inet_aton(server_ip_addr)
	except:
		print "Not a valid IP Address of server"
		sys.exit()

	# Port number for client must be even
	#if portnumber % 2 != 1:
	#    print 'Port number for server must be odd'
	#    sys.exit()

	client_port = 49152
	# Need to get local host's IP Address
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect('8.8.8.8', 0)
	client_ip_address = s.getsockname()[0]
	# creating and binding rxp socket
	global clientSocket
	clientSocket = CRP_Controller.createAndBindSocket(client_ip_address, client_port)
	clientSocket.dst_addr = (server_ip_addr, portnumber)
	CRP_Controller.clientSideConnect(serverSocket)
	client_info = serverSocket.connectionsQueue.get

	terminated = False
	while not terminated:
		command = raw_input('\nCommand: ').split(" ")
		if len(command) > 2:
			print "Invalid Command. Refer to README for valid commands."

		if len(command) == 1:
			if command[0] == "disconnect":
				disconnect()
				sys.exit()
			elif command[0] == "connect":
				connect()
			else:
				print "Invalid Command. Refer to README for valid commands."

		elif len(command) == 2:
			if command[0] == "window":
				try:
					newSize = int(command[1])
				except:
					print "Non-Integer window size entered"
				window(newSize)
			elif command[0] == "get":
				file_name = str(command[1])
				get(file_name)
			elif command[0] == "post":
				file_name= str(command[1])
				post(file_name)
			else:
				print "Invalid Command. Refer to README for valid commands."