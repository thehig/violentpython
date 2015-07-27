import crypt

def testPass(cryptPass):
	salt = cryptPass[0:2]
	dictFile = open('dictionaries/dictionary.txt', 'r')
	for word in dictFile.readlines():
		word = word.strip('\n')
		word = word.strip('\r')
		# print "[*] Trying '" + word + "'\n"
		cryptWord = crypt.crypt(word, salt)
		if(cryptWord == cryptPass):
			print "[+] Found Password: "+word+"\n"
			return
	print "[-] Password Not Found.\n"
	return

def main():
	passFile = open('2.passwords.txt')
	for line in passFile.readlines():
		if ":" in line:
			user = line.split(':')[0]
			cryptPass = line.split(':')[1].strip(' ')
			print "[*] Cracking Password For: " + user
			testPass(cryptPass)

if __name__ == "__main__":
	main()