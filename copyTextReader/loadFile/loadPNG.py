# ./copyTextReader/loadFile/loadPNG.py
from copyTextReader.abstractClass.abstractLoadFile import AbstractLoadFile
import os
from typing import *

from PIL import Image
# 이미지를 열고, 처리하고, 저장하는 라이브러리

class LoadPNG(AbstractLoadFile):
    """png 파일(이미지)을 로컬 경로에 따라 불러오는 구체 클래스"""

    def __init__(self, filePath):
        """멤버변수 초기화
        
        Parameters
        ----------
        filePath(str): 지정된 파일 경로
        """
        self.filePath = filePath
    
    def listFiles(self) -> List[str]:
        """반복문 리스트 컴프리핸션을 통해 .png 확장자인 파일명만 반환"""
        return [file for file in os.listdir(self.filePath) if file.endswith(".png")]

    def uploadData(self) -> List[Image.Image]:
        """
        Returns
        -------
        List[Image.Image]
        PNG 이미지 객체 리스트
        """

        imageList: List[Image.Image] = []
        # .png 확장자 파일명이 원소로 담을 리스트 선언

        for pngfileName in self.listFiles():
            # 클래스 멤버함수에 객체 생성 시 투입된 파일경로를 통해 받은 pdf파일을 이미지로 변환하는 for루프 수행

            try:
                pngPath = os.path.join(self.filePath, pngfileName)
                image = Image.open(pngPath)
                imageList.append(image)
                # 단일 Image.Image 객체이며 iterable 처리 시 에러 발생
            except Exception as e:
                print(f"{pngfileName}파일 처리 중 알 수 없는 오류가 발생하였습니다.: {e}")

        return imageList