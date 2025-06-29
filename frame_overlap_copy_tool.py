#!/usr/bin/env python3
"""
🎯 Frame 중복 파일 복사 도구 (Frame Overlap Copy Tool)

=== 주요 기능 ===
✅ Source 디렉토리와 Train 디렉토리에서 같은 frame 번호를 가진 파일들을 찾아서 복사
✅ frame 번호 추출: 파일명에서 정규식을 사용하여 frame_XXXXXX 패턴 인식
✅ 중복 감지: Source의 frame 번호와 Train의 frame 번호를 비교
✅ 선택적 복사: 중복된 frame 번호를 가진 Train 파일들만 Output 디렉토리로 복사

=== 사용 사례 ===
🔸 머신러닝 데이터셋에서 특정 frame들만 필터링할 때
🔸 비디오 프레임 데이터에서 중복 프레임을 별도로 관리할 때
🔸 대용량 이미지 데이터셋에서 특정 조건의 파일들만 추출할 때

=== 파일명 패턴 예시 ===
📁 Source: frame_000004_png.rf.bc57731e2806e1eb3e0b4d66077b3627.jpg
📁 Train: frame_000004.png
📁 Output: frame_000004.png (Train에서 복사됨)

=== 기술적 특징 ===
🔧 정규식 패턴 매칭을 통한 frame 번호 추출
🔧 Set을 사용한 효율적인 중복 검사
🔧 파일 존재 여부 확인 및 덮어쓰기 처리
🔧 상세한 진행 상황 출력 및 에러 핸들링
"""
import sys
import os
import shutil
import re
from pathlib import Path

def extract_frame_number(filename):
    """
    파일명에서 frame 번호를 추출하는 함수
    
    Args:
        filename (str): 분석할 파일명
        
    Returns:
        str: 추출된 frame 번호 (예: "000004") 또는 None
        
    Examples:
        >>> extract_frame_number("frame_000004_png.rf.bc57731e2806e1eb3e0b4d66077b3627.jpg")
        "000004"
        >>> extract_frame_number("frame_003754.png")
        "003754"
    """
    # 정규식으로 frame_XXXXXX 패턴에서 숫자 부분만 추출
    match = re.search(r'frame_(\d+)', filename)
    if match:
        return match.group(1)
    return None

def get_source_frame_numbers(source_dir):
    """
    Source 디렉토리에서 모든 frame 번호들을 수집하는 함수
    
    Args:
        source_dir (str): Source 디렉토리 경로
        
    Returns:
        set: 고유한 frame 번호들의 집합
    """
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
    """
    Source와 중복된 frame 번호를 가진 Train 파일들을 Output으로 복사하는 메인 함수
    
    Args:
        source_dir (str): 기준이 되는 Source 디렉토리 경로
        train_dir (str): 복사할 파일들이 있는 Train 디렉토리 경로
        output_dir (str): 복사된 파일들이 저장될 Output 디렉토리 경로
        
    Processing Flow:
        1. 디렉토리 존재 여부 확인
        2. Source 디렉토리에서 frame 번호 목록 추출
        3. Train 디렉토리에서 일치하는 frame 번호 파일 검색
        4. 중복 파일들을 Output 디렉토리로 복사
        5. 복사 결과 통계 출력
    """
    train_path = Path(train_dir)
    output_path = Path(output_dir)
    
    print(f"📂 Source 디렉토리: {source_dir}")
    print(f"📂 Train 디렉토리: {train_path}")
    print(f"📂 Output 디렉토리: {output_path}")
    print("-" * 50)
    
    # 디렉토리 존재 확인
    if not train_path.exists():
        print(f"⚠️ Train 디렉토리가 없습니다: {train_path}")
        return
    
    # Output 디렉토리 생성 (없으면 자동 생성)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Source 디렉토리의 frame 번호들 수집
    source_frames = get_source_frame_numbers(source_dir)
    print(f"📊 Source 디렉토리의 frame 번호 개수: {len(source_frames)}")
    
    if not source_frames:
        print("⚠️ Source 디렉토리에 frame 파일이 없습니다.")
        return
    
    # Train 디렉토리에서 중복된 frame 번호를 가진 파일들 검색
    train_files = list(train_path.iterdir())
    overlapping_files = []
    
    print(f"📊 Train 디렉토리의 총 파일 개수: {len([f for f in train_files if f.is_file()])}")
    print()
    
    # 중복 frame 번호 파일 찾기 및 출력
    for file in train_files:
        if file.is_file():
            frame_num = extract_frame_number(file.name)
            if frame_num and frame_num in source_frames:
                overlapping_files.append(file)
                print(f"🎯 중복 발견: {file.name} (frame_{frame_num})")
    
    # 중복 파일이 없는 경우 디버깅 정보 출력
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
    
    # 파일 복사 실행
    copied_count = 0
    
    for file in overlapping_files:
        output_file = output_path / file.name
        
        try:
            # 같은 이름의 파일이 있으면 덮어쓰기 경고
            if output_file.exists():
                print(f"⚠️ 기존 파일 덮어쓰기: {output_file}")
            
            # 파일 복사 (메타데이터 포함)
            shutil.copy2(str(file), str(output_file))
            print(f"✅ 복사됨: {file.name}")
            copied_count += 1
        except Exception as e:
            print(f"❌ 복사 실패: {file.name} - {e}")
    
    # 최종 결과 요약
    print()
    print("-" * 50)
    print(f"📦 총 {copied_count}개 Train 파일이 Output으로 복사되었습니다.")

if __name__ == "__main__":
    """
    메인 실행 부분 - 하드코딩된 경로로 실행
    
    ⚠️ 실행 전 확인사항:
    1. Source 디렉토리에 기준이 되는 frame 파일들이 있는지 확인
    2. Train 디렉토리에 복사할 파일들이 있는지 확인
    3. Output 디렉토리는 자동으로 생성됨
    """
    # 하드코딩된 디렉토리 경로들
    source = "C:/Users/USER/Tools/LongToShort/source"    # 기준 frame들이 있는 디렉토리
    train = "C:/Users/USER/Tools/LongToShort/train"      # 복사할 파일들이 있는 디렉토리
    output = "C:/Users/USER/Tools/LongToShort/output"    # 복사된 파일들이 저장될 디렉토리
    
    # 필수 디렉토리 존재 여부 확인
    source_path = Path(source)
    train_path = Path(train)
    
    if not source_path.exists():
        print(f"❌ Source 디렉토리가 없습니다: {source}")
        sys.exit(1)
        
    if not train_path.exists():
        print(f"❌ Train 디렉토리가 없습니다: {train}")
        sys.exit(1)
    
    # 사용자 확인 및 실행
    print("=" * 70)
    print("🎯 Frame 중복 파일 복사 도구")
    print("=" * 70)
    print(f"📂 Source: {source}")
    print(f"📂 Train: {train}")
    print(f"📂 Output: {output}")
    print()
    print("📝 동작: Source와 같은 frame 번호를 가진 Train 파일들을 Output으로 복사")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    copy_overlapping_train_files(source, train, output) 