import socketserver

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	def __init__(self, server_address, RequestHandlerClass):
		self.allow_reuse_address = True
		socketserver.ThreadingMixIn.__init__(self)
		socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
