python-libfap
=============

Python ctypes bindings for libfap, the C port of the HAM::APRS::FAP Finnish APRS Parser

See <http://pakettiradio.net/libfap/> for more information and documentation on the libfap APRS parser.

See `example.py` for example usage.

Settings
--------

Before running `example.py`, you will need to configure your APRS login information in `settings.py`.

    APRS_SERVER_HOST = 'rotate.aprs2.net'
    APRS_SERVER_PORT = 14580
    APRS_USER = ''
    APRS_PASSCODE = ''

Compatibility
-------------

* Linux
* Mac OS X

`libfap.py` currently only looks for the libfap library with Linux and Mac OS X naming schemes. Windows may be able to find the library, but this is completely untested (if you have Windows available, it won't hurt to try).

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
