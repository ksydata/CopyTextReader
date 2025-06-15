# ./copyTextReader/ocrImage/recognizeOpticalKorean.py

from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
import cv2
import numpy

# git clone https://github.com/rkdgg0/DevelopmentOfHangeulOCR.git
# cd DevelopmentOfHangeulOCR
# pip install -r requirements.txt

# git lfs install
# git lfs pull

class RecognizeOpticalKorean(AbstractOCRImage):
    def __init__(self, processedImage: numpy.ndarray):
        self.processedImage = processedImage

    def preprocessImageObject(self) -> str:
        """이미지에서 문자 추출"""
        outputText = ""
        return outputText
    
    