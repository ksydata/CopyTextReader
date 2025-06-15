# ./copyTextReader/ocrImage/resizeImage.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import numpy
from PIL import Image, ImageFilter
import cv2

class ResizeImage(AbstractOCRImage):
    def __init__(self, imageArray: numpy.ndarray, scale: float):
        self.imageArray = imageArray
        self.scale = scale
        # 확대 비율

    def preprocessImageObject(self) -> numpy.array:
        """이미지를 지정된 배율로 확대하는 메서드
        
        Parameters
        ----------
        imageArray: 전처리된 넘파이 배열 형태의 이미지 객체
        scale: 확대/축소 비율

        AS-IS
        -----
        cv2.imshow()
        cv2.imwrite()
        """
        currentHeight, currentWidth = self.imageArray.shape[:2]
        # 이미지 높이 및 너비를 변수에 저장
        newHeight = int(currentHeight * self.scale)
        newWidth = int(currentWidth * self.scale)
        # 입력받은 배율로 새로운 이미지 높이 및 너비(크기) 설정

        resizedImage = cv2.resize(
            src = self.imageArray,
            dsize = (newHeight, newWidth),
            interpolation = cv2.INTER_LINEAR
        )

        return resizedImage