#!/usr/bin/env python3
"""
디렉토리 파일 제외 도구
디렉토리1에서 디렉토리2에 있는 파일들을 제외(삭제 또는 이동)하는 도구
"""
import sys
import os
import shutil
from pathlib import Path

def get_files_by_comparison_mode(directory, mode):
    """비교 모드에 따라 파일 정보를 가져옴"""
    path = Path(directory)
    files_info = {}
    
    if not path.exists():
        return files_info
    
    for file in path.iterdir():
        if file.is_file():
            if mode == "name":
                # 파일명으로 비교
                files_info[file.name] = file
            elif mode == "size":
                # 파일명 + 크기로 비교
                key = f"{file.name}_{file.stat().st_size}"
                files_info[key] = file
            elif mode == "content":
                # 파일 내용 해시로 비교 (간단히 크기로 대체)
                key = f"{file.stat().st_size}_{file.name}"
                files_info[key] = file
    
    return files_info

def exclude_files_from_directory(source_dir, exclude_dir, output_dir=None, 
                                action="delete", comparison_mode="name", dry_run=False):
    """
    디렉토리1에서 디렉토리2에 있는 파일들을 제외
    
    Args:
        source_dir: 기준 디렉토리 (파일을 제외할 디렉토리)
        exclude_dir: 제외할 파일들이 있는 디렉토리
        output_dir: 이동할 디렉토리 (action이 "move"일 때만)
        action: "delete" 또는 "move"
        comparison_mode: "name", "size", "content" 중 하나
        dry_run: True이면 실제 작업하지 않고 미리보기만
    """
    source_path = Path(source_dir)
    exclude_path = Path(exclude_dir)
    
    print(f"기준 디렉토리: {source_path}")
    print(f"제외 기준 디렉토리: {exclude_path}")
    print(f"비교 모드: {comparison_mode}")
    print(f"동작: {action}")
    if action == "move" and output_dir:
        print(f"이동 대상: {output_dir}")
    print(f"미리보기 모드: {'예' if dry_run else '아니오'}")
    print("-" * 60)
    
    # 디렉토리 존재 확인
    if not source_path.exists():
        print(f"⚠️ 기준 디렉토리가 없습니다: {source_path}")
        return 0
    
    if not exclude_path.exists():
        print(f"⚠️ 제외 기준 디렉토리가 없습니다: {exclude_path}")
        return 0
    
    # 제외할 파일들의 정보 가져오기
    exclude_files = get_files_by_comparison_mode(exclude_dir, comparison_mode)
    print(f"제외 기준 파일 개수: {len(exclude_files)}")
    
    # 기준 디렉토리의 파일들 확인
    source_files = get_files_by_comparison_mode(source_dir, comparison_mode)
    print(f"기준 디렉토리 파일 개수: {len(source_files)}")
    print()
    
    if not exclude_files:
        print("⚠️ 제외할 파일이 없습니다.")
        return 0
    
    # 제외할 파일들 찾기
    files_to_exclude = []
    for key, source_file in source_files.items():
        if key in exclude_files:
            files_to_exclude.append((key, source_file, exclude_files[key]))
    
    if not files_to_exclude:
        print("⚠️ 제외할 파일이 발견되지 않았습니다.")
        print(f"📋 비교 모드 '{comparison_mode}'로 일치하는 파일이 없습니다.")
        return 0
    
    print(f"🎯 제외할 파일 개수: {len(files_to_exclude)}개")
    print()
    
    # 이동 모드인 경우 출력 디렉토리 생성
    if action == "move" and output_dir:
        output_path = Path(output_dir)
        if not dry_run:
            output_path.mkdir(parents=True, exist_ok=True)
    
    # 파일 처리
    processed_count = 0
    failed_count = 0
    
    for i, (key, source_file, exclude_file) in enumerate(files_to_exclude, 1):
        try:
            if dry_run:
                print(f"[미리보기 {i:3d}] {action}: {source_file.name}")
                if comparison_mode != "name":
                    print(f"              기준: {exclude_file}")
            else:
                if action == "delete":
                    source_file.unlink()
                    print(f"✓ [{i:3d}] 삭제됨: {source_file.name}")
                elif action == "move" and output_dir:
                    output_file = Path(output_dir) / source_file.name
                    # 같은 이름 파일이 있으면 번호 추가
                    counter = 1
                    while output_file.exists():
                        stem = source_file.stem
                        suffix = source_file.suffix
                        output_file = Path(output_dir) / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(source_file), str(output_file))
                    print(f"✓ [{i:3d}] 이동됨: {source_file.name} → {output_file.name}")
                
                processed_count += 1
        except Exception as e:
            print(f"❌ [{i:3d}] 실패: {source_file.name} - {e}")
            failed_count += 1
    
    print()
    print("-" * 60)
    if dry_run:
        print(f"📋 미리보기: {len(files_to_exclude)}개 파일이 {action} 대상입니다.")
    else:
        print(f"✅ 성공: {processed_count}개 파일이 {action}되었습니다.")
        if failed_count > 0:
            print(f"❌ 실패: {failed_count}개 파일에서 오류가 발생했습니다.")
    
    return processed_count



if __name__ == "__main__":
    # 하드코딩된 디렉토리 경로
    source = "C:/Users/USER/Tools/directory_excluder/source"      # 기준 디렉토리 (파일을 제외할 디렉토리)
    exclude = "C:/Users/USER/Tools/directory_excluder/exclude"       # 제외할 파일들이 있는 디렉토리
    backup = "C:/Users/USER/Tools/directory_excluder/backup"  # 이동할 디렉토리 (선택사항)
    
    # 디렉토리 존재 여부 확인
    source_path = Path(source)
    exclude_path = Path(exclude)
    
    if not source_path.exists():
        print(f"기준 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not exclude_path.exists():
        print(f"제외 기준 디렉토리가 없습니다: {exclude}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 확인 메시지
    print("=" * 70)
    print("🗂️  디렉토리 파일 제외 도구")
    print("=" * 70)
    print(f"기준 디렉토리: {source}")
    print(f"제외 기준: {exclude}")
    print(f"백업 디렉토리: {backup}")
    print()
    print("📝 동작: 기준 디렉토리에서 제외 기준 디렉토리에 있는 같은 이름의 파일들을 백업 폴더로 이동")
    print()
    
    response = input("계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("작업이 취소되었습니다.")
        sys.exit(0)
    
    print()
    exclude_files_from_directory(source, exclude, backup, "move", "name", False) 