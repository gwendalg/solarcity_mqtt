Solarcity Gateway to MQTT Bridge
================================

This is a little project that monitors a Solar City gateway, and passes along instantaneous and total demand messages to a Mosquitto server.

Configuration is in `server.ini`; an example file is in `server.ini.sample`.

It requires the `paho-mqtt` Python module.

To run:

```
# Gather data in a directory:
# using a smart switch where the port of the gateway is spied upon
sudo tcpflow -o solar_city -i p121p1 -e http host sg.solarcity.com

# using a router with tcpdump installed:
ssh root@192.168.1.1 tcpdump -i vlan2 -s 65535 -w -  host sg.solarcity.com | tcpflow -r - -e http  -o solar_city

python runner.py server.ini
```
