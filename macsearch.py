import nmap
import time

# http://iltabiai.github.io/home%20automation/2015/09/11/npm-roommates.html

class Person:
    def __init__(self, name, MAC, disconnectedloops=-1):
        self.name = name
        self.disconnectedloops = disconnectedloops # make this -1
        self.MAC = MAC
        self.connection_time = -1
        self.disconnect_time = -1

known_macs = {
    '18:F1:D8:96:AC:AD' : 'Tucker',
    '88:19:08:2C:EE:BD' : 'Hayden',
    # '78:88:6D:BB:27:41' : 'Tucker\'s Ipad',
    '94:BF:2D:1D:E9:1A' : 'Eli'
}

people = []
connected_macs = []
active_people = []
away_people = []
# This var will hold the people who are connected. Add people to this if they show up as connected in "if person.MAC in connected_macs:" by using the "in" keyword
# Remove them if disconnected


for mac, name in known_macs.items():
    people.append(Person(name, mac))

away_people = people[:]

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


# Took 1:38 for 10 iterations
# need to figure out how I should remove people from active list when signal hasn't been received in a while
while True:
    nm.scan(hosts = '10.0.0.180/24', arguments = '-sn')


    connected_macs = []
    for host in nm.all_hosts():
        # print(nm[host])
        if (nm[host]['status']['state'] == "up"):
            try:
                mac = nm[host]['addresses']['mac']
            except:
                mac = 'unknown'

            # print("MAC {} is connected".format(mac))
            connected_macs.append(mac)

    # print('Post nmap search registered users in connected_macs on this iteration:\n')
    # for person in people:
    #     if person.MAC in connected_macs:
    #         print(person.name)
    # print()

    # The issue is that once you go into the active people list, you never get out.
    for person in people:
        if person.MAC in connected_macs:
            if time.time() - person.disconnect_time >= 120 or person.connection_time == -1:
                # start connected timer
                person.connection_time = time.time()

                # meaning they've been disconnected for a while or have never connected, so notify that they've connected
                # possibly send a text, an email, some sort of alert when a specified mac address is connected 

                person.disconnectedloops = 0

            if person not in active_people:
                person.connection_time = time.time()
                active_people.append(person)

            if person in away_people:
                away_people.remove(person)
        else:
            # Start disconnect timer ONLY if they're leaving the active people list, so that the disconnect is still -1
            # They must be connected for at least 2 minutes to be disconnected
            # if person in active_people and time.time() - person.connection_time >= 120:
                # person.disconnect_time = time.time()

            # Then remove them
            if person not in away_people and time.time() - person.connection_time >= 120:
                person.disconnect_time = time.time()
                active_people.remove(person)
                away_people.append(person)

    print('Connected Users:')
    for person in active_people:
        print('{} last pinged at {}'.format(person.name, time.ctime(person.connection_time)))

    print()

    print('Disconnected Users:')
    for person in away_people:
        if person.connection_time == -1 and person.disconnect_time == -1:
            print('{} has not connected since script began'.format(person.name))
        else:
            print('{} has been disconnected for {} seconds'.format(person.name, time.time() - person.disconnect_time))

    print()
    print()

    time.sleep(10)