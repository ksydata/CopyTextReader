# ./copyTextReader/ocrImage/recognizeOpticalNaturalLang.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import numpy
import cv2
import os

import tempfile
import uuid
from PIL import Image

from pororo import Pororo
# Platform Of neuRal mOdels for natuRal language prOcessing
from torchvision.models import resnet50, ResNet50_Weights

from skimage import io, color, filters, transform
from skimage.filters import threshold_otsu
# python -m pip install tensorboardX, scikit-image


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
        # koreanOCR = Pororo(task = "ocr", lang = "ko")
        # Pororo 초기화하는 클래스 변수

        """
        Parameters
        ----------
        processedImage: numpy.ndarray
            전처리된 이미지 (흑백/이진화 처리된 이미지)
        """
        if not isinstance(processedImage, numpy.ndarray):
            raise TypeError("processedImage는 numpy.ndarray 타입이어야 합니다.")
        self.processedImage = processedImage
        self.koreanOCR = Pororo(task = "ocr", lang = "ko")
        # 클래스 변수 초기화
        # if RecognizeOpticalNaturalLang.koreanOCR is None:
            # RecognizeOpticalNaturalLang.koreanOCR = Pororo(task = "ocr", lang = "ko")

    def preprocessImageObject(self) -> str:
        """
        이진 이미지로부터 한글 텍스트를 추출하여 반환하는 메서드

        Returns
        -------
        str : 이미지에서 감지된 텍스트 문자열
        """
        imagePath = self.saveToTempFile(self.processedImage)
        # 전처리된 이미지를 임시 파일로 저장한 뒤, Pororo에 경로로 전달

        ocrResult = self.koreanOCR(imagePath, detail = True)
        # ocrResult = RecognizeOpticalNaturalLang.koreanOCR(pillowImage)
        # self로 접근하여 클래스 변수인 Pororo OCR 실행
        # 좌표값을 함께 반환
        
        if isinstance(ocrResult , list):
        # 각 글자영역 및 인식텍스트를 리스트 형식으로 반환되는 결과
            try:
                return "\n".join([
                    item["text"]
                    for item in ocrResult
                    if isinstance(item, dict) and "text" in item
                ])
            # 인식된 영역에서 텍스트만 추출하여 줄바꿈 연산자인 "\n"으로 연결
            except Exception as e:
                print(f"[OCR 리스트 처리 오류] {e}")
                return str(ocrResult)
            # ocrResult가 리스트가 아닐 경우 문자열로 처리
        else:
            return str(ocrResult)

    @staticmethod
    def saveToTempFile(imageArray: numpy.ndarray) -> str:
        """
        전처리된 Numpy 이미지 배열을 임시 JPG 파일로 저장하고 파일경로를 반환

        Returns
        -------
        str : 임시 저장된 이미지 파일경로
        """
        pillowImage = Image.fromarray(imageArray)
        # numpy 배열을 PIL 이미지로 변환
        # [.jpg 처리 중 img 변수가 할당 전에 참조되었다는 오류] local variable 'img' referenced before assignment
        # [cmd > cd C:/copyTextReader/] findstr /S /N "img" *.py
        
        tempFileName = f"ocr_temp_{uuid.uuid4().hex}.jpg"
        tempFilePath = os.path.join(tempfile.gettempdir(), tempFileName)
        pillowImage.save(tempFilePath)
        # 이미지를 임시저장할 파일경로 설정 후 저장
        
        return tempFilePath
