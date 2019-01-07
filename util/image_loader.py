# -*- encoding=utf-8 -*-
import io
from PIL import Image
from . import BufferInfo
from lib import ASVLOFFSCREEN, c_ubyte_p
from lib import asvl_color_format
from ctypes import *

USING_FLOAT = True


def bgra_2_i420(bgr_buffer, width, height):
    yuv = bytearray(width * height * 3 // 2)
    u_offset = width * height
    y_offset = width * height * 5 // 4

    for i in range(0, height):
        for j in range(0, width):
            b = ord(bgr_buffer[54 + (i * width + j) * 3 + 0])
            g = ord(bgr_buffer[54 + (i * width + j) * 3 + 1])
            r = ord(bgr_buffer[54 + (i * width + j) * 3 + 2])

            y = ((77 * r + 150 * g + 29 * b + 128) >> 8)
            u = (((-43) * r - 84 * g + 127 * b + 128) >> 8) + 128
            v = ((127 * r - 106 * g - 21 * b + 128) >> 8) + 128

            y = 0 if y < 0 else (255 if y > 255 else (y & 0xFF))
            u = 0 if u < 0 else (255 if u > 255 else (u & 0xFF))
            v = 0 if v < 0 else (255 if v > 255 else (v & 0xFF))

            yuv[i * width + j] = y
            yuv[u_offset + (i >> 1) * (width >> 1) + (j >> 1)] = u
            yuv[y_offset + (i >> 1) * (width >> 1) + (j >> 1)] = v

    return bytes(yuv)


def bgra_2_i420_float(bgr_buffer, width, height):
    yuv = bytearray(width * height * 3 // 2)
    u_offset = width * height
    y_offset = width * height * 5 // 4

    for i in range(0, height):
        for j in range(0, width):
            b = ord(bgr_buffer[54 + (i * width + j) * 3 + 0])
            g = ord(bgr_buffer[54 + (i * width + j) * 3 + 1])
            r = ord(bgr_buffer[54 + (i * width + j) * 3 + 2])

            y = (0.299 * r + 0.587 * g + 0.114 * b)
            u = (-0.169) * r - 0.331 * g + 0.499 * b + 128.0
            v = 0.499 * r - 0.418 * g - 0.0813 * b + 128.0

            yuv[i * width + j] = int(y)
            yuv[u_offset + (i >> 1) * (width >> 1) + (j >> 1)] = int(u)
            yuv[y_offset + (i >> 1) * (width >> 1) + (j >> 1)] = int(v)

    return bytes(yuv)


def get_i420_from_file(file_path):
    old_img = Image.open(file_path)

    # BMP 4 byte align
    new_width = old_img.width & 0xFFFFFFFC
    new_height = old_img.height & 0xFFFFFFFE
    if (new_width != old_img.width) or (new_height != old_img.height):
        crop_area = (0, 0, new_width, new_height)
        img = old_img.crop(crop_area)
    else:
        img = old_img
    bmp_bytes = io.BytesIO()
    img.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').save(bmp_bytes, format='BMP')
    bgr_buffer = bmp_bytes.getvalue()

    if USING_FLOAT:
        yuv = bgra_2_i420_float(bgr_buffer, new_width, new_height)
    else:
        yuv = bgra_2_i420(bgr_buffer, new_width, new_height)
    return BufferInfo(new_width, new_height, yuv)


def get_bgra_from_file(file_Path):
    old_img = Image.open(file_Path)

    # BMP 4 byte align
    new_width = old_img.width & 0xFFFFFFFC
    new_height = old_img.height & 0xFFFFFFFE
    if (new_width != old_img.width) or (new_height != old_img.height):
        crop_area = (0, 0, new_width, new_height)
        img = old_img.crop(crop_area)
    else:
        img = old_img

    bmp_bytes = io.BytesIO()
    img.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').save(bmp_bytes, format='BMP')
    bgr_buffer = bytes(bmp_bytes.getvalue()[54:])

    return BufferInfo(new_width, new_height, bgr_buffer)


def load_image(bUseBGRToEngine, file_path):
    inputImg = ASVLOFFSCREEN()

    if bUseBGRToEngine:  # true
        bufferInfo = get_bgra_from_file(file_path)
        inputImg.u32PixelArrayFormat = asvl_color_format.ASVL_PAF_RGB24_B8G8R8
        inputImg.i32Width = bufferInfo.width
        inputImg.i32Height = bufferInfo.height
        inputImg.pi32Pitch[0] = bufferInfo.width * 3
        inputImg.ppu8Plane[0] = cast(bufferInfo.buffer, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    else:
        bufferInfo = get_i420_from_file(file_path)
        inputImg.u32PixelArrayFormat = asvl_color_format.ASVL_PAF_I420
        inputImg.i32Width = bufferInfo.width
        inputImg.i32Height = bufferInfo.height
        inputImg.pi32Pitch[0] = inputImg.i32Width
        inputImg.pi32Pitch[1] = inputImg.i32Width // 2
        inputImg.pi32Pitch[2] = inputImg.i32Width // 2
        inputImg.ppu8Plane[0] = cast(bufferInfo.buffer, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(
            addressof(inputImg.ppu8Plane[0].contents) + (inputImg.pi32Pitch[0] * inputImg.i32Height), c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(
            addressof(inputImg.ppu8Plane[1].contents) + (inputImg.pi32Pitch[1] * inputImg.i32Height // 2), c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    inputImg.gc_ppu8Plane0 = bufferInfo.buffer

    return inputImg
