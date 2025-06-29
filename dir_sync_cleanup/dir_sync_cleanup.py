#!/usr/bin/env python3
"""
디렉토리 동기화 삭제 도구
디렉토리1에 없는 파일이 디렉토리2에 있으면 삭제하는 일회성 동기화 도구
"""
import sys
import os
from pathlib import Path

def sync_delete_files(source_dir, target_dir):
    """디렉토리1에 없는 파일들을 디렉토리2에서 삭제"""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    print(f"기준 디렉토리: {source_path}")
    print(f"정리 대상 디렉토리: {target_path}")
    print("-" * 50)
    
    # 디렉토리1의 파일 목록 (파일명만)
    source_files = set()
    if source_path.exists():
        source_files = {f.name for f in source_path.iterdir() if f.is_file()}
        print(f"기준 디렉토리 파일 개수: {len(source_files)}")
    else:
        print(f"⚠️ 기준 디렉토리가 없습니다: {source_path}")
        return
    
    # 디렉토리2의 파일 목록
    if not target_path.exists():
        print(f"⚠️ 정리 대상 디렉토리가 없습니다: {target_path}")
        return
    
    target_files = [f for f in target_path.iterdir() if f.is_file()]
    print(f"정리 대상 디렉토리 파일 개수: {len(target_files)}")
    print()
    
    # 디렉토리1에 없는 파일들을 디렉토리2에서 찾아 삭제
    deleted_count = 0
    
    for target_file in target_files:
        filename = target_file.name
        
        if filename not in source_files:
            try:
                target_file.unlink()
                print(f"✓ 삭제됨: {target_file}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 삭제 실패: {target_file} - {e}")
        else:
            print(f"⚪ 유지됨: {target_file}")
    
    print()
    print("-" * 50)
    print(f"🗑️ 총 {deleted_count}개 파일이 삭제되었습니다.")
    print(f"📁 {len(target_files) - deleted_count}개 파일이 유지되었습니다.")

if __name__ == "__main__":
    # 하드코딩된 디렉토리 경로
    source = "C:/Users/USER/Tools/raw"
    target = "C:/Users/USER/Tools/seg"
    
    # 디렉토리 존재 여부 확인
    source_path = Path(source)
    target_path = Path(target)
    
    if not source_path.exists():
        print(f"기준 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not target_path.exists():
        print(f"정리 대상 디렉토리가 없습니다: {target}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 확인 메시지
    print("=" * 60)
    print("📁 디렉토리 동기화 삭제 도구")
    print("=" * 60)
    print(f"기준: {source}")
    print(f"정리: {target}")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    sync_delete_files(source, target)