If there are any problems installing or running GeoSniff, please contact gbourq3@lsu.edu for help.

Requirements:
Python 2.7

This product uses IP2Location LITE data available from http://lite.ip2location.com.
The IP2Location LITE database is not packaged with this software. You must agree to the terms of use yourself
and download the free database DB11.LITE. The file IP2LOCATION-LITE-DB11.BIN must be in the same folder as
the rest of the code.

Installing required modules for packet sniffing:
	- Windows
		Download and install the following executables:
			http://www.winpcap.org/install/bin/WinPcap_4_1_3.exe
			https://github.com/Kondziowy/scapy_win64/raw/master/win64/dnet-1.12.win-amd64-py2.7.exe
			https://github.com/Kondziowy/scapy_win64/raw/master/win64/pcap-1.1.win-amd64-py2.7.exe
			https://github.com/Kondziowy/scapy_win64/raw/master/win64/scapy-2.2.0.win-amd64.exe

	- Linux/Unix
		$ cd /tmp
		$ wget scapy.net
		$ unzip scapy-latest.zip
		$ cd scapy-2.*
		$ sudo python setup.py install

	- OS X
		$ brew install --with-python libdnet
		(may need to follow additional instructions to complete libdnet installation)
		$ pip install pcapy
		$ pip install scapy

Installing wxPython (wxPython 3.0 for Python 2.7):
	http://wxpython.org/download.php

Installing pySlip (must use GitHub version):
	https://github.com/rzzzwilson/pySlip
	`$ python setup.py install`

Installing matplotlib module:
	http://matplotlib.org/users/installing.html

Once all of the requirements are satisfied, you should be able to run the program:
`$ python GeoSniff.py`