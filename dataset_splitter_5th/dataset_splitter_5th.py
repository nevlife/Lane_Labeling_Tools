#!/usr/bin/env python3
"""
파일 이동 도구
디렉토리1에서 N번째마다 있는 파일을 디렉토리2로 이동하는 도구
"""
import sys
import os
import shutil
from pathlib import Path

# 설정 변수
MOVE_INTERVAL = 5  # 2개 중 1개 이동 (원하는 간격으로 변경 가능)

def move_every_nth_file(source_dir, target_dir, interval=MOVE_INTERVAL):
    """디렉토리1에서 N번째마다 있는 파일을 디렉토리2로 이동"""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    print(f"원본 디렉토리: {source_path}")
    print(f"이동 대상 디렉토리: {target_path}")
    print(f"이동 간격: {interval}개 중 1개")
    print("-" * 50)
    
    # 디렉토리1의 파일 목록
    if not source_path.exists():
        print(f"⚠️ 원본 디렉토리가 없습니다: {source_path}")
        return
    
    # 대상 디렉토리 생성 (없으면)
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 파일 목록을 정렬된 순서로 가져오기
    source_files = sorted([f for f in source_path.iterdir() if f.is_file()])
    print(f"원본 디렉토리 파일 개수: {len(source_files)}")
    
    if len(source_files) == 0:
        print("⚠️ 이동할 파일이 없습니다.")
        return
    
    print()
    
    # N번째마다 파일 선택 (interval에 따라)
    moved_count = 0
    
    for i, source_file in enumerate(source_files):
        if (i + 1) % interval == 0:  # N번째마다
            target_file = target_path / source_file.name
            
            try:
                # 같은 이름의 파일이 있으면 덮어쓰기
                if target_file.exists():
                    print(f"⚠️ 기존 파일 덮어쓰기: {target_file}")
                
                shutil.move(str(source_file), str(target_file))
                print(f"✓ 이동됨: {source_file.name} -> {target_file}")
                moved_count += 1
            except Exception as e:
                print(f"❌ 이동 실패: {source_file.name} - {e}")
        else:
            print(f"⚪ 유지됨: {source_file.name}")
    
    print()
    print("-" * 50)
    print(f"📦 총 {moved_count}개 파일이 이동되었습니다.")
    print(f"📁 {len(source_files) - moved_count}개 파일이 원본에 남아있습니다.")

if __name__ == "__main__":
    # 하드코딩된 디렉토리 경로
    source = "C:/Users/USER/Lane_Labeling_Tools/dataset_splitter_5th/input"
    target = "C:/Users/USER/Lane_Labeling_Tools/dataset_splitter_5th/output"
    
    # 디렉토리 존재 여부 확인
    source_path = Path(source)
    
    if not source_path.exists():
        print(f"원본 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 확인 메시지
    print("=" * 60)
    print("📦 파일 이동 도구")
    print("=" * 60)
    print(f"원본: {source}")
    print(f"대상: {target}")
    print(f"간격: {MOVE_INTERVAL}개 중 1개 이동")
    print()
    print(f"⚠️ {MOVE_INTERVAL}번째마다 있는 파일들이 이동됩니다!")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    move_every_nth_file(source, target)