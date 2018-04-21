from ctypes import *
from datetime import datetime

try:
    # Try loading linux library
    libfap = cdll.LoadLibrary('libfap.so')
except OSError:
    try:
        # Try loading Mac OS X library
        libfap = cdll.LoadLibrary('libfap.dylib')
    except OSError:
        try:
            # This might find the dll for Windows, but it has not been tested
            libfap = cdll.LoadLibrary('libfap')
        except OSError:
            raise OSError, 'Could not find libfap.'

time_t = c_long

fap_error_code_t = c_int
(
    fapPACKET_NO,
    fapPACKET_SHORT,
    fapPACKET_NOBODY,
    
    fapSRCCALL_NOAX25,
    fapSRCCALL_BADCHARS,
    
    fapDSTPATH_TOOMANY,
    fapDSTCALL_NONE,
    fapDSTCALL_NOAX25,
    
    fapDIGICALL_NOAX25,
    fapDIGICALL_BADCHARS,
    
    fapTIMESTAMP_INV_LOC,
    fapTIMESTAMP_INV_OBJ,
    fapTIMESTAMP_INV_STA,
    fapTIMESTAMP_INV_GPGGA,
    fapTIMESTAMP_INV_GPGLL,
    
    fapPACKET_INVALID,
    
    fapNMEA_INV_CVAL,
    fapNMEA_LARGE_EW,
    fapNMEA_LARGE_NS,
    fapNMEA_INV_SIGN,
    fapNMEA_INV_CKSUM,
    
    fapGPRMC_FEWFIELDS,
    fapGPRMC_NOFIX,
    fapGPRMC_INV_TIME,
    fapGPRMC_INV_DATE,
    fapGPRMC_DATE_OUT,
    
    fapGPGGA_FEWFIELDS,
    fapGPGGA_NOFIX,
    
    fapGPGLL_FEWFIELDS,
    fapGPGLL_NOFIX,
    
    fapNMEA_UNSUPP,
    
    fapOBJ_SHORT,
    fapOBJ_INV,
    fapOBJ_DEC_ERR,
    
    fapITEM_SHORT,
    fapITEM_INV,
    fapITEM_DEC_ERR,
    
    fapLOC_SHORT,
    fapLOC_INV,
    fapLOC_LARGE,
    fapLOC_AMB_INV,
    
    fapMICE_SHORT,
    fapMICE_INV,
    fapMICE_INV_INFO,
    fapMICE_AMB_LARGE,
    fapMICE_AMB_INV,
    fapMICE_AMB_ODD,
    
    fapCOMP_INV,
    fapCOMP_SHORT,
    
    fapMSG_INV,
    
    fapWX_UNSUPP,
    fapUSER_UNSUPP,
    
    fapDX_INV_SRC,
    fapDX_INF_FREQ,
    fapDX_NO_DX,
    
    fapTLM_INV,
    fapTLM_LARGE,
    fapTLM_UNSUPP,
    
    fapEXP_UNSUPP,
    fapSYM_INV_TABLE,
    
    fapNOT_IMPLEMENTED,
    fapNMEA_NOFIELDS,
    
    fapNO_APRS
) = map(c_int, xrange(63))

# fap_packet_type_t
(
    fapLOCATION,
	fapOBJECT,
	fapITEM,
	fapMICE,
	fapNMEA,
    
	fapWX,
	fapMESSAGE,
	fapCAPABILITIES,
	fapSTATUS,
	fapTELEMETRY,
	fapTELEMETRY_MESSAGE,
	fapDX_SPOT,
    
	fapEXPERIMENTAL
) = map(c_int, xrange(13))

# fap_pos_format_t
(
    fapPOS_COMPRESSED,
	fapPOS_UNCOMPRESSED,
	fapPOS_MICE,
	fapPOS_NMEA
) = map(c_int, xrange(4))

class fap_wx_report_t(Structure):
    _fields_ = [
        ('wind_gust', POINTER(c_double)),
        ('wind_dir', POINTER(c_uint)),
        ('wind_speed', POINTER(c_double)),
        
        ('temp', POINTER(c_double)),
        ('temp_in', POINTER(c_double)),
        ('rain_1h', POINTER(c_double)),
        ('rain_24h', POINTER(c_double)),
        ('rain_midnight', POINTER(c_double)),
        
        ('humidity', POINTER(c_uint)),
        ('humidity_in', POINTER(c_uint)),
        
        ('pressure', POINTER(c_double)),
        ('luminosity', POINTER(c_uint)),
        
        ('snow_24h', POINTER(c_double)),
        
        ('soft', c_char_p),
    ]

class fap_telemetry_t(Structure):
    _fields_ = [
        ('seq', POINTER(c_uint)),
        ('val1', POINTER(c_double)),
        ('val2', POINTER(c_double)),
        ('val3', POINTER(c_double)),
        ('val4', POINTER(c_double)),
        ('val5', POINTER(c_double)),
        
        ('bits', c_byte * 8),
    ]

class fap_packet_t(Structure):
    _fields_ = [
        ('error_code', POINTER(fap_error_code_t)), # POINTER(fap_error_code_t)
        ('type', POINTER(c_int)), # POINTER(fap_packet_type_t)
        
        ('orig_packet', c_char_p),
        ('orig_packet_len', c_uint),
        
        ('header', c_char_p),
        ('body', c_char_p),
        ('body_len', c_uint),
        ('src_callsign', c_char_p),
        ('dst_callsign', c_char_p),
        ('path', POINTER(c_char_p)),
        ('path_len', c_uint),
        
        ('latitude', POINTER(c_double)),
        ('longitude', POINTER(c_double)),
        ('format', POINTER(c_int)), # POINTER(fap_pos_format_t)
        ('pos_resolution', POINTER(c_double)),
        ('pos_ambiguity', POINTER(c_uint)),
        ('dao_datum_byte', c_byte),
        
        ('altitude', POINTER(c_double)),
        ('course', POINTER(c_uint)),
        ('speed', POINTER(c_double)),
        
        ('symbol_table', c_byte),
        ('symbol_code', c_byte),
        
        ('messaging', POINTER(c_short)),
        ('destination', c_char_p),
        ('message',c_char_p ),
        ('message_ack', c_char_p),
        ('message_nack', c_char_p),
        ('message_id', c_char_p),
        
        ('comment', c_char_p),
        ('comment_len', c_uint),
        
        ('object_or_item_name', c_char_p),
        ('alive', POINTER(c_short)),
        
        ('gps_fix_status', POINTER(c_short)),
        ('radio_range', POINTER(c_uint)),
        ('phg', c_char_p),
        ('timestamp', POINTER(time_t)),
        ('raw_timestamp', c_char_p),
        ('nmea_checksum_ok', POINTER(c_short)),
        
        ('wx_report', POINTER(fap_wx_report_t)),
        
        ('telemetry', POINTER(fap_telemetry_t)),
        
        ('messagebits', c_char_p),
        ('status', c_char_p),
        ('status_len', c_uint),
        ('capabilities', POINTER(c_char_p)),
        ('capabilities_len', c_uint),
    ]

    def get_timestamp(self):
        return datetime.fromtimestamp(self.timestamp.contents)
    
    def __repr__(self):
        return '%s(\'%s:%s\')' % (self.__class__.__name__, self.header, self.body)

libfap.fap_parseaprs.restype = POINTER(fap_packet_t)

libfap.fap_explain_error.argtypes = [fap_error_code_t, c_char_p]
libfap.fap_explain_error.restype = None

libfap.fap_mice_mbits_to_message.argtypes = [c_char_p, c_char_p]
libfap.fap_mice_mbits_to_message.restype = None

libfap.fap_distance.argtypes = [c_double, c_double, c_double, c_double]
libfap.fap_distance.restype = c_double

libfap.fap_direction.argtypes = [c_double, c_double, c_double, c_double]
libfap.fap_direction.restype = c_double

libfap.fap_count_digihops.argtypes = [POINTER(fap_packet_t)]
libfap.fap_count_digihops.restype = c_int

libfap.fap_check_ax25_call.argtypes = [c_char_p, c_short]
libfap.fap_check_ax25_call.restype = c_char_p

libfap.fap_kiss_to_tnc2.argtypes = [c_char_p, c_uint, c_char_p, c_uint, POINTER(c_uint)]
libfap.fap_kiss_to_tnc2.restype = c_int

libfap.fap_tnc2_to_kiss.argtypes = [c_char_p, c_uint, c_uint, c_char_p, c_uint]
libfap.fap_tnc2_to_kiss.restype = c_int

libfap.fap_ax25_to_tnc2.argtypes = [c_char_p, c_uint, c_char_p, c_uint]
libfap.fap_ax25_to_tnc2.restype = c_int

libfap.fap_tnc2_to_ax25.argtypes = [c_char_p, c_uint, c_char_p, c_uint]
libfap.fap_tnc2_to_ax25.restype = c_int

libfap.fap_free.argtypes = [POINTER(fap_packet_t)]
