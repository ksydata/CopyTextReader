# ./copyTextReader/ocrImage/recognizeOpticalChars.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import pytesseract
import cv2
import numpy

class RecognizeOpticalChars(AbstractOCRImage):
    def __init__(self, processedImage: numpy.ndarray):
        self.processedImage = processedImage
        self.config = "-l kor --oem 3 --psm 6"
        # config 내용변수에 한글 및 영어(kor+eng) 언어 설정 및 엔진 설정 후 저장
        # [oem1] OCR Engine Mode 1(LSTM 엔진 사용)
        # [oem3] OCR Engine Mode 3(LSTM & legacy hybrid 엔진 사용)
        # [psm3] Page Segmentation Mode 3(전체 페이지 텍스트 블록 인식)
        # [psm6] Page Segmentation Mode 6(테이블 형태와 같은 단일 유니폼 텍스트 블록 인식)
        # [psm11] Page Segmentation Mode 11(단일 텍스트 줄 인식)

    def preprocessImageObject(self) -> str:
        """이미지에서 문자 추출"""
        outputText = pytesseract.image_to_string(
            image = self.processedImage,
            config = self.config
        )
        return outputText