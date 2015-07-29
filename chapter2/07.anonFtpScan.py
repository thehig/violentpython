import ftplib

def anonLogin(hostname):
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous', 'me@your.com')
		print "[*] " + str(hostname) + " FTP Anonymous Logon Succeeded."
		ftp.quit()
		return True
	except Exception, e:
		print "[-] " + str(hostname) + " FTP Anonymous Logon Failed."
		return False

def main():
	anonLogin('127.0.0.1')

if __name__ == "__main__":
	main()
