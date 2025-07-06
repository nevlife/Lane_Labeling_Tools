import json
import numpy as np
import cv2
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def load_coco_annotations(json_path):
    """COCO JSON 파일을 로드합니다."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_binary_mask_from_segmentation(segmentation, image_width, image_height):
    """세그멘테이션 좌표로부터 이진 마스크를 생성합니다."""
    # 빈 마스크 생성
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    
    # PIL Image로 변환하여 다각형 그리기
    pil_mask = Image.fromarray(mask)
    draw = ImageDraw.Draw(pil_mask)
    
    # 세그멘테이션 좌표를 정수로 변환
    if isinstance(segmentation, list):
        # 첫 번째 세그멘테이션 사용 (보통 하나만 있음)
        coords = segmentation[0]
        # 좌표를 (x, y) 쌍으로 변환
        points = [(int(coords[i]), int(coords[i+1])) for i in range(0, len(coords), 2)]
        
        # 다각형 그리기 (흰색으로 채우기)
        draw.polygon(points, fill=255)
    
    # numpy 배열로 변환
    mask = np.array(pil_mask)
    return mask

def create_binary_masks_from_coco(json_path, output_dir="binary_masks"):
    """COCO 어노테이션으로부터 모든 이미지의 이진 마스크를 생성합니다."""
    
    # COCO 데이터 로드
    coco_data = load_coco_annotations(json_path)
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 이미지 정보를 딕셔너리로 변환 (빠른 검색을 위해)
    images_dict = {img['id']: img for img in coco_data['images']}
    
    # 어노테이션을 이미지별로 그룹화
    annotations_by_image = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    print(f"총 {len(coco_data['images'])}개 이미지에서 마스크를 생성합니다...")
    
    # 처리 결과 추적
    processed_files = []
    black_mask_files = []
    
    # 각 이미지에 대해 마스크 생성
    for image_info in coco_data['images']:
        image_id = image_info['id']
        image_name = image_info['file_name']
        width = image_info['width']
        height = image_info['height']
        
        # 변환 후 파일명 사용 (해시값이 붙은 jpg 파일명)
        if image_name.endswith('.jpg'):
            base_name = image_name[:-4]  # .jpg 제거
        else:
            base_name = image_name
        
        # 해당 이미지의 어노테이션들 가져오기
        annotations = annotations_by_image.get(image_id, [])
        
        # 빈 마스크 생성 (검은색)
        combined_mask = np.zeros((height, width), dtype=np.uint8)
        
        if not annotations:
            print(f"검은색 마스크 생성: {image_name} (어노테이션 없음)")
            black_mask_files.append(image_name)
        else:
            # 모든 어노테이션을 하나의 마스크에 합치기
            for ann in annotations:
                segmentation = ann['segmentation']
                mask = create_binary_mask_from_segmentation(segmentation, width, height)
                combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # 마스크 저장
        output_path = os.path.join(output_dir, f"{base_name}.jpg")
        cv2.imwrite(output_path, combined_mask)
        
        print(f"생성됨: {output_path}")
        processed_files.append(image_name)
    
    print(f"\n모든 마스크가 {output_dir} 폴더에 저장되었습니다!")
    
    # 처리 결과 요약
    print(f"\n=== 처리 결과 요약 ===")
    print(f"전체 이미지 수: {len(coco_data['images'])}")
    print(f"정상 마스크 생성 파일 수: {len(processed_files) - len(black_mask_files)}")
    print(f"검은색 마스크 생성 파일 수: {len(black_mask_files)}")
    print(f"총 처리된 파일 수: {len(processed_files)}")
    
    if black_mask_files:
        print(f"\n검은색 마스크로 저장된 파일들 (어노테이션 없음):")
        for file in black_mask_files:
            print(f"  - {file}")
    
    print(f"\n모든 파일이 성공적으로 처리되었습니다!")

def visualize_masks(json_path, num_samples=3):
    """몇 개의 마스크를 시각화합니다."""
    coco_data = load_coco_annotations(json_path)
    images_dict = {img['id']: img for img in coco_data['images']}
    
    # 어노테이션을 이미지별로 그룹화
    annotations_by_image = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    # 샘플 이미지들 시각화
    sample_count = 0
    for image_info in coco_data['images'][:num_samples]:
        image_id = image_info['id']
        width = image_info['width']
        height = image_info['height']
        image_name = image_info['file_name']
        
        annotations = annotations_by_image.get(image_id, [])
        if not annotations:
            continue
        
        # 마스크 생성
        combined_mask = np.zeros((height, width), dtype=np.uint8)
        for ann in annotations:
            segmentation = ann['segmentation']
            mask = create_binary_mask_from_segmentation(segmentation, width, height)
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # 시각화
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(combined_mask, cmap='gray')
        plt.title(f'Binary Mask: {image_name}')
        plt.axis('off')
        
        # 바운딩 박스도 그려보기
        plt.subplot(1, 2, 2)
        blank_img = np.zeros((height, width, 3), dtype=np.uint8)
        for ann in annotations:
            bbox = ann['bbox']  # [x, y, width, height]
            x, y, w, h = bbox
            cv2.rectangle(blank_img, (int(x), int(y)), (int(x+w), int(y+h)), (255, 255, 255), 2)
        plt.imshow(blank_img)
        plt.title('Bounding Boxes')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        sample_count += 1
        if sample_count >= num_samples:
            break

if __name__ == "__main__":
    json_path = "C:/Users/USER/Lane_Labeling_Tools/create_binary_masks/_annotations.coco.json"
    
    # 마스크 생성
    print("이진 마스크를 생성합니다...")
    create_binary_masks_from_coco(json_path)
    
    # 샘플 시각화 (선택사항)
    print("\n샘플 마스크를 시각화합니다...")
    visualize_masks(json_path, num_samples=2) 