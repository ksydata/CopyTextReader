# ./copyTextReader/abstractClass/abstractLoadFile.py
from abc import ABC, abstractmethod # ABCMeta

class AbstractLoadFile:
    """pdf, tif, jpg, png 형태의 파일을 불러오는 추상 부모 클래스"""

    @abstractmethod
    def listFiles(self, filepath):
        """파일 경로 내 디렉토리의 모든 파일명 불러오기 위한 추상 메서드"""
        pass

    @abstractmethod    
    def uploadData(self, filepath):
        """다양한 확장자의 파일을 적용하기 위한 추상 메서드"""
        pass