# ./copyTextReader/factory/loadFileFactory.py
from copyTextReader.abstractClass.abstractLoadFile import AbstractLoadFile
from copyTextReader.loadFile.loadPDF import LoadPDF
from copyTextReader.loadFile.loadTIF import LoadTIF
from copyTextReader.loadFile.loadJPG import LoadJPG
from copyTextReader.loadFile.loadPNG import LoadPNG

class LoadFileFactory:
    """확장자에 따라 적절한 로더 기능(구체) 클래스 반환하는 팩토리 클래스"""

    @staticmethod
    def loadImage(filePath: str, fileExtension: str) -> AbstractLoadFile:
        """OOP(Open/Closed 원칙) 
        확장자가 추가될 경우 로더 기능 클래스만 새로 추가하면 기존 클래스 수정 없이 팩토리 패턴을 통해 실행 가능"""
        extension = fileExtension.lower()
        
        if extension == ".pdf": return LoadPDF(filePath)
        elif extension == ".tif": return LoadTIF(filePath)
            # in [".tif", ".tiff"]
        elif extension == ".jpg": return LoadJPG(filePath)
        elif extension == ".png": return LoadPNG(filePath)  
        else: raise ValueError(f"{extension}은 지원하지 않는 파일 확장자입니다.")