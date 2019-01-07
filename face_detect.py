import time

from lib import FaceInfo
from lib import fd_clibrary
from lib.face_detect_sdk_library import *
from util import image_loader
from conf.config import *

APP_ID = c_char_p(bytes(config.get('arcsoft', 'APP_ID'), encoding='utf-8'))
FD_SDK_KEY = c_char_p(bytes(config.get('arcsoft', 'FD_SDK_KEY'), encoding='utf-8'))

FD_WORKBUF_SIZE = 20 * 1024 * 1024
MAX_FACE_NUM = 50
bUseYUVFile = False
bUseBGRToEngine = True


def do_face_detection(fd_engine, image):
    face_info = []

    face_res = POINTER(AFD_FSDK_FACERES)()
    ret = AFD_FSDK_StillImageFaceDetection(fd_engine, byref(image), byref(face_res))

    if ret != 0:
        print(u'AFD_FSDK_StillImageFaceDetection 0x{0:x}'.format(ret))
        return face_info

    faces = face_res.contents

    # faces 是一个对象所以 输出会是一个地址值 而他的一个属性nface是表示的是人脸的个数
    face_num = faces.nFace
    print('{} 个人脸'.format(face_num))

    if face_num > 0:
        for i in range(0, face_num):
            rect = faces.rcFace[i]
            orient = faces.lfaceOrient[i]
            face_info.append(FaceInfo(rect.left, rect.top, rect.right, rect.bottom, orient))
    return face_info


def main():
    start_time = time.time()

    fd_work_memery = fd_clibrary.malloc(c_size_t(FD_WORKBUF_SIZE))
    fd_engine = c_void_p()
    ret = AFD_FSDK_InitialFaceEngine(APP_ID, FD_SDK_KEY, fd_work_memery, c_int32(FD_WORKBUF_SIZE), byref(fd_engine),
                                     AFD_FSDK_OPF_0_HIGHER_EXT, 32, MAX_FACE_NUM)

    if ret != 0:
        fd_clibrary.free(fd_work_memery)
        print(u'AFD_FSDK_InitialFaceEngine ret 0x{:x}'.format(ret))
        exit(0)

    file_path = '001.jpg'
    image = image_loader.load_image(bUseBGRToEngine, file_path)

    face_info = do_face_detection(fd_engine, image)
    for i in range(0, len(face_info)):
        rect = face_info[i]
        print(u'{} ({} {} {} {}) orient {}'.format(i, rect.left, rect.top, rect.right, rect.bottom, rect.orient))

    AFD_FSDK_UninitialFaceEngine(fd_engine)
    end_time = time.time()
    print('所用时间{}'.format(end_time - start_time))
    fd_clibrary.free(fd_work_memery)


if __name__ == '__main__':
    main()
