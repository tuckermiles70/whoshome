import nmap
import time

from emailtest import em_send
from config import known_macs

class Person:
    def __init__(self, name, MAC):
        self.name = name
        self.MAC = MAC
        self.connection_time = -1
        self.disconnect_time = -1


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
print('-----------------------------------------------------------------------')
print()

#First, you need a Postscanner object that will be used to do the scan
nm = nmap.PortScanner()

# Change this to your machine's IPV4, could be 192.168.1...etc


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

            connected_macs.append(mac)

    for person in people:
        if person.MAC in connected_macs:
            if time.time() - person.disconnect_time >= 120 or person.connection_time == -1:
                # start connected timer
                person.connection_time = time.time()

                person.disconnectedloops = 0

            if person not in active_people:
                person.connection_time = time.time()
                active_people.append(person)

                # I only want to send this if person has been disconnected for a while
                em_send(person.name)

            if person in away_people:
                away_people.remove(person)
        else:
            # Start disconnect timer ONLY if they're leaving the active people list, so that the disconnect is still -1
            # They must be connected for at least 2 minutes to be disconnected

            # Then remove them
            if person not in away_people and time.time() - person.connection_time >= 120:
                person.disconnect_time = time.time()
                active_people.remove(person)
                away_people.append(person)

    print('Connected Users:')
    if active_people:
        for person in active_people:
            print('{:<10} last pinged on {}'.format(person.name, time.ctime(person.connection_time)))
    else:
        print('None')

    print()

    print('Disconnected Users:')
    if away_people:
        for person in away_people:
            if person.connection_time == -1 and person.disconnect_time == -1:
                print('{:<10} has not connected since script began'.format(person.name))
            else:
                print('{:<10} has been disconnected for {:.2f} seconds'.format(person.name, time.time() - person.disconnect_time))
    else:
        print('None')

    print()
    print('-----------------------------------------------------------------------')
    print()

    time.sleep(10)