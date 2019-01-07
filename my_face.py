import time

from lib import fd_clibrary, fg_clibrary, fa_clibrary
from lib.face_detect_sdk_library import *
from lib.face_age_sdk_library import *
from lib.face_gender_sdk_library import *
from util import image_loader
from conf.config import *

APP_ID = c_char_p(bytes(config.get('arcsoft', 'APP_ID'), encoding='utf-8'))
FD_SDK_KEY = c_char_p(bytes(config.get('arcsoft', 'FD_SDK_KEY'), encoding='utf-8'))
FASE_SDK_KEY = c_char_p(bytes(config.get('arcsoft', 'FASE_SDK_KEY'), encoding='utf-8'))
FSGE_SDK_KEY = c_char_p(bytes(config.get('arcsoft', 'FSGE_SDK_KEY'), encoding='utf-8'))

WORKBUF_SIZE = 20 * 1024 * 1024
MAX_FACE_NUM = 50
bUseYUVFile = False
bUseBGRToEngine = True

fd_engine = None
fa_engine = None
fg_engine = None


def init_face_engine():
    global fd_engine
    fd_work_memery = fd_clibrary.malloc(c_size_t(WORKBUF_SIZE))
    fd_engine = c_void_p()
    ret = AFD_FSDK_InitialFaceEngine(APP_ID, FD_SDK_KEY, fd_work_memery, c_int32(WORKBUF_SIZE), byref(fd_engine),
                                     AFD_FSDK_OPF_0_HIGHER_EXT, 32, MAX_FACE_NUM)

    if ret != 0:
        fd_clibrary.free(fd_work_memery)
        print(u'AFD_FSDK_InitialFaceEngine ret 0x{:x}'.format(ret))
        exit(0)


def init_face_age_engine():
    global fa_engine
    fa_work_memery = fa_clibrary.malloc(c_size_t(WORKBUF_SIZE))
    fa_engine = c_void_p()
    ret = ASAE_FSDK_InitAgeEngine(APP_ID, FASE_SDK_KEY, fa_work_memery, c_int32(WORKBUF_SIZE), byref(fa_engine))
    if ret != 0:
        fa_clibrary.free(fa_work_memery)
        print(u'ASAE_FSDK_InitAgeEngine ret 0x{:x}'.format(ret))
        exit(0)


def init_face_gender_engine():
    global fg_engine
    fg_work_memery = fg_clibrary.malloc(c_size_t(WORKBUF_SIZE))
    fg_engine = c_void_p()
    ret = ASGE_FSDK_InitGenderEngine(APP_ID, FSGE_SDK_KEY, fg_work_memery, c_int32(WORKBUF_SIZE), byref(fg_engine))
    if ret != 0:
        fg_clibrary.free(fg_work_memery)
        print(u'ASGE_FSDK_InitGenderEngine ret 0x{:x}'.format(ret))
        exit(0)


def do_face_detection(fd_engine, image):
    face_res = POINTER(AFD_FSDK_FACERES)()
    ret = AFD_FSDK_StillImageFaceDetection(fd_engine, byref(image), byref(face_res))

    if ret != 0:
        print(u'AFD_FSDK_StillImageFaceDetection 0x{0:x}'.format(ret))
        return 0, [], []

    faces = face_res.contents
    face_num = faces.nFace
    print('{} 个人脸'.format(face_num))

    if face_num > 0:
        return face_num, faces.rcFace, faces.lfaceOrient


def do_face_age_estimation(fa_engine, image, age_face_input, age_result):
    ret = ASAE_FSDK_AgeEstimation_StaticImage(fa_engine, byref(image), byref(age_face_input),
                                              byref(age_result))

    if ret != 0:
        print(u'ASAE_FSDK_AgeEstimation_StaticImage 0x{0:x}'.format(ret))
        return []

    return age_result


def do_face_gender_estimation(fg_engine, image, gender_face_input, gender_result):
    ret = ASGE_FSDK_GenderEstimation_StaticImage(fg_engine, byref(image), byref(gender_face_input),
                                                 byref(gender_result))
    if ret != 0:
        print(u'ASGE_FSDK_GenderEstimation_StaticImage 0x{0:x}'.format(ret))
        return []
    return gender_result


def main():
    init_face_engine()
    init_face_age_engine()
    init_face_gender_engine()

    start_time = time.time()
    file_path = '001.jpg'
    image = image_loader.load_image(bUseBGRToEngine, file_path)

    # 1. detect
    face_num, rect_info, orient_info = do_face_detection(fd_engine, image)

    # 2. age
    age_face_input = ASAE_FSDK_AGEFACEINPUT()
    age_face_input.lFaceNumber = face_num
    age_face_input.pFaceRectArray = rect_info
    age_face_input.pFaceOrientArray = orient_info
    age_result = ASAE_FSDK_AGERESULT()

    age_info = do_face_age_estimation(fa_engine, image, age_face_input, age_result)

    # 3. gender
    gender_face_input = ASGE_FSDK_GENDERFACEINPUT()
    gender_face_input.lFaceNumber = face_num
    gender_face_input.pFaceRectArray = rect_info
    gender_face_input.pFaceOrientArray = orient_info
    gender_result = ASGE_FSDK_GENDERRESULT()
    gender_info = do_face_gender_estimation(fg_engine, image, gender_face_input, gender_result)

    # output
    for i in range(0, gender_info.lFaceNumber):
        print(age_info.pAgeResultArray[i], '男' if gender_info.pGenderResultArray[i] == 0 else '女')

    ASAE_FSDK_UninitAgeEngine(fa_engine)
    ASGE_FSDK_UninitGenderEngine(fg_engine)
    AFD_FSDK_UninitialFaceEngine(fd_engine)
    end_time = time.time()
    print('所用时间{}'.format(end_time - start_time))


if __name__ == '__main__':
    main()
