import nmap

# http://iltabiai.github.io/home%20automation/2015/09/11/npm-roommates.html

class Person:
    def __init__(self, name, MAC, disconnectedloops=0):
        self.name = name
        self.disconnectedloops = disconnectedloops
        self.MAC = MAC

known_macs = {
    '18:F1:D8:96:AC:AD' : 'Tucker',
    '88:19:08:2C:EE:BD' : 'Hayden',
    # '78:88:6D:BB:27:41' : 'Tucker\'s Ipad',
    '94:BF:2D:1D:E9:1A' : 'Eli'
}

people = []
connected_macs = []
# This var will hold the people who are connected. Add people to this if they show up as connected in "if person.MAC in connected_macs:" by using the "in" keyword
# Remove them if disconnected
activeusers = []

for mac, name in known_macs.items():
    people.append(Person(name, mac))

print('Registered People:')
for person in people:
    print('Name: {:<10} MAC: {:<20}'.format(person.name, person.MAC))

print()
print()

#First, you need a Postscanner object that will be used to do the scan
nm = nmap.PortScanner()

#You can then do a scan of all the IPV4 addresses provided by the network you are connected to
# Change this to your machine's IPV4, could be 192.168.1...etc
# https://askubuntu.com/questions/377787/how-to-scan-an-entire-network-using-nmap

while True:
    print('top of loop...')
    nm.scan(hosts = '10.0.0.180/24', arguments = '-sn')

    for host in nm.all_hosts():
        # print(nm[host])
        if (nm[host]['status']['state'] == "up"):
            try:
                mac = nm[host]['addresses']['mac']
            except:
                mac = 'unknown'

            # print("MAC {} is connected".format(mac))
            connected_macs.append(mac)


    for person in people:
        if person.MAC in connected_macs:
            person.disconnectedloops = 0
            print('{} is connected'.format(person.name))
        else:
            person.disconnectedloops += 1
            print('{} has been disconnected for {} loops'.format(person.name, person.disconnectedloops))

    print()
    print()
# possibly send a text, an email, some sort of alert when a specified mac address is connected 