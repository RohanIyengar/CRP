import sys
from CRP_Controller import CRP_Controller
from CRP_Socket_State import CRP_Socket_State
import threading

import socket

windowSize = 1
threads = []
global CRP_Controller
CRP_Controller = CRP_Controller()

def window(newSize):
	print "Changing window size to " + str(windowSize)
	windowSize = newSize

def terminate():
	print "Shutting down the FTA-Server"
	CRP_Controller.closeServer(serverSocket)


def listenThread():
	#print "Listening for client requests..."
	while 1:
		request = CRP_Controller.recvDataPacket(serverSocket, 1024)
		if "GET" in str(request):
			file_name = str(request).replace("GET: ", "")
			print "Getting file", file_name

			with open (file_name, "r") as newFile:
				fileData = newFile.read()
			CRP_Controller.sendDataPacket(fileData)
		if "POST" in str(request):
			#Todo
			pass

def main():
	print "Starting FTA-Server"
	# check for number of correct command line arguments
	if len(sys.argv) != 2:
		print ('Please enter arguments in the correct format: X' + 
			'\nX: The port number this server should bind to')
		sys.exit()
	# port number at which the FxA-Server's UDP socket should bind to
	try:
		portnumber = int(sys.argv[1])
	except:
		print 'Please enter a valid port number for Server (1025-65536)'
		sys.exit()
	windowSize = 1

	# check for valid client port numbers
	if portnumber < 1025 or portnumber > 65536: 
		print 'Please enter a valid port number for client (1025-65536)'
		sys.exit()

	# Port number for client must be even
	#if portnumber % 2 != 1:
	#    print 'Port number for server must be odd'
	#    sys.exit()


	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 2016))
	ipaddress = s.getsockname()[0]
	print ipaddress
	# creating and binding rxp socket
	global serverSocket
	client_info = None
	serverSocket = CRP_Controller.createAndBindSocket(ipaddress, portnumber)
	while client_info is None:
		client_info = CRP_Controller.listenForConnection(serverSocket, 1)
		# client_info = serverSocket.connectionsQueue.get()
		# print str(serverSocket.connectionsQueue.qsize())

	try:
		CRP_Controller.serverSideAccept(serverSocket, client_info)
	except (UnboundLocalError, Exception):
		print "Client did not connect within 1000 tries"
		sys.exit()
	if serverSocket.state == CRP_Socket_State.CONNECTED:
		thread = threading.Thread(target = listenThread)
		thread.start()
		threads.append(thread)

	terminated = False
	while not terminated:
		command = raw_input('\nCommand: ').split(" ")
		if len(command) > 2:
			print "Invalid Command. Refer to README for valid commands."

		if len(command) == 1:
			if command[0] == "terminate":
				terminate()
				# for thread in threads:
				# 	thread.exit()
				sys.exit()
			else:
				print "Invalid Command. Refer to README for valid commands."

		elif len(command) == 2:
			if command[0] == "window":
				try:
					newSize = int(command[1])
				except:
					print "Non-Integer window size entered"
				window(newSize)
			else:
				print "Invalid Command. Refer to README for valid commands."

main()