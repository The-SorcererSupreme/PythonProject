---------------------
*PYTHON NETCORMANCER*
---------------------
This is a network monitoring and manipulation tool built on Python and PHP. It uses a MySQL database (sqlinthesky) to store crucial data for the interface. The interface allows you to:
----------
#NEW Security
----------
There is an authentication process to call the website. It uses php sessions and a python script to try the credentials on the system and if it succeeds, access is granted.
----------
Dashboard
----------
- View interface throughput of a specific interface (e.g., enp0s3).
- List hosts connected to the LAN of the webserver (e.g., 192.168.178.0/24).
	- #NEW The network scan is faster because it manages the resources better and makes it also capable of scanning larger networks than /24
	- Scan for available ports on a specific host.
	- Spam the selected port with TCP segments.

----------
Sniffer
----------
- Capture packets in the LAN and view their sender and receiver IPs.

----------
Capturer
----------
N/A

----------
#NEW Special
----------
The special is a small shell with limited functions. Interactive commands, verbose commands and cli applications won't work.

*****************
Table of Contents
*****************
Installation
Usage
License
Bugs

*****************
Installation
*****************

You Need:
- Apache server:
	- Copy the PythonNetcromancer/html folder to an available site (e.g., /var/www/).
- MySQL server:
	- Create a database sqlinthesky using PythonNetcromancer/html/sql/createdb.sql
	- Add the user dbuser with the password vv2j@&T2zax@HhApm2 and grant all privileges on sqlinthesky.
- Python libraries:
	- Refer to install.txt
- Python:
	- Copy the PythonNetcromancer/python folder to your home directory of your webserver.
	*Note: You need to execute it manually.*
- Other:
	- Refer to install.txt

*****************
Usage
*****************
1. Access the website using your webserver.
2. Run main.py using sudo python3 <path_to_file>/main.py and enjoy!

------------------
THING TO CONSIDER:
------------------
1. Database size
You might want to clear the tblPacket an tblThroughput regularly using:
TRUNCATE TABLE tblThroughput;
TRUNCATE TABLE tblPacket;
(Don't forget USE sqlinthesky;)

2. Browser Cache
As the website is frequently talking to the webserver, the memory of the website fills up after a while. Press Ctrl+F5 to refresh with new memory

3. Hardcoded
Some elements, for example, IP-Addresses, are hardcoded, which means that you need to change the affected element. Here are some files you can look for hardcoded elements:
- traffic_analyser.py (IP addresses to be ignored in the sniffer)
- network_scanner.py (Interface which sends the ARP requests to update the Device Table on the Dashboard)

4. High Resource Usage
Depending on the available resources, the program will fail. It requires at least 8GB RAM and I recommend at least 8 CPUs

5. Security
The Security is not tested

*****************
Bugs
*****************
- Some devices will not (always) be found by the ARP scan; this happens when the script doesn't receive a response from the device.
- After a while, the graph starts to jump; the solution would be to implement socket communication, but that's out of the scope for this version
  These improvements include proper punctuation, formatting, and consistency throughout the README.
