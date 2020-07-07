import nmap

# http://iltabiai.github.io/home%20automation/2015/09/11/npm-roommates.html

known_macs = {
    '18:F1:D8:96:AC:AD' : 'Tucker',
    '88:19:08:2C:EE:BD' : 'Hayden'
}

connected_macs = []

#First, you need a Postscanner object that will be used to do the scan
nm = nmap.PortScanner()
#You can then do a scan of all the IPV4 addresses provided by the network you are connected to
nm.scan(hosts = '192.168.1.0/24', arguments = '-sn')

# possibly send a text, an email, some sort of alert when a specified mac address is connected

for index, host in enumerate(known_macs):
    # print(index)
    print(host)

print()

for host in nm.all_hosts():
    print(nm[host])
    if (nm[host]['status']['state'] == "up"):
        try:
            mac = nm[host]['addresses']['mac']
        except:
            # continue
            mac = 'unknown'

        print("mac {} is connected".format(mac))
        connected_macs.append(mac)
        
# for mac in connected_macs:
#     if mac in known_macs:
#         print("{} is connected".format(known_macs[mac]))