# ./copyTextReader/ocrImage/recognizeOpticalKorean.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import numpy
import cv2
import os
from PIL import Image
from ultralytics import YOLO
# python -m pip install ultralytics
# YOLO (You Only Look Once) object detection model
# (프로젝트: https://github.com/rkdgg0/DevelopmentOfHangeulOCR)


class RecognizeOpticalKorean(AbstractOCRImage):
    """YOLOv8 & Keras ResNet 기반 한글 OCR 모델(YOLO 기반)을 활용한 문자 검출 및 인식 클래스"""
    def __init__(self, processedImage: numpy.ndarray, clonePath: str):
        """
        Parameters
        ----------
        processedImage: numpy.ndarray
            전처리된 이미지 (흑백/이진화 처리된 이미지)
        clonePath: str
            git clone 받은 DevelopmentOfHangeulOCR 경로
        """
        self.processedImage = processedImage
        self.koreanOCRPath = clonePath
        self.YOLOModelPath = os.path.join(
            self.koreanOCRPath, "YOLOv8x_best.pt")
        # 모델 가중치 경로
        # C:/Users/sooyeon Kang/DevelopmentOfHangeulOCR | C:/copyTextReader/dependency

        self.koreanOCR = None  
        # 한글 OCR 객체
        self._loadKoreanOCR()

    def _loadKoreanOCR(self):
        """DevelopmentOfHangeulOCR 내 HangeulOCR 클래스 import 및 객체 생성하는 메서드"""
        import sys
        if self.koreanOCRPath not in sys.path:
            sys.path.append(self.koreanOCRPath)

        # inference.py 내 HangeulOCR.class 정의
        from inference import HangeulOCR
        self.koreanOCR = HangeulOCR(model_path=self.YOLOModelPath)
        # YOLOv8(YOLOv8x_best.pt)으로 문자 영역 탐지
        # ResNet(best_ResNet_consonants_model.h5)으로 자음 인식
        # 다시 조합해 한글을 완성

    def preprocessImageObject(self) -> str:
        """
        YOLOv8로 글자 영역 탐지 후, ResNet으로 문자를 인식하여 이미지로부터 한글 텍스트를 추출하는 메서드
        """
        pillowImage = Image.fromarray(self.processedImage)
        ocrText = self.koreanOCR.run(pillowImage)

        return ocrText