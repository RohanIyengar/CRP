Readme

Client Call:

python FTA-client.py <server IP> <server Port>

Server Call:

python FTA-server.py <server Port>

In client terminal after intial call, to connect the server to the client, type in "connect". This will initiate and complete the 3-way handshake.

In client terminal, type in "get <filename>" in order to start the get call which will obtain the file from the server. This consists of the send functionality. 

C:\Users\Sara\Documents\CRP>python FTA-client.py 10.0.0.10 1025
Controller Initialized
Starting FTA-Client
10.0.0.10
Not a valid IP Address of server

Command: connect
Connecting to CRP Server...
Send SYN packet
Send ACK packet

Command: get Test.txt
Download file from Server named Test.txt
GET: Test.txt
1
i: 1
Data: GET: Test.txt
GET: Test.txt
Received file:

The above code shows that the send code will correctly package the message.

The disconnect function can be called from the client terminal, and the terminate function can be called from the server terminal. Each will shut down the socket and show that our socket API works correctly.

C:\Users\Sara\Documents\CRP>python FTA-server.py 1025
Controller Initialized
Starting FTA-Server
10.0.0.10
Connection timed out
Connection timed out
Connection timed out
Connection timed out
Connection timed out
Connection timed out
Connection timed out
Connection timed out
Connection timed out
Send SYNACK packet
here

Command: terminate
Shutting down the FTA-Server
Server has been terminated.

C:\Users\Sara\Documents\CRP>python FTA-client.py 10.0.0.10 1025
Controller Initialized
Starting FTA-Client
10.0.0.10
Not a valid IP Address of server

Command: connect
Connecting to CRP Server...
Send SYN packet
Send ACK packet

Command: disconnect
Disconnecting client from server

Our window size can also be changed

C:\Users\Sara\Documents\CRP>python FTA-client.py 10.0.0.10 1025
Controller Initialized
Starting FTA-Client
10.0.0.10
Not a valid IP Address of server

Command: connect
Connecting to CRP Server...
Send SYN packet
Send ACK packet

Command: disconnect
Disconnecting client from server

C:\Users\Sara\Documents\CRP>python FTA-client.py 10.0.0.10 1025
Controller Initialized
Starting FTA-Client
10.0.0.10
Not a valid IP Address of server

Command: connect
Connecting to CRP Server...
Send SYN packet
Send ACK packet

Command: window 3
Changing window size to 3


As this functionality works, this shows that the STOP-and-Wait ARQ works as it can send the packets back and forth.

We can also handle out-of-order packets, corruption, and dropped packets.

We had some functionality for sliding window as in the code allowed for out of order packets to be removed from the send queue if an ack was received in that window.

As we cannot fully transfer files, we cannot show you any extensive tests. The code in the controller class can help show what we did and what we attempted to configure.
