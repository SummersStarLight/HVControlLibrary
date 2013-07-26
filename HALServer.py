import HVControlBoard
import socket
import select
import multiprocessing
import string

def handleCommands(strData,controlBoard,q,block=False):
	inputData =  string.split(strData)
	methodtoCall = getattr(controlBoard,inputData.pop(0))
	arguments=[]
	for x in inputData:
		arguments.append(float(x))
	q.put(methodtoCall(*arguments))
	
class HALServer:
	def __init__(self):
		HOST = '127.0.0.1'              # Symbolic name meaning all available interfaces
		PORTA = 3737              		# Arbitrary non-privileged port
		PORTB = 2828			  		# Arbitrary non-privileged port

		self.server_socket_plugin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket_plugin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket_plugin.bind((HOST, PORTA))
		self.server_socket_plugin.listen(5)
		print "Listening to plugin commands on port: " + str(PORTB)
		
		self.server_socket_trace = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket_trace.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket_trace.bind((HOST, PORTB))
		self.server_socket_trace.listen(5)
		print "Listening to tracing commands on port " + str(PORTB)
		self.HVBoard = HVControlBoard.HVControlBoard()
		self.myQueue = multiprocessing.Queue()

	def serve(self):
		read_list = [self.server_socket_trace, self.server_socket_plugin]
		while True:
			readable, writable, errored = select.select(read_list, [], [])
			for s in readable:
				if s is self.server_socket_trace:
					client_socket, address = self.server_socket_trace.accept()
					read_list.append(client_socket)
					#print "Connection from", address
				elif s is self.server_socket_plugin:
					client_socket, address = self.server_socket_plugin.accept()
					read_list.append(client_socket)
					#print "Connection from", address
				else:
					data = s.recv(1024)
					if data:
						#print data
						p = multiprocessing.Process(target=handleCommands, args=(data,self.HVBoard,self.myQueue))
						p.start()
						x = self.myQueue.get()
						s.send(str(x))
					else:
						s.close()
						read_list.remove(s)

if (__name__ == "__main__"):
	HALSer = HALServer()
	HALSer.serve()
