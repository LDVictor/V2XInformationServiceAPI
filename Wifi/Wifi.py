import os
def getuphosts():
	os.system("fping -a -i 1 -r 0 -g 192.168.1.0/16 2>/dev/null > /tmp/uphosts &")
