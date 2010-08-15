#!/bin/python
import socket

from libfap import *
import settings


# create socket & connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((settings.APRS_SERVER_HOST, settings.APRS_SERVER_PORT))

# logon
sock.send('user %s pass %s vers KD7LXL-Python 0.1 filter r/0/0/25000\n' % (settings.APRS_USER, settings.APRS_PASSCODE) )

sock_file = sock.makefile()
libfap.fap_init()
try:
    while 1:
        packet_str = sock_file.readline().strip()
        packet = libfap.fap_parseaprs(packet_str, len(packet_str), 0)
        print '%s' % (packet[0])
        libfap.fap_free(packet)
except KeyboardInterrupt:
    pass

libfap.fap_cleanup()

# close socket -- must be closed to avoid buffer overflow
sock.shutdown(0)
sock.close()
