# -*- encoding=utf-8 -*-
from ctypes import *
import platform
import os

if platform.system() == u'Windows':
    internal_library = cdll.msvcrt
else:
    sdk_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                            'sdk/libarcsoft_fsdk_face_detection.so')
    internal_library = CDLL(sdk_path)

malloc = internal_library.malloc
free = internal_library.free
memcpy = internal_library.memcpy

malloc.restype = c_void_p
malloc.argtypes = (c_size_t,)
free.restype = None
free.argtypes = (c_void_p,)
memcpy.restype = c_void_p
memcpy.argtypes = (c_void_p, c_void_p, c_size_t)
