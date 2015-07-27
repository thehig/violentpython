# import hashlib
import crypt 																# Crypto library
import glob																	# Directory scraping
import datetime 															# Getting the time

def testSHA512Pass(cipheredPassword, showDebug = False):

	cipheredChunks = cipheredPassword.split('$')

	hashingAlgorithm = cipheredChunks[1]
	salt = cipheredChunks[2]
	passwordOnly = cipheredChunks[3]
	
	hashCipher = "$" + str(hashingAlgorithm) + "$" + str(salt) + "$"

	if(showDebug):
		print "[*] Algorithm: 		"	+ hashingAlgorithm
		print "[*] Salt: 			"	+ salt
		print "[*] Password: 		"	+ passwordOnly
		print "[*] Cipher: 			"	+ hashCipher


	startTime = datetime.datetime.now()
	lastScan = datetime.datetime.now()
	wordsTried = 0															# Number of words tried in total
	wordsTriedSinceLastReset = 0											# Number of words tried this second

	
	for filename in glob.glob("dictionaries/*.txt"):						# Dictionaries are expected in a dictionaries subfolder, in plaintext format, with a single word per line
		dictFile = open(filename, 'r')
		lineCount = 0														# Number of lines in this dictionary

		for word in dictFile.readlines():
			lineCount += 1
			wordsTried += 1
			wordsTriedSinceLastReset += 1


			scanDelta = datetime.datetime.now() - lastScan					# Calculate scans per second
			if(scanDelta.total_seconds() >= 1):
				print "[*] Scanned " + str(wordsTriedSinceLastReset) + " per second (" + str(wordsTried) + ")"
				lastScan = datetime.datetime.now()
				wordsTriedSinceLastReset = 0
			
			word = word.strip('\n').strip('\r')								# Clean up the dictionary word (Remove newline)
			cipheredWord = crypt.crypt(word, hashCipher)					# Encrypt the word with the cipher			

			if(showDebug):
				print "[*] Trying '" + word + "':\t" + cipheredWord

			if(cipheredWord == cipheredPassword):
				print "[+] Found Password: " + word + "\n"
				return

		print "[*] Password not found in " + filename + " (" + str(lineCount) + ")"

	print "[-] Password not found in any dictionary provided"

	elapsed = datetime.datetime.now() - startTime
	print "[*] Ran for " + str(elapsed.total_seconds()) + " seconds"
	return

def main(targetFile = 'shadow.txt'):	
	print "[*] Opening " + targetFile
	for line in open(targetFile).readlines():
		if ":" in line:
			user = line.split(':')[0]
			cryptPass = line.split(':')[1].strip(' ')
			print "[*] Cracking Password For: " + user
			testSHA512Pass(cryptPass)

if __name__ == "__main__":
	main()