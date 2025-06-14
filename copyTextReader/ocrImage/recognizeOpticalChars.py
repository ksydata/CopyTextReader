# ./copyTextReader/ocrImage/recognizeOpticalChars.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import pytesseract
import cv2
import numpy

class RecognizeOpticalChars(AbstractOCRImage):
    def __init__(self, processedImage: numpy.ndarray):
        self.processedImage = processedImage
        self.config = "-l kor+eng --oem 3 --psm 11"
        # config 내용변수에 '한글 및 영어 언어 설정, OCR Engine Mode 3 및 Page Segmentation Mode 11' 저장

    def preprocessImageObject(self) -> str:
        """이미지에서 문자 추출"""
        outputText = pytesseract.image_to_string(
            image = self.processedImage,
            config = self.config
        )
        return outputText