# -*- encoding=utf-8 -*-
from . import MRECT, ASVLOFFSCREEN
from .fa_clibrary import *


# 定义年龄检测结果信息
class ASAE_FSDK_AGERESULT(Structure):
    _fields_ = [(u'pAgeResultArray', POINTER(c_int32)), (u'lFaceNumber', c_int32)]


# 定义脸部信息
class ASAE_FSDK_AGEFACEINPUT(Structure):
    _fields_ = [(u'pFaceRectArray', POINTER(MRECT)), (u'pFaceOrientArray', POINTER(c_int32)),
                (u'lFaceNumber', c_int32)]


# 定义版本信息
class ASAE_FSDK_VERSION(Structure):
    _fields_ = [(u'lCodebase', c_int32), (u'lMajor', c_int32), (u'lMinor', c_int32), (u'lBuild', c_int32),
                (u'Version', c_char_p), (u'BuildDate', c_char_p), (u'CopyRight', c_char_p)]


# 定义脸部角度的检测范围
ASAE_FSDK_OPF_0_ONLY = 0x1  # 0; 0; ...
ASAE_FSDK_OPF_90_ONLY = 0x2  # 90; 90; ...
ASAE_FSDK_OPF_270_ONLY = 0x3  # 270; 270; ...
ASAE_FSDK_OPF_180_ONLY = 0x4  # 180; 180; ...
ASAE_FSDK_OPF_0_HIGHER_EXT = 0x5  # 0; 90; 270; 180; 0; 90; 270; 180; ...

# 定义人脸检测结果中的人脸角度
ASAE_FSDK_FOC_0 = 0x1  # 0 degree
ASAE_FSDK_FOC_90 = 0x2  # 90 degree
ASAE_FSDK_FOC_270 = 0x3  # 270 degree
ASAE_FSDK_FOC_180 = 0x4  # 180 degree
ASAE_FSDK_FOC_30 = 0x5  # 30 degree
ASAE_FSDK_FOC_60 = 0x6  # 60 degree
ASAE_FSDK_FOC_120 = 0x7  # 120 degree
ASAE_FSDK_FOC_150 = 0x8  # 150 degree
ASAE_FSDK_FOC_210 = 0x9  # 210 degree
ASAE_FSDK_FOC_240 = 0xa  # 240 degree
ASAE_FSDK_FOC_300 = 0xb  # 300 degree
ASAE_FSDK_FOC_330 = 0xc  # 330 degree

ASAE_FSDK_InitAgeEngine = internal_library.ASAE_FSDK_InitAgeEngine
ASAE_FSDK_UninitAgeEngine = internal_library.ASAE_FSDK_UninitAgeEngine
ASAE_FSDK_AgeEstimation_StaticImage = internal_library.ASAE_FSDK_AgeEstimation_StaticImage
ASAE_FSDK_AgeEstimation_Preview = internal_library.ASAE_FSDK_AgeEstimation_Preview
ASAE_FSDK_GetVersion = internal_library.ASAE_FSDK_GetVersion

ASAE_FSDK_InitAgeEngine.restype = c_long
ASAE_FSDK_InitAgeEngine.argtypes = (c_char_p, c_char_p, c_void_p, c_int32, POINTER(c_void_p))
ASAE_FSDK_UninitAgeEngine.restype = c_long
ASAE_FSDK_UninitAgeEngine.argtypes = (c_void_p,)
ASAE_FSDK_AgeEstimation_StaticImage.restype = c_long
ASAE_FSDK_AgeEstimation_StaticImage.argtypes = (
    c_void_p, POINTER(ASVLOFFSCREEN), POINTER(ASAE_FSDK_AGEFACEINPUT), POINTER(ASAE_FSDK_AGERESULT))
ASAE_FSDK_GetVersion.restype = POINTER(ASAE_FSDK_VERSION)
ASAE_FSDK_GetVersion.argtypes = (c_void_p,)
