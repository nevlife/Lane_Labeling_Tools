#!/usr/bin/env python3
"""
🗂️ 디렉토리 동기화 정리 도구 (Directory Sync Cleanup Tool)

=== 주요 기능 ===
✅ 기준 디렉토리를 참조하여 정리 대상 디렉토리에서 불필요한 파일들을 삭제
✅ 파일명 기반 비교: 기준 디렉토리에 없는 파일들을 자동 식별
✅ 일방향 동기화: 기준 디렉토리 → 정리 대상 디렉토리로 파일 목록 동기화
✅ 안전한 삭제: 개별 파일 삭제 상태 확인 및 에러 처리

=== 사용 사례 ===
🔸 머신러닝 데이터셋의 Label과 Image 파일 동기화
🔸 백업 디렉토리와 원본 디렉토리의 파일 목록 일치화
🔸 프로젝트 정리 시 불필요한 파일들 자동 제거
🔸 데이터 전처리 후 매칭되지 않는 파일들 정리

=== 동기화 로직 ===
📂 기준 디렉토리: [A.jpg, B.jpg, C.jpg]
📂 정리 대상: [A.txt, B.txt, C.txt, D.txt, E.txt]
📂 삭제 대상: [D.txt, E.txt] (기준에 없는 파일들)
📂 결과: [A.txt, B.txt, C.txt] (기준과 일치)

=== 기술적 특징 ===
🔧 Set 자료구조를 사용한 효율적인 파일명 비교
🔧 파일명만 비교하므로 확장자 차이 허용
🔧 Path 객체를 사용한 안전한 파일 시스템 조작
🔧 상세한 삭제 과정 로그 및 통계 정보 제공
"""
import sys
import os
from pathlib import Path

def sync_delete_files(source_dir, target_dir):
    """
    기준 디렉토리에 없는 파일들을 정리 대상 디렉토리에서 삭제하는 메인 함수
    
    Args:
        source_dir (str): 기준이 되는 디렉토리 경로 (참조용, 수정되지 않음)
        target_dir (str): 정리할 디렉토리 경로 (파일이 삭제될 디렉토리)
        
    Algorithm:
        1. 기준 디렉토리의 모든 파일명을 Set으로 수집
        2. 정리 대상 디렉토리의 각 파일을 기준 Set과 비교
        3. 기준에 없는 파일들을 삭제 대상으로 식별
        4. 삭제 대상 파일들을 하나씩 안전하게 삭제
        5. 삭제 결과 통계 출력
        
    Safety Features:
        - 개별 파일 삭제로 부분 실패 시에도 작업 계속
        - 예외 처리로 권한 문제 등 에러 상황 대응
        - 상세한 삭제 로그로 작업 추적 가능
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    print(f"📂 기준 디렉토리: {source_path}")
    print(f"📂 정리 대상 디렉토리: {target_path}")
    print("-" * 50)
    
    # 기준 디렉토리의 파일명 수집 (확장자 포함)
    source_files = set()
    if source_path.exists():
        source_files = {f.name for f in source_path.iterdir() if f.is_file()}
        print(f"📊 기준 디렉토리 파일 개수: {len(source_files)}")
    else:
        print(f"⚠️ 기준 디렉토리가 없습니다: {source_path}")
        return
    
    # 정리 대상 디렉토리 존재 확인
    if not target_path.exists():
        print(f"⚠️ 정리 대상 디렉토리가 없습니다: {target_path}")
        return
    
    # 정리 대상 디렉토리의 파일 목록 수집
    target_files = [f for f in target_path.iterdir() if f.is_file()]
    print(f"📊 정리 대상 디렉토리 파일 개수: {len(target_files)}")
    
    if not target_files:
        print("ℹ️ 정리 대상 디렉토리에 파일이 없습니다.")
        return
    
    print()
    print("🔍 파일 비교 및 삭제 작업 시작...")
    print()
    
    # 파일별 처리 및 삭제 작업
    deleted_count = 0
    kept_count = 0
    error_count = 0
    
    # 삭제 대상 파일들을 먼저 식별
    files_to_delete = []
    files_to_keep = []
    
    for target_file in target_files:
        filename = target_file.name
        if filename not in source_files:
            files_to_delete.append(target_file)
        else:
            files_to_keep.append(target_file)
    
    # 삭제 작업 미리보기
    if files_to_delete:
        print(f"🗑️ 삭제 예정 파일들 ({len(files_to_delete)}개):")
        for file_to_delete in files_to_delete[:10]:  # 처음 10개만 미리보기
            print(f"   - {file_to_delete.name}")
        if len(files_to_delete) > 10:
            print(f"   ... 외 {len(files_to_delete) - 10}개")
        print()
    
    # 실제 삭제 작업 수행
    for target_file in target_files:
        filename = target_file.name
        
        if filename not in source_files:
            # 기준 디렉토리에 없는 파일 → 삭제
            try:
                target_file.unlink()
                print(f"✅ 삭제됨: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 삭제 실패: {filename} - {e}")
                error_count += 1
        else:
            # 기준 디렉토리에 있는 파일 → 유지
            print(f"⚪ 유지됨: {filename}")
            kept_count += 1
    
    # 최종 결과 통계 출력
    print()
    print("-" * 50)
    print("📊 동기화 정리 작업 완료!")
    print(f"🗑️ 삭제된 파일: {deleted_count}개")
    print(f"📁 유지된 파일: {kept_count}개")
    if error_count > 0:
        print(f"❌ 삭제 실패: {error_count}개")
    
    # 동기화 성공률 계산
    total_processed = deleted_count + kept_count + error_count
    if total_processed > 0:
        success_rate = (deleted_count + kept_count) / total_processed * 100
        print(f"📈 작업 성공률: {success_rate:.1f}%")
    
    # 동기화 결과 확인
    remaining_files = len([f for f in target_path.iterdir() if f.is_file()])
    expected_files = len(source_files)
    print(f"🎯 동기화 결과: {remaining_files}개 파일 (기준: {expected_files}개)")

if __name__ == "__main__":
    """
    메인 실행 부분 - 하드코딩된 경로로 실행
    
    ⚠️ 중요 주의사항:
    1. 이 도구는 파일을 영구적으로 삭제합니다 (휴지통 이동 아님)
    2. 실행 전 반드시 백업을 생성하세요
    3. 기준 디렉토리는 수정되지 않습니다
    4. 정리 대상 디렉토리에서만 파일이 삭제됩니다
    
    💡 사용 시나리오:
    - 이미지 파일과 라벨 파일을 동기화할 때
    - 전처리 후 매칭되지 않는 파일들을 정리할 때
    - 백업 디렉토리를 원본과 일치시킬 때
    """
    # 하드코딩된 디렉토리 경로들
    source = "C:/Users/USER/Documents/dataset/image/train"           # 기준 디렉토리 (참조용)
    target = "C:/Users/USER/Documents/dataset/ll_seg_annotations/train"  # 정리 대상 디렉토리 (파일 삭제됨)
    
    # 필수 디렉토리 존재 확인
    source_path = Path(source)
    target_path = Path(target)
    
    if not source_path.exists():
        print(f"❌ 기준 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not target_path.exists():
        print(f"❌ 정리 대상 디렉토리가 없습니다: {target}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 사용자 확인 및 실행
    print("=" * 70)
    print("🗂️ 디렉토리 동기화 정리 도구")
    print("=" * 70)
    print(f"📂 기준 디렉토리: {source}")
    print(f"📂 정리 대상: {target}")
    print()
    print("⚠️ 주의: 기준 디렉토리에 없는 파일들이 정리 대상에서 삭제됩니다!")
    print("📝 동작: 정리 대상 디렉토리를 기준 디렉토리와 일치하도록 동기화")
    print()
    
    response = input("정말로 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    sync_delete_files(source, target) 