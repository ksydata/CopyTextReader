# ./copyTextReader/ocrImage/recognizeOpticalKorean.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import numpy as np
import cv2
import os
from PIL import Image

from ultralytics import YOLO
# import tensorflow
from keras.models import load_model
# from tensorflow.keras.models import load_model
# Import "tensorflow.keras.models" could not be resolvedPylancereportMissingImports


class RecognizeOpticalKorean(AbstractOCRImage):
    """
    YOLOv8과 ResNet을 사용한 한글 OCR 클래스.
    - YOLOv8로 자/모음 등의 문자 영역을 탐지
    - ResNet 모델로 해당 문자 이미지를 분류 (자음 등)
    """

    def __init__(self, processedImage: np.ndarray, dependencyPath: str):
        """
        생성자
        Parameters
        ----------
        processedImage : np.ndarray
            OCR을 수행할 전처리된 이미지 (numpy 배열, BGR 혹은 흑백 이미지)
        dependencyPath : str
            모델이 저장된 폴더 경로. YOLO(.pt)와 ResNet(.h5) 파일이 이 경로에 있어야 함.
        """
        self.processedImage = processedImage
        self.depPath = dependencyPath

        # YOLOv8 모델 경로 설정
        self.yoloModelPath = os.path.join(self.depPath, "YOLOv8x_best.pt")
        # ResNet 분류 모델 경로 설정
        self.resnetPath = os.path.join(self.depPath, "best_ResNet_consonants_model.h5")

        # 모델 불러오기
        self.yolo = YOLO(self.yoloModelPath)  # YOLOv8 객체 탐지 모델
        self.resnet = load_model(self.resnetPath)  # 자음 분류 ResNet 모델

        # 분류 결과 인덱스를 문자로 매핑하는 리스트
        # 예: ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', ..., 'ㅎ']
        # ResNet 학습 시 사용한 라벨 순서와 일치해야 함
        self.class_names = [...]  # TODO: 실제 라벨 순서로 채우기

    def preprocessImageObject(self) -> str:
        """
        이미지에서 한글 자음 문자열 추출 (YOLO → ResNet 추론)
        Returns
        -------
        str: 이미지에서 탐지된 자음 문자열
        """
        # YOLOv8을 사용하여 이미지에서 문자(자음 등) 영역을 탐지
        results = self.yolo(self.processedImage)

        boxes = []
        for r in results:
            # 탐지된 박스 좌표들을 numpy 배열로 수집 (xyxy 포맷: x1, y1, x2, y2)
            boxes.extend(r.boxes.xyxy.cpu().numpy().astype(int))

        # 탐지된 영역이 없을 경우 빈 문자열 반환
        if not boxes:
            return ""

        # 글자를 왼쪽 → 오른쪽 순으로 정렬
        boxes = sorted(boxes, key=lambda x: x[0])

        chars = []  # 최종 문자 결과 리스트

        # 각 탐지 박스를 순회하며 문자를 인식
        for (x1, y1, x2, y2) in boxes:
            # 해당 영역 잘라내기 (crop)
            crop = self.processedImage[y1:y2, x1:x2]

            # 컬러 이미지를 흑백으로 변환
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            # ResNet 입력 크기(64x64)로 리사이즈
            resized = cv2.resize(gray, (64, 64))

            # 픽셀 값을 0~1 사이로 정규화
            norm = resized / 255.0

            # 모델 입력 형태에 맞게 차원 확장: (1, 64, 64, 1)
            inp = np.expand_dims(norm, axis=(0, -1))

            # 분류 예측 수행
            pred = self.resnet.predict(inp)

            # 가장 높은 확률의 클래스 인덱스를 추출
            idx = np.argmax(pred, axis=1)[0]

            # 해당 인덱스에 대응되는 자음 문자로 변환
            chars.append(self.class_names[idx])

        # 탐지된 자음들을 문자열로 결합하여 반환
        # 추후: 초성/중성/종성을 조합하여 완성형으로 확장 가능
        return "".join(chars)
