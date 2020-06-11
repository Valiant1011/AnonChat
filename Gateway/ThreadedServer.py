import socketserver

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass