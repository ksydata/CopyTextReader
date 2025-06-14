# ./copyTextReader/loadFile/loadPDF.py
from copyTextReader.abstractClass.abstractLoadFile import AbstractLoadFile
import os
from typing import *

from PIL import Image
from pdf2image import convert_from_path
# 이미지를 열고, 처리하고, 저장하는 라이브러리
# > python -m pip install Pillow
# > python -m pip install pdf2image
# C:\poppler\poppler-24.02.0\Library\bin

class LoadPDF(AbstractLoadFile):
    """pdf 파일을 로컬 경로에 따라 불러와 이미지로 변환하는 구체 클래스"""

    def __init__(self, filePath):
        """멤버변수 초기화
        
        Parameters
        ----------
        filePath(str): 지정된 파일 경로
        """
        self.filePath = filePath
    
    def listFiles(self) -> List[str]:
        """반복문 리스트 컴프리핸션을 통해 .pdf 확장자인 파일명만 반환"""
        return [file for file in os.listdir(self.filePath) if file.endswith(".pdf")]
        # 파일 확장자 필터링 시 file.endswith(extension) # (".pdf", ".tif", ".png", ".jpg", ".jpeg")
        # 향후 재귀적으로 하위 디렉토리 파일 나열 시 os.walk()
    
    def uploadData(self) -> List[Image.Image]:
        """
        Returns
        -------
        List[Image.Image]
        PDF의 각 페이지가 변환된 이미지 객체 리스트
        """
        imageList: List[Image.Image] = []
        # .pdf 확장자 파일명이 원소로 담을 리스트 선언

        for pdffileName in self.listFiles():
            # 클래스 멤버함수에 객체 생성 시 투입된 파일경로를 통해 받은 pdf파일을 이미지로 변환하는 for루프 수행
            pdfPath = os.path.join(self.filePath, pdffileName)

            try:                
                page = convert_from_path(
                    pdfPath, dpi = 600, 
                    poppler_path=r"C:\copyTextReader\poppler\poppler-24.02.0\Library\bin")
                # 해상도 dpi 기본값 600으로 설정 후 이미지 객체로 반환
                imageList.extend(page)
            except Exception as e:
                print(f"{pdffileName}파일 처리 중 알 수 없는 오류가 발생하였습니다.: {e}")

        return imageList
