import nmap

# nmScan = nmap.PortScanner()

# print(nmScan.scan('127.0.0.1', '21-443'))

# http://iltabiai.github.io/home%20automation/2015/09/11/npm-roommates.html

#First, you need a Postscanner object that will be used to do the scan
nm = nmap.PortScanner()
#You can then do a scan of all the IPV4 addresses provided by the network you are connected to
nm.scan(hosts = '192.168.1.0/24', arguments = '-sn')

# 88:19:08:2C:EE:BD

# possibly send a text, an email, some sort of alert when a specified mac address is connected

for host in nm.all_hosts():
    print(nm[host])

# for host in nm.all_hosts():
#     #If the status of an IP address is not down, print it
#     if nm[host]['status']['state'] != "down":
#         print ("STATUS:", nm[host]['status']['state'])
#         #Print the MAC address
#         try:
#             print ("MAC ADDRESS:", nm[host]['addresses']['mac'])
#         except:
#             mac = 'unknown'