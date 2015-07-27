import pexpect

PROMPT = ['#', '>>>', '>', '\$\b']											# Regexes to match command prompts

def send_command(child, cmd):
	child.sendline(cmd)														# Send the command
	child.expect(PROMPT)													# Expect the prompt

	response = child.before.split('\r\n')									# Split the response into lines
	linecount = len(response)												# There should be 2 lines when no command output is returned
																			#	First line is the command that was sent
																			#	Last line is the prompt again
	if(linecount > 2):
		return "\r\n".join(response[1:linecount - 1])						# Strip the command and prompt, then rejoin the lines to return a coherent result
	return

def connect(user, host, password):
	ssh_newkey = 'Are you sure you want to continue connecting'				# Message to expect when connecting to a machine for the first time
	connStr = 'ssh ' + user + '@' + host									# Command to run eg: ssh root@localhost
	print "[*] Attempting to run '" + connStr + "'.."
	child = pexpect.spawn(connStr)					
	ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])		# Expect a timeout, ssh_newkey warning or password prompt

	if ret == 0: 															# Matches timeout, nothing we can do
		print '[-] Error Connecting'
		return
	if ret == 1: 															# Matches ssh_newkey
		child.sendline('yes')												# Send back 'yes' to the new key prompt
		ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])				# Expect the password prompt

		if ret == 0: 														# Matches timeout again, nothing we can do
			print '[-] Error Connecting'
			return

	print "[*] Got password prompt..\n[*] Sending password.."				# All other cases return, so we must be at the password prompt

	child.sendline(password)												# Send the password

	ret = child.expect([pexpect.TIMEOUT] + PROMPT)							# Expect the command prompt
	if ret > 0:																# Matched the prompt (0 would be timeout)
		print "[*] Got command prompt.."
		return child														# Return the connected child process

	return

def main():
	host = 'localhost'
	user = 'root'
	password = 'vagrant'
	command = 'cat /etc/shadow'
	
	child = connect(user, host, password)									# Attempt to spawn an ssh shell on the remote host
	if child:
		result = send_command(child, command)								# Run the provided command
		print "[+] Command: " + command
		for line in result.split('\r\n'):									# Print the results
			print "[+]\t" + line
	else:
		print "[-] Could not get past password prompt."						# Shell did not spawn or log in properly

if __name__ == "__main__":
	main()