#!/usr/bin/env python3
"""
디렉토리 파일 삭제 도구
디렉토리1에서 디렉토리2에 있는 같은 이름의 파일들을 삭제하는 도구
"""
import sys
import os
from pathlib import Path

def delete_matching_files(directory1, directory2):
    """디렉토리1에서 디렉토리2에 있는 같은 이름의 파일들을 삭제"""
    dir1_path = Path(directory1)
    dir2_path = Path(directory2)
    
    print(f"디렉토리1 (삭제 대상): {dir1_path}")
    print(f"디렉토리2 (삭제 기준): {dir2_path}")
    print("-" * 50)
    
    # 디렉토리 존재 확인
    if not dir1_path.exists():
        print(f"⚠️ 디렉토리1이 없습니다: {dir1_path}")
        return
    
    if not dir2_path.exists():
        print(f"⚠️ 디렉토리2가 없습니다: {dir2_path}")
        return
    
    # 디렉토리2의 파일 목록 (파일명만)
    dir2_files = set()
    if dir2_path.exists():
        dir2_files = {f.name for f in dir2_path.iterdir() if f.is_file()}
        print(f"디렉토리2의 파일 개수: {len(dir2_files)}")
    
    # 디렉토리1의 파일 목록
    dir1_files = [f for f in dir1_path.iterdir() if f.is_file()]
    print(f"디렉토리1의 파일 개수: {len(dir1_files)}")
    print()
    
    if not dir2_files:
        print("⚠️ 디렉토리2에 파일이 없습니다.")
        return
    
    # 디렉토리1에서 디렉토리2와 같은 이름의 파일들 찾아서 삭제
    deleted_count = 0
    skipped_count = 0
    
    for file in dir1_files:
        filename = file.name
        
        if filename in dir2_files:
            try:
                file.unlink()
                print(f"✓ 삭제됨: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 삭제 실패: {filename} - {e}")
        else:
            print(f"⚪ 유지됨: {filename}")
            skipped_count += 1
    
    print()
    print("-" * 50)
    print(f"🗑️ 총 {deleted_count}개 파일이 삭제되었습니다.")
    print(f"📁 {skipped_count}개 파일이 유지되었습니다.")

if __name__ == "__main__":
    # 하드코딩된 디렉토리 경로
    directory1 = "C:/Users/USER/Tools/directory_file_deleter/source"      # 디렉토리1 (파일을 삭제할 디렉토리)
    directory2 = "C:/Users/USER/Tools/directory_file_deleter/exclude"     # 디렉토리2 (삭제 기준이 되는 디렉토리)
    
    # 디렉토리 존재 여부 확인
    dir1_path = Path(directory1)
    dir2_path = Path(directory2)
    
    if not dir1_path.exists():
        print(f"디렉토리1이 없습니다: {directory1}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not dir2_path.exists():
        print(f"디렉토리2가 없습니다: {directory2}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 확인 메시지
    print("=" * 60)
    print("🗑️  디렉토리 파일 삭제 도구")
    print("=" * 60)
    print(f"디렉토리1 (삭제 대상): {directory1}")
    print(f"디렉토리2 (삭제 기준): {directory2}")
    print()
    print("📝 동작: 디렉토리1에서 디렉토리2에 있는 같은 이름의 파일들을 삭제")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    delete_matching_files(directory1, directory2) 