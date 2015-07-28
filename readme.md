# Violent Python

## Chapter 1: Introduction

| Filename      		| Explanation 
| ------------- 		| -------------
| 1.bannerChecker.py 	| Scans 192.168.95.[147-150] ports [21,22,25,80,110,443] looking for vulnerable banners (provided file parameter)
| 2.crack.py 	      	| Brute force cracking of /etc/passwd (passwords.txt) using dictionary (dictionaries/dictionary.txt)
| 3.crack_sha512.py 	| Dictionary cracking of /etc/shadow (shadow.txt) using all dictionaries (dictionaries/*.txt)
| 4.zipCrack.py 		| Brute forces the provided zip file (evil.zip) with a dictionary file (dictionaries/dictionary.txt)

## Chapter 2: Penetration Testing with Python

| Filename      		| Explanation 
| ------------- 		| -------------
| 1.portScan.py 		| Scans a target host (-H) for provided ports (-p)
| 2.nmapPortScan.py 	| Same as above, but uses nmap
| 3.sshCommand.py 		| Uses pexpect to remote ssh into localhost as root with password vagrant. If successful, returns the output of 'cat /etc/shadow | grep root'
| 4.sshBrute.py 		| Brute forces SSH attacks against a host (-H) as user (-u) with password dictionary (-F)
| 5.bruteKey.py 		| Brute forces SSH attacks against a host (-H) as user (-u) with pregenerated keys (-d)

## Misc


Useful Links:
* [Password lists](https://github.com/danielmiessler/SecLists)
* [Outdated PenTools](https://github.com/ChrisFernandez/PenTools)
* [Newer PenTools](https://github.com/HispaGatos/tools)
