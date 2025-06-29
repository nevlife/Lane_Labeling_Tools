#!/usr/bin/env python3
"""
파일 복사 도구
source와 중복된 frame 번호를 가진 train의 png 파일들을 output 디렉토리로 복사하는 도구
"""
import sys
import os
import shutil
import re
from pathlib import Path

def extract_frame_number(filename):
    """파일명에서 frame 번호 추출"""
    # source: frame_000004_png.rf.bc57731e2806e1eb3e0b4d66077b3627.jpg -> 000004
    # train: frame_003754.png -> 003754
    match = re.search(r'frame_(\d+)', filename)
    if match:
        return match.group(1)
    return None

def get_source_frame_numbers(source_dir):
    """source 디렉토리에서 모든 frame 번호들을 가져오기"""
    source_path = Path(source_dir)
    source_frames = set()
    
    if source_path.exists():
        for file in source_path.iterdir():
            if file.is_file():
                frame_num = extract_frame_number(file.name)
                if frame_num:
                    source_frames.add(frame_num)
    
    return source_frames

def copy_overlapping_train_files(source_dir, train_dir, output_dir):
    """source와 중복된 frame 번호를 가진 train 파일들을 output으로 복사"""
    train_path = Path(train_dir)
    output_path = Path(output_dir)
    
    print(f"Source 디렉토리: {source_dir}")
    print(f"Train 디렉토리: {train_path}")
    print(f"Output 디렉토리: {output_path}")
    print("-" * 50)
    
    # 디렉토리 존재 확인
    if not train_path.exists():
        print(f"⚠️ Train 디렉토리가 없습니다: {train_path}")
        return
    
    # output 디렉토리 생성 (없으면)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # source 디렉토리의 frame 번호들 가져오기
    source_frames = get_source_frame_numbers(source_dir)
    print(f"Source 디렉토리의 frame 번호 개수: {len(source_frames)}")
    
    if not source_frames:
        print("⚠️ Source 디렉토리에 frame 파일이 없습니다.")
        return
    
    # train 디렉토리에서 중복된 frame 번호를 가진 파일들 찾기
    train_files = list(train_path.iterdir())
    overlapping_files = []
    
    print(f"Train 디렉토리의 총 파일 개수: {len([f for f in train_files if f.is_file()])}")
    print()
    
    for file in train_files:
        if file.is_file():
            frame_num = extract_frame_number(file.name)
            if frame_num and frame_num in source_frames:
                overlapping_files.append(file)
                print(f"🎯 중복 발견: {file.name} (frame_{frame_num})")
    
    if not overlapping_files:
        print("⚠️ Source와 Train에 공통된 frame 번호가 없습니다.")
        print()
        print("📋 Source의 frame 번호들 (처음 10개):")
        for i, frame in enumerate(sorted(source_frames)[:10]):
            print(f"  {i+1}. frame_{frame}")
        
        print()
        print("📋 Train의 frame 번호들 (처음 10개):")
        train_frames = set()
        for file in train_files:
            if file.is_file():
                frame_num = extract_frame_number(file.name)
                if frame_num:
                    train_frames.add(frame_num)
        
        for i, frame in enumerate(sorted(train_frames)[:10]):
            print(f"  {i+1}. frame_{frame}")
        
        return
    
    print()
    print(f"🎯 복사할 Train 파일 개수: {len(overlapping_files)}개")
    print()
    
    # 파일들 복사
    copied_count = 0
    
    for file in overlapping_files:
        output_file = output_path / file.name
        
        try:
            # 같은 이름의 파일이 있으면 덮어쓰기
            if output_file.exists():
                print(f"⚠️ 기존 파일 덮어쓰기: {output_file}")
            
            shutil.copy2(str(file), str(output_file))
            print(f"✓ 복사됨: {file.name}")
            copied_count += 1
        except Exception as e:
            print(f"❌ 복사 실패: {file.name} - {e}")
    
    print()
    print("-" * 50)
    print(f"📦 총 {copied_count}개 Train 파일이 output으로 복사되었습니다.")

if __name__ == "__main__":
    # 실제 디렉토리 경로
    source = "C:/Users/USER/Tools/LongToShort/source"
    train = "C:/Users/USER/Tools/LongToShort/train"
    output = "C:/Users/USER/Tools/LongToShort/output"
    
    # 디렉토리 존재 여부 확인
    source_path = Path(source)
    train_path = Path(train)
    
    if not source_path.exists():
        print(f"Source 디렉토리가 없습니다: {source}")
        sys.exit(1)
        
    if not train_path.exists():
        print(f"Train 디렉토리가 없습니다: {train}")
        sys.exit(1)
    
    # 확인 메시지
    print("=" * 60)
    print("🎯 중복 Frame Train 파일 복사 도구")
    print("=" * 60)
    print(f"Source: {source}")
    print(f"Train: {train}")
    print(f"Output: {output}")
    print()
    print("📝 동작: Source와 같은 frame 번호를 가진 Train 파일들을 Output으로 복사")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    copy_overlapping_train_files(source, train, output)
