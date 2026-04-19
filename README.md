The following is a SDN Mininet project, that observes the incoming traffic, sets a hard limit and marks any activity over that limit as suspicious (limit set to 20 here). The host that acts suspiciously is blocked. In our demonstration, we verify this using ping commands.

Setup:

Install mininet-

In your linux terminal, run:

sudo apt update
sudo apt install mininet

Install POX-

git clone https://github.com/noxrepo/pox
cd pox

Navigate to ~pox/pox/misc and place the "CN_SDN.py" file in that location.

Open two terminals, one for the SDN controller and one for mininet

In terminal 1, run - ./pox.py log.level --DEBUG misc.CN_SDN
Then, wait

In terminal 2, run - sudo mn --topo single,3 --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow10, verify connections using pingall (you should see 0% packet drop rate)

Testing:

To test normal behaviour, run a normal ping (within the limits) from h1 to h2 - h1 ping -c 5 -s 56 h2
To test the blocking, run - h1 ping -c 10 -s 1000 h2

To view the flow tables, open another terminal and type - sudo ovs-ofctl dump-flows s1 -O OpenFlow10

