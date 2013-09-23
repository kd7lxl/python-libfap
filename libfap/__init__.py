from libfap import *

Version = '0.2'

libfap.fap_init()

class OldPacket(dict):
    def __init__(self, packet_str):
        packet = libfap.fap_parseaprs(packet_str, len(packet_str), 0)
        # try:
        #     print 'Error:', libfap.fap_explain_error(packet[0].error_code[0])
        # except ValueError:
        #     pass
        
        for attr in dir(packet[0]):
            if attr == 'timestamp':
                self[attr] = datetime.fromtimestamp(packet[0].timestamp[0])
            elif attr == 'telemetry':
                print attr, name, dir(packet[0].__getattribute__(attr))
            elif attr == 'wx_report':
                print attr, name, dir(packet[0].__getattribute__(attr)[0])
            elif attr[0] != '_':
                name = type(packet[0].__getattribute__(attr)).__name__
                if name in ('str', 'int', 'long', 'NoneType'):
                    # ctypes properly converted these types, simply assign them
                    self[attr] = packet[0].__getattribute__(attr)
                elif name in ('LP_c_short', 'LP_c_double', 'LP_c_char_p', 'LP_c_uint', 'LP_c_int', 'LP_c_long'):
                    # NULL pointers will be False
                    if bool(packet[0].__getattribute__(attr)) is False:
                        self[attr] = None
                    # Try to resolve all other pointers
                    else:
                        try:
                            self[attr] = packet[0].__getattribute__(attr)[0]
                        except ValueError, msg:
                            print 'ERROR:', msg, attr, name, packet[0].__getattribute__(attr)
                # elif name == 'instancemethod':
                #     print attr, type(packet[0].__getattribute__(attr)())
                else:
                    print attr, name, packet[0].__getattribute__(attr)
        
        # print '%s' % (packet[0])
        libfap.fap_free(packet)
    
    # def __repr__(self):
    #     return '%s(\'%s:%s\')' % (self.__class__.__name__, self['header'], self['body'])
