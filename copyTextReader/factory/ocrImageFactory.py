# ./copyTextReader/factory/ocrImageFactory.py
from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
from copyTextReader.ocrImage.preprocessImage import PreprocessImage
from copyTextReader.ocrImage.binarizeImage import BinarizeImage
from copyTextReader.ocrImage.recognizeOpticalChars import RecognizeOpticalChars

from PIL import Image, ImageFilter


class OCRImageFactory:
    """이미지 전처리 후 이진화 및 후처리 프로세스를 수행하는 팩토리 클래스"""

    def __init__(self, scanImage: Image.Image):
        self.scanImage = scanImage  
        # PIL.Image.Image 객체 형식의 스캔본(초본) 이미지

    def setPreprocessedImage(self) -> AbstractOCRImage:
        """전처리(preprocess), 이진화(binarize), 후처리(mophology)를 수행하고 최종 이진 이미지를 반환하는 구체 메서드"""

        # 흐림 블러링, 흑백 변환
        preprocesser = PreprocessImage(self.scanImage)
        blurredImageArray = preprocesser.preprocessImageObject()

        # Otsu 이진화, 모폴로지 후처리
        binarizer = BinarizeImage(blurredImageArray)
        binarizedImage = binarizer.preprocessImageObject()

        charsExtracter = RecognizeOpticalChars(binarizedImage)
        ocrText = charsExtracter.preprocessImageObject()

        return binarizedImage, ocrText