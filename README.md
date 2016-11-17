# CRP
Implementing custom transport layer connection oriented protocol on top of UDP

File Transfer Application (FTA)

FTA is a simple client-server file transfer application which will use the CRP API which you have designed and implemented. This means that your FTA data will be carried in CRP messages which will be encapsulated in UDP packets. In other words, CRP will be implemented using the best-effort connectionless services of UDP sockets (instead of using TCP sockets or raw IP sockets). The FTA commands should be as follows: 


FTA SERVER

 

● Command-line: FTA-server X 

 	The command-line arguments are:

	X: the port number at which the FTA-server’s UDP socket should bind.

● Command: window W

	(only for projects that support pipelined and bi-directional transfers) 

	W: the maximum receiver’s window-size at the FTA-Server (in segments). 

● Command: terminate

	Shut-down FTA-Server gracefully.



FTA CLIENT

 

● Command-line: FTA-client A P 

 	The command-line arguments are:

           	A: the IP address of FTA-server

 	     P: the UDP port number of FTA-server

● Command: connect

	The FTA-client connects to the FTA-server. 

● Command: get F

	The FTA-client downloads file F from the server (if F exists in the same directory with the FTA-server program). 

● Command: post F

	The FTA-client uploads file F to the server (if F exists in the same directory with the FTA-client program).

	This feature will be treated as extra credit for up to 20 project points.

● Command: window W

	(only for projects that support configurable flow window)

	W: the maximum receiver’s window-size at the FTA-Client (in segments). 

● Command: disconnect

	The FTA-client terminates gracefully from the FTA-server. 

  