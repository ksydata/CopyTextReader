# ./copyTextReader/factory/ocrImageFactory.py
from copyTextReader.abstractClass.abstractOCRImage import AbstractOCRImage
from copyTextReader.ocrImage.preprocessImage import PreprocessImage
from copyTextReader.ocrImage.binarizeImage import BinarizeImage
from copyTextReader.ocrImage.recognizeOpticalChars import RecognizeOpticalChars
from copyTextReader.ocrImage.recognizeOpticalKorean import RecognizeOpticalKorean

from PIL import Image, ImageFilter


class OCRImageFactory:
    """이미지 전처리 후 이진화 및 후처리 프로세스를 수행하는 팩토리 클래스"""

    def __init__(self, 
                 scanImage, 
                 ocrEngine: str, 
                 dependencyPath: str):
        self.scanImage = scanImage            
        # PIL.Image.Image 객체 형식의 스캔본(초본) 이미지
        self.processedImage = None
        # 전처리 결과 저장 필드 추가
        self.OCREngine = ocrEngine
        self.dependencyPath = dependencyPath
        
    def setPreprocessedImage(self) -> AbstractOCRImage:
        """전처리(preprocess), 이진화(binarize), 후처리(mophology)를 수행하고 이진 이미지를 반환하는 실행 메서드"""

        # 흐림 블러링, 흑백 변환
        preprocesser = PreprocessImage(self.scanImage)
        blurredImageArray = preprocesser.preprocessImageObject()

        # Otsu 이진화, 모폴로지 후처리
        binarizer = BinarizeImage(blurredImageArray)
        binarizedImage = binarizer.preprocessImageObject()

        self.processedImage = binarizedImage
        return self.processedImage
        # get에서 사용하도록 멤버변수에 저장 가능
        # return binarizedImage

    def getPreprocessedImage(self) -> AbstractOCRImage:
        """OCR 엔진을 선택하여 이진 이미지 객체에서 추출한 텍스트를 반환하는 실행 메서드"""
        if self.processedImage is None:
            raise ValueError("스캔본 이미지를 먼저 전처리한 후 OCR을 실행해주세요: setProcessedImage()")
        
        if self.OCREngine.lower() == "tesseract":
            OCR = RecognizeOpticalChars(self.processedImage)
        elif self.OCREngine.lower()  == "koreanOCR":
            OCR = RecognizeOpticalKorean(self.processedImage, self.dependencyPath)
        # elif self.OCREngine.lower() == "pororo":
            # OCR = RecognizeOpticalNaturalLang(self.getPreprocessedImage)
        else: 
            raise ValueError(f"{self.OCREngine}은 지원하지 않는 OCR 엔진입니다.")

        return OCR.preprocessImageObject()