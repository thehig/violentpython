import pxssh

def send_command(s, cmd):
	s.sendline(cmd)
	s.prompt()
	return s.before

def connect(host, user, password):
	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		return s
	except:
		print '[-] Error connecting'
		return

def main():
	host = 'localhost'
	user = 'root'
	password = 'vagrant'
	command = 'cat /etc/shadow | grep root'
	
	child = connect(host, user, password)									# Attempt to spawn an ssh shell on the remote host
	if child:
		result = send_command(child, command)								# Run the provided command
		for line in result.split('\r\n'):									# Print the results
			if len(line) > 0:
				print "[+]\t" + line
	else:
		print "[-] Could not get past password prompt."						# Shell did not spawn or log in properly
		exit(0)

if __name__ == "__main__":
	main()