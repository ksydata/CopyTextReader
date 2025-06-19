# ./copyTextReader/ocrImage/hangeulOCR.py

import numpy
import cv2
import os
from PIL import Image

from ultralytics import YOLO
# import tensorflow
# from keras.models import load_model
from tensorflow.python.keras.models import load_model
# Import "tensorflow.keras.models" could not be resolvedPylancereportMissingImports


class HangeulOCR:
    """이미지에서 문자 영역을 탐지해서 bounding box 리스트 반환하는 한글OCR 클래스"""

    def __init__(self, yoloModelPath: str, resnetModelPath: str):
        """생성자

        Parameters
        ----------
        processedImage : numpy.ndarray
            OCR을 수행할 전처리된 이미지 (numpy 배열, BGR 혹은 흑백 이미지)
        dependencyPath : str
            모델 가중치가 저장된 폴더 경로. YOLO(.pt)와 ResNet(.h5) 파일이 이 경로에 있어야 함.
        """
        self.yolo = YOLO(self.yoloModelPath)  
        # YOLOv8 객체 탐지 모델 (자/모음 등의 문자 영역을 탐지)
        self.resnet = load_model(self.resnetModelPath)  
        # 자음 분류 ResNet 모델 (자음 등 해당 문자 이미지를 분류)

        # 분류 결과 인덱스를 문자로 매핑하는 리스트
        self.classNames = [
            'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
            'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ]
        # ResNet 학습 시 사용한 라벨 순서와 일치해야 함

    def run(self, processedImage: Image.Image) ->  str:
        """이미지에서 한글 자음 문자열 추출 (YOLO → ResNet 추론)
        
        Returns
        -------
        str: 이미지에서 탐지된 자음 문자열
        """
        results = self.yolo(self.processedImage)
        # YOLOv8을 사용하여 이미지에서 문자(자음 등) 영역을 탐지

        boxes = []
        for r in results:
            boxes.extend(
                r.boxes.xyxy.cpu().numpy().astype(int))
            # 탐지된 박스 좌표들을 numpy 배열로 수집 (xyxy 포맷: x1, y1, x2, y2)

        if not boxes:
            return ""
        # 탐지된 영역이 없을 경우 빈 문자열 반환

        boxes = sorted(boxes, key=lambda x: x[0])
        # 글자를 왼쪽에서 오른쪽 순으로 정렬

        chars = []  
        # 최종 문자 결과 리스트

        for (x1, y1, x2, y2) in boxes:
        # 각 탐지 박스를 순회하며 문자를 인식
            crop = self.processedImage[y1:y2, x1:x2]
            # 해당 영역 잘라내기 (crop)

            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            # 컬러 이미지를 흑백으로 변환

            resized = cv2.resize(gray, (64, 64))
            # ResNet 입력 크기(64x64)로 리사이즈

            norm = resized / 255.0
            # 픽셀 값을 0~1 사이로 정규화

            dimension = numpy.expand_dims(norm, axis=(0, -1))
            # 모델 입력 형태에 맞게 차원 확장: (1, 64, 64, 1)

            pred = self.resnet.predict(dimension)
            # 분류 예측 수행

            idx = numpy.argmax(pred, axis=1)[0]
            # 가장 높은 확률의 클래스 인덱스를 추출

            chars.append(self.classNames[idx])
            # 해당 인덱스에 대응되는 자음 문자로 변환

        return "".join(chars)
        # 탐지된 자음들을 문자열로 결합하여 반환
        # [Develop] 초성/중성/종성을 조합하여 완성형으로 확장 가능