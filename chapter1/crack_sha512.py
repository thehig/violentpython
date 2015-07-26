# import hashlib
import crypt
import glob

def testSHA512Pass(cryptpass):
	# $6$ms32yIGN$NyXj0YofkK14MpRwFHvXQW0yvUid.slJtgxHE2EuQqgD74S/ GaGGs5VCnqeC.bS0MzTf/EFS3uspQMNeepIAc.

	original = cryptpass

	line = cryptpass.split('$')

	hashingAlgo = line[1]
	salt = line[2]
	cryptpass = line[3]
	
	cryptcypher = "$" + str(hashingAlgo) + "$" + str(salt) + "$"

	# print "\tAlgorithm: " + hashingAlgo + "\n\tSalt: " + salt + "\n\tPass: " + cryptpass + "\n\tCipher: " + cryptcypher
	for filename in glob.glob("dictionaries/*.txt"):

		dictFile = open(filename, 'r')
		counter = 0

		for word in dictFile.readlines():
			counter += 1
			if counter % 500 == 0:
				print "[*] " + str(counter)
			word = word.strip('\n')
			word = word.strip('\r')

			cryptword = crypt.crypt(word, cryptcypher)
			# print "[*] Trying '" + word + "':\t" + cryptword

			if(cryptword == original):
				print "[+] Found Password: "+word+"\n"
				return
		print "[-] Password not found in " + filename + " (" + str(counter) + ")"
	print "[-] Password not found in any dictionary provided"
	return

def main():
	passFile = open('shadow.txt')
	for line in passFile.readlines():
		if ":" in line:
			user = line.split(':')[0]
			cryptPass = line.split(':')[1].strip(' ')
			print "[*] Cracking Password For: " + user
			testSHA512Pass(cryptPass)

if __name__ == "__main__":
	main()