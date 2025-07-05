# ./copyTextReader/test/test.py
import sys
sys.path.append("C:/CopyTextReader")
# 최상위 프로젝트 루트 경로를 추가해야 Python이 모듈 인식 가능
# print(sys.path)

from copyTextReader.factory.loadFileFactory import LoadFileFactory
from copyTextReader.factory.ocrImageFactory import OCRImageFactory
import os
import numpy
from typing import List

from PIL import Image
import cv2
import pytesseract
# @https://github.com/tesseract-ocr/tessdoc
# @https://github.com/UB-Mannheim/tesseract/wiki
# @https://github.com/tesseract-ocr/tessdata/blob/main/kor.traineddata

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\sooyeon Kang\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata" 
# 한글 언어 모델을 위한 훈련 데이터 경로 강제 지정

from ultralytics import YOLO
from tensorflow.python.keras.models import load_model
# python -m pip install --upgrade typing_extensions
# from tensorflow import keras
# from keras.models import load_model


def test():
    folderPath = input("테스트할 폴더 경로를 입력하세요: ").strip() 
    # C:/copyTextReader/data
    # saveFilePath = "C:/copyTextReader/data/test.png"
    if not os.path.isdir(folderPath):
        print(f"{folderPath}는 유효한 폴더 경로가 아닙니다.").strip() 
        return
    ocrEngine = input("OCR 모델 엔진을 선택하세요: ")
    dependencyPath = input("모델(의존성 패키지)) 경로를 입력하세요: ").strip()

    fileExtensions: List = [".pdf", ".tif", ".jpg", ".png"]
    
    for extension in fileExtensions:
        try:
            print(f"\n=== 확장자 {extension} 테스트 중 ===")
            loader = LoadFileFactory.loadImage(folderPath, extension)
            images = loader.uploadData()
            print(f"{extension} 확장자에서 {len(images)}개의 이미지 로딩 성공")
        
            # if images:
                # print("첫 번째 이미지 미리보기를 실행합니다.")
                # images[0].show()  
                # image.save("privewSample.jpg")
            # [생략] 샘플 이미지 OS의 뷰어로 열림
            
            for image in images:
            # for index, image in enumerate(images):
                # print(f"{index+1}번째 이미지 전처리 및 OCR 수행")
                ocrfactory = OCRImageFactory(image, ocrEngine, dependencyPath)
                processedImage = ocrfactory.setPreprocessedImage()
                # OCR 전처리 파이프라인 실행

                # resizer = ResizeImage(processedImage, scale = 2.0)
                # resizedImage = resizer.preprocessImageObject()
                # [생략] 이미지 사이즈 변경

                if processedImage is not None:
                    # 전처리 시 에러가 발생하거나 인식에 실패하여 Null이 아닌 경우
                   cv2.imshow("Processed", processedImage)
                   cv2.waitKey(0)
                   cv2.destroyAllWindows()
                   # 전처리 결과 이미지 확인
                   # cv2.imwrite(saveFilePath, processedImage)
                   # 전처리 결과 이미지 로컬에 저장
                   
                else:
                    raise ValueError("")
                
                ocrText = ocrfactory.getPreprocessedImage()
                print(f"OCR 추출 결과: \n{ocrText}")
                
                break
                # 테스트 목적이므로 첫 번째 이미지만 처리 후 break

        except Exception as e:
            print(f"{extension} 처리 중 오류: {e}")

    print("=== \n테스트 완료=== ")

if __name__ == "__main__":
    test()

"""
C:\CopyTextReader>"C:/Users/sooyeon Kang/AppData/Local/Programs/Python/Python310/python.exe" 
C:/CopyTextReader/test/test.py

테스트할 폴더 경로를 입력하세요: C:/copyTextReader/data
OCR 모델 엔진을 선택하세요: koreanOCR | tesseract
모델(의존성 패키지)) 경로를 입력하세요: C:/copyTextReader/dependency

=== 확장자 .jpg 테스트 중 ===
.jpg 확장자에서 3개의 이미지 로딩 성공
.jpg 처리 중 오류: OpenCV(4.11.0) :-1: error: (-5:Bad argument) in function 'cvtColor'
> Overload resolution failed:
>  - src data type = object is not supported
>  - Expected Ptr<cv::UMat> for argument 'src'

=== 확장자 .jpg 테스트 중 ===
.jpg 확장자에서 3개의 이미지 로딩 성공
.jpg 처리 중 오류: OCRImageFactory.getPreprocessedImage() takes 1 positional argument but 2 were given

=== 확장자 .jpg 테스트 중 ===
.jpg 확장자에서 3개의 이미지 로딩 성공
.jpg 처리 중 오류: koreanOCR은 지원하지 않는 OCR 엔진입니다.
"""