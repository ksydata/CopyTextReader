# ./copyTextReader/ocrImage/recognizeOpticalKorean.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
from copyTextReader.ocrImage.hangeulOCR import HangeulOCR

import numpy
import cv2
import os
from PIL import Image
from ultralytics import YOLO
# python -m pip install ultralytics
# YOLO (You Only Look Once) object detection model
# (프로젝트: https://github.com/rkdgg0/DevelopmentOfHangeulOCR)


class RecognizeOpticalKorean(AbstractOCRImage):
    """YOLOv8 & Keras ResNet 기반 한글 OCR 모델(YOLO 기반)을 활용한 문자 검출 및 인식 클래스
    
    YOLO(Bounding Box): 글자(자모, 단어 등) 위치 탐지 
    ResNet(ㄱ, ㄴ, ㄷ 등): 탐지된 글자 영역 분류 
    """
    
    def __init__(self, processedImage: numpy.ndarray, dependencyPath: str):
        """
        Parameters
        ----------
        processedImage: numpy.ndarray
            전처리된 이미지 (흑백/이진화 처리된 이미지)
        dependencyPath : str
            git clone 받은 DevelopmentOfHangeulOCR 경로
        """
        self.processedImage = processedImage
        self.dependencyPath = dependencyPath
        self.YOLOModelPath = os.path.join(self.dependencyPath, "YOLOv8x_best.pt")
        self.ResNetModelPath = os.path.join(self.dependencyPath, "best_ResNet_consonants_model.h5")
        # 모델 가중치 경로
        # C:/Users/sooyeon Kang/DevelopmentOfHangeulOCR | C:/copyTextReader/dependency

        self.koreanOCR = None  
        # 한글 OCR 객체 초기화
        self._loadKoreanOCR()

    def _loadKoreanOCR(self):
        """
        기존에 DevelopmentOfHangeulOCR 프로젝트에서 HangeulOCR 클래스를 import 했으나,
        외부 프로젝트가 없으므로, 내부에 구현한 HangeulOCR 클래스를 직접 사용합니다.
        """
        self.koreanOCR = self.HangeulOCR(
            self.YOLOModelPath, self.ResNetModelPath)
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