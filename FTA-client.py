import sys
#import CRP

from socket import inet_aton

def connect():
	print "Connecting to CRP Server..."

def get(file):
	print "Download file from Server named " + str(file)

def post(file):
	print "Uploading file to Server named " + str(file)

def disconnect():
	print "Disconnecting client from server"

def main():
	print "Blah"