python-libfab
=============

Python ctypes bindings for libfap, the C port of the HAM::APRS::FAP Finnish APRS Parser

See <http://pakettiradio.net/libfap/> for more information and documentation on the libfap APRS parser.

See example.py for example usage.

Compatibility
-------------

This code currently only supports loading the libfap library if it is named with the Mac OS X naming scheme. If you are using Linux or Windows, you will need to change the line in libfap.py that loads the library to something like libfap.so on Linux or libfap.dll on Windows.

    libfap = cdll.LoadLibrary('libfap.dylib')

Once I have a chance to test other platforms, I plan to automatically detect the platform and load the appropriate library.