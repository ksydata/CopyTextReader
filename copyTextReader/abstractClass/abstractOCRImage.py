# ./copyTextReader/abstractClass/abstractOCRImage.py

from abc import ABC, abstractmethod
from typing import List

class AbstractOCRImage:
    """주민등록초본 이미지 객체에서 글자를 추출하는 추상 클래스
    
    Problems
    --------
    밝은 배경으로 대비율 낮아짐
    흐린 이미지(해상도의 한계)로 글자 경계에 대한 구분이 떨어짐
    글자와 혼동하도록 하는 워터마크

    Solutions
    ---------
    이미지로부터 텍스트 영역에 대한 모델의 인식률을 높이기 위한 보정/노이즈 제거 기술
    글자 검출 모델을 이용하여 텍스트 영역을 찾는 기술
    어떤 문자를 의미하는지 찾는 기술
    """
    
    @abstractmethod
    def preprocessImageObject(self): 
        """흑백 처리, 배경 블러, 노이즈 제거, 적응형 이진화 등 전처리를 수행하고 이진수를 텍스트로 인식하기 위한 추상 메서드"""
        pass

    

