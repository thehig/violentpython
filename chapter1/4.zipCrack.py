import zipfile
from threading import Thread
import optparse

def extractFile(zFile, password):
	try:
		zFile.extractall(pwd=password)
		print "[+] Password Found " + password + "\n"
	except Exception, e:
		pass

def main():
	parser = optparse.OptionParser("%prog -f <zipfile> -d <dictionary>")
	parser.add_option('-f', dest='zname', type='string', help='specify zip file')
	parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
	(options, args) = parser.parse_args()

	if (options.zname == None) | (options.dname == None):
		print parser.usage
		exit(0)
	else:
		zname = options.zname
		dname = options.dname

	zFile = zipfile.ZipFile(zname)
	passFile = open(dname, 'r')

	for line in passFile.readlines():
		password = line.strip('\n').strip('\r')

		t = Thread(target=extractFile, args=(zFile, password))
		t.start()

if __name__ == '__main__':
	main()