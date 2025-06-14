# ./copyTextReader/ocrImage/binarizeImage.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import numpy
from PIL import Image, ImageFilter
import cv2

class BinarizeImage(AbstractOCRImage):
    def __init__(self, imageArray: numpy.ndarray):
        self.imageArray = imageArray

    def preprocessImageObject(self):
        """이진화 전처리 및 모폴로지 후처리(글자 형상 보정, 잡티 제거)를 수행하는 메서드"""

        _, binaryImage = cv2.threshold(
            src = self.imageArray, 
            thresh = 0, 
            maxval = 255, 
            type = cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # [binary type] 임계값 구간 설정 적용 및 자동(추천) 임계값 결정

        structruedkernel = cv2.getStructuringElement(
            shape = cv2.MORPH_RECT, 
            ksize = (3, 3))
        # [cv2.MORPH_RECT] 구조 요소 정의 (3x3 사각형)

        morphedImage = cv2.morphologyEx(
            src = binaryImage, 
            op = cv2.MORPH_CLOSE, 
            kernel = structruedkernel,
            iterations = 1)
        # [morphedImage] 작은 구멍을 채우고 떨어진 문자 연결을 강화하는 연산

        return morphedImage
        # pilImage = Image.fromarray(morphedImage)