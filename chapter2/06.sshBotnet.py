import optparse
import pxssh

botNet = []

class Client:
	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password
		self.session = self.connect()

	def connect(self):
		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password)
			return s
		except Exception, e:
			print e
			print '[-] Error Connecting'

	def send_command(self, cmd):
		self.session.sendline(cmd)
		self.session.prompt()
		return self.session.before


def botnetCommand(command):
	for client in botNet:
		output = client.send_command(command)
		print '[*] Output from ' + client.host
		print '[+] ' + output.split('\r\n')[1] + '\n'

def addClient(host, user, password):
	client = Client(host, user, password)
	botNet.append(client)
	
def main():
	# addClient('10.10.10.110', 'root', 'toor')
	# addClient('10.10.10.120', 'root', 'toor')
	addClient('localhost', 'root', 'vagrant')

	botnetCommand('uname -v')
	botnetCommand('cat /etc/issue')

if __name__ == "__main__":
	main()