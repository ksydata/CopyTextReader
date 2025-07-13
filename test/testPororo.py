# ./copyTextReader/test/testPororo.py

import numpy
import cv2
import os

import tempfile
import uuid
from PIL import Image

from pororo import Pororo
# Platform Of neuRal mOdels for natuRal language prOcessing
from torchvision.models import resnet50, ResNet50_Weights

from skimage import io, color, filters, transform
from skimage.filters import threshold_otsu


def isinArea(vertices, area):
    """
    주어진 좌표 리스트(vertices)가 지정된 영역(area)에 포함되는지 확인

    Parameters
    ----------
    vertices : list of dict
        텍스트 박스의 꼭짓점 좌표 리스트 [{'x': int, 'y': int}, ...]
    area : tuple
        (x_min, y_min, x_max, y_max) 형태의 영역 좌표

    Returns
    -------
    bool
        하나라도 영역 내에 포함되면 True, 아니면 False
    """
    x_min, y_min, x_max, y_max = area
    for point in vertices:
        x = point.get('x', 0)
        y = point.get('y', 0)
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
    return False


def extractTextByArea(ocr_result, area):
    """
    OCR 결과 리스트에서 지정된 영역에 포함된 텍스트만 추출

    Parameters
    ----------
    ocr_result : list of dict
        Pororo OCR에서 detail=True일 때 반환되는 전체 텍스트 영역 리스트
    area : tuple
        추출할 영역 (x_min, y_min, x_max, y_max)

    Returns
    -------
    str
        영역 내 텍스트를 공백으로 연결한 문자열
    """
    texts = []
    for item in ocr_result:
        if not isinstance(item, dict):
            continue
        # 'bounding_poly' 또는 'vertices' 중 존재하는 키 사용
        vertices = item.get("bounding_poly", item.get("vertices", []))
        if vertices and isinArea(vertices, area):
            texts.append(item.get("text", ""))
    return " ".join(texts)


class testPororo:
    def __init__(self):
        self.koreanOCR = Pororo(task="ocr", lang="ko")
    
    def preprocessImageObject(self) -> str:
        """
        이진 이미지로부터 한글 텍스트를 추출하여 반환하는 메서드

        Returns
        -------
        str : 이미지에서 감지된 특정 영역별 텍스트 문자열
        """
        name = input("대상자 이름을 입력하세요: ")
        
        imagePath = f"C:/copyTextReader/data/test/{name}_초본_grayScale_PNG.png"
        # imagePath = self.saveToTempFile(self.processedImage)
        # 전처리된 이미지를 임시 파일로 저장한 뒤, Pororo에 경로로 전달

        ocrResult = self.koreanOCR(imagePath, detail=True)
        # ocrResult = self.koreanOCR(imagePath)
        # if isinstance(ocrResult , list):
        # 각 글자영역 및 인식텍스트를 리스트 형식으로 반환되는 결과
            # try:
                # return "\n".join([
                    # item["text"]
                    # for item in ocrResult
                    # if isinstance(item, dict) and "text" in item])
            # 인식된 영역에서 텍스트만 추출하여 줄바꿈 연산자인 "\n"으로 연결
            # except Exception as e:
                # print(f"[OCR 리스트 처리 오류] {e}")
                # return str(ocrResult)
            # ocrResult가 리스트가 아닐 경우 문자열로 처리
        # else: return str(ocrResult)
    
        # 아래 영역 좌표는 이미지마다 조정 필요, (x_min, y_min, x_max, y_max) 순서
        issuedDate_area = (1700, 700, 3600, 900)
        name_area = (300, 1150, 900, 1300)
        residentNum_area = (2900, 1150, 4300, 1300)
        address_area = (100, 2600, 2000, 2900)
        certificateType_area = (2000, 100, 4000, 700)

        # 각 영역별 텍스트 추출
        issuedDate = extractTextByArea(ocrResult, issuedDate_area)
        personName = extractTextByArea(ocrResult, name_area)
        residentNum = extractTextByArea(ocrResult, residentNum_area)
        address = extractTextByArea(ocrResult, address_area)
        certificateType = extractTextByArea(ocrResult, certificateType_area)

        # 디버깅용: 영역별 추출값 출력 (필요 시 주석 해제)
        # print(f"발급일자 영역 텍스트: '{issuedDate}'")
        # print(f"성명 영역 텍스트: '{personName}'")
        # print(f"주민등록번호 영역 텍스트: '{residentNum}'")
        # print(f"주소 영역 텍스트: '{address}'")
        # print(f"초본 종류 영역 텍스트: '{certificateType}'")

        result = (
            f"발급일자: {issuedDate}\n"
            f"성명: {personName}\n"
            f"주민등록번호: {residentNum}\n"
            f"주소: {address}\n"
            f"초본 종류: {certificateType}\n"
        )
        return result


if __name__ == "__main__":
    pororo_test = testPororo()
    result = pororo_test.preprocessImageObject()
    print("OCR 인식 결과:")
    print(result)
