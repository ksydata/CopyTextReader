# ./copyTextReader/ocrImage/preprocessImage.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
from PIL import Image, ImageFilter
import numpy
import cv2

class PreprocessImage(AbstractOCRImage):
    def __init__(self, scanImage: Image.Image):
        self.scanImage = scanImage

    def preprocessImageObject(self):
        """이진화 전처리를 수행하는 메서드 """

        imageArray = numpy.array(self.scanImage)
        # Pillow.Image.Image 객체를 OpenCV가 이해할 수 있도록 넘파이 배열로 변환
        # readImage = cv2.imread(imageArray)
        
        grayImage = cv2.cvtColor(imageArray, cv2.COLOR_BGR2GRAY)
        # 글자 추출 전처리를 위해 흑백 처리
        # grayImage = self.scanImage.convert("L") 
        # .lambda(x for x: 0 if x <= 128 else 1)

        blurredImage = cv2.GaussianBlur(
            src = grayImage, # 이미지 객체 행렬 
            ksize = (5, 5), # 너비방향, 높이방향 평균 필터 크기(홀수 지정)
            sigmaX = 0, # 가우시안 커널의 표준편차를 필터 가장자리 부근 가중치로 설정(0으로 설정 시 자동 계산)
            sigmaY= 0
        )
        # 노이즈 제거(글자 경계 선명도)를 위한 가우시안 블러링 처리
        # 필터 내 모든 픽셀에 가중치 동일하게 부여하여 단순 평균하는 방식
        # [ksize] 노이즈 적으면 (3, 3) 많거나 흐릿하면 (5, 5), (7, 7)
        # [대체 블러] medianBlur, bilateralFilter

        return blurredImage
    