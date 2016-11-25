import sys
from CRP_Controller import CRP_Controller
from CRP_Socket_State import CRP_Socket_State
import threading

from socket import inet_aton

windowSize = 1
threads = []
global CRP_Controller
CRP_Controller = CRP_Controller()

def window(newSize):
	print "Changing window size to " + str(windowSize)
	windowSize = newSize

def terminate():
	print "Shutting down the FTA-Server"
	CRP_Controller.closeSocket(serverSocket)

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

	# creating and binding rxp socket
	global serverSocket
	serverSocket = CRP_Controller.createAndBindSocket(ipaddress, portnumber)
	client_info = None # CRP_Controller.listen(serverSocket)
	CRP_Controller.serverSideAccept(serverSocket, client_info)
	""" Understand + Uncomment this later
	if serverSocket.state == CRP_Socket_State.CONNECTED:
		thread = threading.Thread()
		thread.start()
		threads.append(thread)
	"""

	terminated = False
	while not terminated:
		command = raw_input('\nCommand: ').split(" ")
		if len(command) > 2:
			print "Invalid Command. Refer to README for valid commands."

		if len(command) == 1:
			if command[0] == "terminate":
				termiante()

			for thread in threads:
				thread.join()
			sys.exit()

		elif len(command) == 2:
			if command[0] == "window":
				try:
					newSize = int(command[1])
				except:
					print "Non-Integer window size entered"
				window(newSize)
			else:
				print "Invalid Command. Refer to README for valid commands."

#main()