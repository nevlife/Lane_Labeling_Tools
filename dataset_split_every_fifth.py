#!/usr/bin/env python3
"""
📊 데이터셋 5분할 도구 (Dataset Split Every Fifth Tool)

=== 주요 기능 ===
✅ 정렬된 파일 목록에서 5번째마다 파일을 선택하여 다른 디렉토리로 이동
✅ 순차적 분할: 인덱스 기반으로 5, 10, 15, 20... 번째 파일들을 선택
✅ 자동 정렬: 파일명 순서대로 정렬하여 일관된 분할 결과 보장
✅ 안전한 이동: 파일 충돌 시 덮어쓰기 경고 및 처리

=== 사용 사례 ===
🔸 머신러닝 데이터셋을 Train/Validation으로 분할할 때 (20% 추출)
🔸 대용량 데이터셋에서 샘플링을 통한 부분집합 생성
🔸 순차적 데이터에서 일정 간격으로 테스트 데이터 추출
🔸 시계열 데이터에서 주기적 샘플링

=== 분할 패턴 ===
📂 Source: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ...]
📂 Target: [5, 10, 15, ...] (5번째마다 이동)
📂 Remain: [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, ...] (나머지 유지)

=== 기술적 특징 ===
🔧 파일명 기반 자동 정렬로 일관된 분할
🔧 모듈로 연산(%)을 사용한 효율적인 주기 선택
🔧 Path 객체를 사용한 안전한 파일 시스템 조작
🔧 예외 처리를 통한 안정적인 파일 이동
"""
import sys
import os
import shutil
from pathlib import Path

def move_every_fifth_file(source_dir, target_dir):
    """
    원본 디렉토리에서 5번째마다 있는 파일을 대상 디렉토리로 이동하는 메인 함수
    
    Args:
        source_dir (str): 원본 파일들이 있는 디렉토리 경로
        target_dir (str): 선택된 파일들이 이동될 디렉토리 경로
        
    Algorithm:
        1. 원본 디렉토리의 모든 파일을 이름순으로 정렬
        2. 인덱스가 5의 배수인 파일들을 선택 (5, 10, 15, 20...)
        3. 선택된 파일들을 대상 디렉토리로 이동
        4. 이동 결과 통계 출력
        
    Math Logic:
        - 파일 인덱스 i (0부터 시작)
        - 조건: (i + 1) % 5 == 0
        - 결과: 5번째, 10번째, 15번째... 파일이 선택됨
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    print(f"📂 원본 디렉토리: {source_path}")
    print(f"📂 이동 대상 디렉토리: {target_path}")
    print("-" * 50)
    
    # 원본 디렉토리 존재 확인
    if not source_path.exists():
        print(f"⚠️ 원본 디렉토리가 없습니다: {source_path}")
        return
    
    # 대상 디렉토리 자동 생성
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 파일 목록을 이름순으로 정렬하여 일관된 결과 보장
    source_files = sorted([f for f in source_path.iterdir() if f.is_file()])
    print(f"📊 원본 디렉토리 파일 개수: {len(source_files)}")
    
    if len(source_files) == 0:
        print("⚠️ 이동할 파일이 없습니다.")
        return
    
    # 예상 이동 파일 개수 계산 및 출력
    expected_move_count = len(source_files) // 5
    print(f"📊 예상 이동 파일 개수: {expected_move_count}개 (전체의 {expected_move_count/len(source_files)*100:.1f}%)")
    print()
    
    # 5번째마다 파일 선택 및 이동
    moved_count = 0
    error_count = 0
    
    for i, source_file in enumerate(source_files):
        file_number = i + 1  # 1부터 시작하는 파일 번호
        
        if file_number % 5 == 0:  # 5번째마다 선택 (5, 10, 15, 20, ...)
            target_file = target_path / source_file.name
            
            try:
                # 파일명 중복 시 덮어쓰기 경고
                if target_file.exists():
                    print(f"⚠️ 기존 파일 덮어쓰기: {target_file}")
                
                # 파일 이동 실행
                shutil.move(str(source_file), str(target_file))
                print(f"✅ [{file_number:4d}번째] 이동됨: {source_file.name}")
                moved_count += 1
            except Exception as e:
                print(f"❌ [{file_number:4d}번째] 이동 실패: {source_file.name} - {e}")
                error_count += 1
        else:
            # 이동하지 않는 파일들은 간단히 표시 (너무 많으면 생략)
            if len(source_files) <= 50:  # 파일 수가 적을 때만 전체 표시
                print(f"⚪ [{file_number:4d}번째] 유지됨: {source_file.name}")
    
    # 최종 결과 통계 출력
    print()
    print("-" * 50)
    print(f"📦 총 {moved_count}개 파일이 이동되었습니다.")
    print(f"📁 {len(source_files) - moved_count}개 파일이 원본에 남아있습니다.")
    if error_count > 0:
        print(f"❌ {error_count}개 파일에서 이동 오류가 발생했습니다.")
    
    # 분할 비율 정보
    if len(source_files) > 0:
        move_ratio = moved_count / len(source_files) * 100
        print(f"📊 실제 분할 비율: {move_ratio:.1f}% (목표: 20%)")

if __name__ == "__main__":
    """
    메인 실행 부분 - 하드코딩된 경로로 실행
    
    ⚠️ 실행 전 확인사항:
    1. Source 디렉토리에 분할할 파일들이 있는지 확인
    2. Target 디렉토리는 자동으로 생성됨
    3. 파일 이동은 되돌릴 수 없으므로 백업 권장
    4. 5번째마다 선택되는 로직 확인
    
    💡 사용 팁:
    - 파일명이 정렬 가능한 형태여야 일관된 결과를 얻을 수 있음
    - 숫자 파일명인 경우 제로패딩(000001, 000002...)이 권장됨
    """
    # 하드코딩된 디렉토리 경로들
    source = "C:/Users/USER/Tools/dataset_splitter_5th/source"  # 원본 파일들이 있는 디렉토리
    target = "C:/Users/USER/Tools/dataset_splitter_5th/target"  # 5번째마다 선택된 파일들이 이동될 디렉토리
    
    # 필수 디렉토리 존재 확인
    source_path = Path(source)
    
    if not source_path.exists():
        print(f"❌ 원본 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 사용자 확인 및 실행
    print("=" * 70)
    print("📊 데이터셋 5분할 도구 (Every 5th File Mover)")
    print("=" * 70)
    print(f"📂 원본: {source}")
    print(f"📂 대상: {target}")
    print()
    print("⚠️ 주의: 5번째마다 있는 파일들이 원본에서 대상 디렉토리로 이동됩니다!")
    print("📝 동작: 정렬된 파일 목록에서 5, 10, 15, 20... 번째 파일들을 이동")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    move_every_fifth_file(source, target) 