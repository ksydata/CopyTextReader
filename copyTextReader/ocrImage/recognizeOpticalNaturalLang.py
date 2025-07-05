# ./copyTextReader/ocrImage/recognizeOpticalNaturalLang.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import numpy
import cv2
import os
from PIL import Image
from pororo import Pororo
# Platform Of neuRal mOdels for natuRal language prOcessing


class RecognizeOpticalNaturalLang(AbstractOCRImage):
    """카카오브레인의 통합된 형태의 자연어 프레임워크인 pororo을 활용한 문자 검출 및 인식 클래스
    
    내부적으로 NAVER Clova AI의 CRAFT 및 CRNN 기반의 OCR 모델
    -CRAFT:
        이미지에서 글자 영역을 탐지하는 모델
        (Character Region Awareness for Text Detection) 
    -CRNN:
        이미지의 공간적 정보를 유지해나가면서 추출한 특징을 바탕으로 RNN을 통해 
        시퀀스별 글자를 예측하는 딥러닝 모델
        (CNN과 RNN을 섞은 모델)
    """
    
    def __init__(self, processedImage: numpy.ndarray):
        """
        Parameters
        ----------
        processedImage: numpy.ndarray
            전처리된 이미지 (흑백/이진화 처리된 이미지)
        """
        self.processedImage = processedImage
        self.koreanOCR = Pororo(task="ocr", lang="ko")

    def preprocessImageObject(self) -> str:
        """
        이진 이미지로부터 한글 텍스트를 추출하여 반환하는 메서드

        Returns
        -------
        str : 이미지에서 감지된 텍스트 문자열
        """
        pillowImage = Image.fromarray(self.processedImage)
        # numpy 배열을 PIL 이미지로 변환
        ocrResult = self.koreanOCR(pillowImage)
        # Pororo OCR 실행
        
        if isinstance(ocrResult , list):
        # 각 글자영역 및 인식텍스트를 리스트 형식으로 반환되는 결과
            return "\n".join([item["text"] for item in ocrResult ])
            # 인식된 영역에서 텍스트만 추출하여 줄바꿈 연산자인 "\n"으로 연결
        return str(ocrResult)
        # ocrResult가 리스트가 아닐 경우 문자열로 처리

