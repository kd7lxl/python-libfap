#!/usr/bin/env python
import socket

from libfap import *
import settings


# create socket & connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((settings.APRS_SERVER_HOST, settings.APRS_SERVER_PORT))

# logon
# wa filter a/49/-125/45/-117
sock.send('user %s pass %s vers KD7LXL-Python 0.2 filter a/49/-125/45/-117\n' % (settings.APRS_USER, settings.APRS_PASSCODE) )

sock_file = sock.makefile()
libfap.fap_init()
try:
    while 1:
        packet_str = sock_file.readline()
        packet = Packet(packet_str)
        if packet.path_len > 0:
            try:
                print '%s %s %8.3f %8.3f %3.0f km/h %s' % (
              packet.src_callsign.ljust(9),
              ','.join(packet.path).ljust(40),
              packet.latitude or 0,
              packet.longitude or 0,
              packet.speed or 0,
              packet.body.rstrip(),
            )
            except ValueError, msg:
                print msg
                print packet.orig_packet
                raise ValueError(msg)
except KeyboardInterrupt:
    pass

libfap.fap_cleanup()

# close socket -- must be closed to avoid buffer overflow
sock.shutdown(0)
sock.close()
