INSTALLATION:
	-Windows
		download and install the following MSIs
			http://www.winpcap.org/install/bin/WinPcap_4_1_3.exe
			https://github.com/Kondziowy/scapy_win64/raw/master/win64/dnet-1.12.win-amd64-py2.7.exe
			https://github.com/Kondziowy/scapy_win64/raw/master/win64/pcap-1.1.win-amd64-py2.7.exe
			https://github.com/Kondziowy/scapy_win64/raw/master/win64/scapy-2.2.0.win-amd64.exe
			
	-Linux/Unix
		$ cd /tmp
		$ wget scapy.net
		$ unzip scapy-latest.zip
		$ cd scapy-2.*
		$ sudo python setup.py install
		
RUN:
	in driver file:
	
	import Listener
	Listener.start()

Installing matplotlib module
http://matplotlib.org/users/installing.html
