"""
1. cv2.imshow() 대신 리사이즈해서 출력
전처리된 이미지를 확대하거나 축소해서 출력해 보세요:

# 전처리 결과 이미지가 너무 클 경우 대비하여 리사이즈
def show_image_resized(image, window_name="Processed", max_width=1200, max_height=800):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    resized = cv2.resize(image, (int(w * scale), int(h * scale)))
    cv2.imshow(window_name, resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
그리고 test.py에 다음처럼 적용:

# 기존 코드
# cv2.imshow("Processed Image", processedImage)

# 변경 코드
show_image_resized(processedImage)
2. 이미지가 짤리는 경우 — 원인 추정
전처리 로직(PreprocessImage 또는 BinarizeImage) 중 일부에서 다음과 같은 코드를 사용하는 경우 확인하세요:

image = image.crop(...)  # 잘리는 원인
image = image.resize(...)  # 과도한 확대/축소 원인
불필요하게 **크롭(crop)**하거나 고정 크기 리사이징(resize) 하고 있다면 제거하거나 image.size를 유지하도록 수정해야 합니다.

3. 이미지 저장해 확인
imshow() 대신 이미지 저장 후 확인하면 확대/축소/손실 여부를 명확히 알 수 있어요:

cv2.imwrite("output_preview.png", processedImage)
print("이미지 저장 완료: output_preview.png")
"""