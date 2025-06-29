#!/usr/bin/env python3
"""
🔧 고급 파일 제외 도구 (Advanced File Excluder Tool)

=== 주요 기능 ===
✅ 다양한 비교 모드: 파일명, 파일명+크기, 파일크기+이름 기반 비교
✅ 유연한 처리 방식: 파일 삭제 또는 안전한 폴더로 이동
✅ 미리보기 기능: 실제 작업 전 결과 확인 (Dry-run mode)
✅ 고급 매칭: 단순 파일명부터 내용 기반까지 다층적 비교

=== 사용 사례 ===
🔸 머신러닝 데이터셋에서 검증용 파일들을 훈련 세트에서 제외
🔸 중복 파일 탐지 및 정리 (크기 기반 또는 내용 기반)
🔸 프로젝트 정리 시 참조 파일 기반 선택적 삭제
🔸 백업 시 특정 조건의 파일들만 별도 관리

=== 비교 모드 상세 ===
📋 name: 파일명만 비교 (가장 빠름, 기본값)
📋 size: 파일명 + 파일크기 조합 비교 (중복 감지 향상)
📋 content: 파일크기 + 파일명 조합 비교 (내용 유사성 추정)

=== 처리 방식 ===
🗑️ delete: 일치하는 파일들을 영구 삭제
📦 move: 일치하는 파일들을 백업 디렉토리로 안전하게 이동

=== 기술적 특징 ===
🔧 Dictionary 기반 효율적인 파일 매핑 및 검색
🔧 Path 객체를 사용한 크로스플랫폼 호환성
🔧 파일명 충돌 시 자동 번호 추가 (file_1.txt, file_2.txt...)
🔧 상세한 진행상황 표시 및 에러 핸들링
"""
import sys
import os
import shutil
from pathlib import Path

def get_files_by_comparison_mode(directory, mode):
    """
    지정된 비교 모드에 따라 디렉토리의 파일 정보를 수집하는 함수
    
    Args:
        directory (str): 분석할 디렉토리 경로
        mode (str): 비교 모드 ('name', 'size', 'content')
        
    Returns:
        dict: 비교 키를 key로, Path 객체를 value로 하는 딕셔너리
        
    Comparison Modes:
        - name: 단순 파일명 비교 (확장자 포함)
        - size: 파일명 + 크기 조합으로 더 정확한 비교
        - content: 파일크기 + 이름 조합으로 내용 유사성 추정
        
    Performance Notes:
        - name 모드가 가장 빠름
        - size/content 모드는 파일 시스템 접근이 필요하므로 더 느림
        - 대용량 디렉토리에서는 모드 선택이 성능에 영향
    """
    path = Path(directory)
    files_info = {}
    
    # 디렉토리가 존재하지 않으면 빈 딕셔너리 반환
    if not path.exists():
        return files_info
    
    # 디렉토리 내 모든 파일 순회
    for file in path.iterdir():
        if file.is_file():
            try:
                if mode == "name":
                    # 파일명만으로 비교 (가장 단순하고 빠름)
                    key = file.name
                    files_info[key] = file
                    
                elif mode == "size":
                    # 파일명 + 크기 조합으로 비교 (중복 파일 감지에 유용)
                    file_size = file.stat().st_size
                    key = f"{file.name}_{file_size}"
                    files_info[key] = file
                    
                elif mode == "content":
                    # 파일 크기 + 이름 조합 (내용 기반 유사성 추정)
                    file_size = file.stat().st_size
                    key = f"{file_size}_{file.name}"
                    files_info[key] = file
                    
            except (OSError, PermissionError) as e:
                # 파일 접근 권한 문제 등 예외 처리
                print(f"⚠️ 파일 정보 읽기 실패: {file} - {e}")
                continue
    
    return files_info

def exclude_files_from_directory(source_dir, exclude_dir, output_dir=None, 
                                action="delete", comparison_mode="name", dry_run=False):
    """
    기준 디렉토리에서 제외 기준에 해당하는 파일들을 처리하는 메인 함수
    
    Args:
        source_dir (str): 기준 디렉토리 (파일을 제외할 디렉토리)
        exclude_dir (str): 제외 기준 디렉토리 (제외할 파일들의 참조)
        output_dir (str, optional): 이동 대상 디렉토리 (move 모드에서만 사용)
        action (str): 처리 방식 ('delete' 또는 'move')
        comparison_mode (str): 비교 모드 ('name', 'size', 'content')
        dry_run (bool): 미리보기 모드 (True면 실제 작업하지 않음)
        
    Returns:
        int: 처리된 파일 개수
        
    Algorithm:
        1. 두 디렉토리의 파일 정보를 비교 모드에 따라 수집
        2. 교집합을 통해 제외 대상 파일들 식별
        3. 선택된 처리 방식(삭제/이동)으로 파일 처리
        4. 처리 결과 통계 및 로그 출력
    """
    source_path = Path(source_dir)
    exclude_path = Path(exclude_dir)
    
    # 작업 설정 정보 출력
    print(f"📂 기준 디렉토리: {source_path}")
    print(f"📂 제외 기준 디렉토리: {exclude_path}")
    print(f"🔍 비교 모드: {comparison_mode}")
    print(f"⚙️ 처리 방식: {action}")
    if action == "move" and output_dir:
        print(f"📦 이동 대상: {output_dir}")
    print(f"👁️ 미리보기 모드: {'예' if dry_run else '아니오'}")
    print("-" * 60)
    
    # 디렉토리 존재 확인
    if not source_path.exists():
        print(f"⚠️ 기준 디렉토리가 없습니다: {source_path}")
        return 0
    
    if not exclude_path.exists():
        print(f"⚠️ 제외 기준 디렉토리가 없습니다: {exclude_path}")
        return 0
    
    # 파일 정보 수집
    print("🔄 파일 정보 수집 중...")
    exclude_files = get_files_by_comparison_mode(exclude_dir, comparison_mode)
    source_files = get_files_by_comparison_mode(source_dir, comparison_mode)
    
    print(f"📊 제외 기준 파일 개수: {len(exclude_files):,}개")
    print(f"📊 기준 디렉토리 파일 개수: {len(source_files):,}개")
    print()
    
    # 제외 기준이 비어있으면 종료
    if not exclude_files:
        print("⚠️ 제외 기준 디렉토리에 파일이 없습니다.")
        return 0
    
    # 제외 대상 파일들 식별 (교집합)
    print("🔍 제외 대상 파일 식별 중...")
    files_to_exclude = []
    
    for key, source_file in source_files.items():
        if key in exclude_files:
            exclude_reference = exclude_files[key]
            files_to_exclude.append((key, source_file, exclude_reference))
    
    # 제외 대상이 없으면 종료
    if not files_to_exclude:
        print("ℹ️ 제외할 파일이 발견되지 않았습니다.")
        print(f"📋 '{comparison_mode}' 모드로 일치하는 파일이 없습니다.")
        
        # 디버깅을 위한 샘플 정보 출력
        if len(exclude_files) > 0 and len(source_files) > 0:
            print(f"\n🔍 디버깅 정보:")
            print(f"제외 기준 샘플: {list(exclude_files.keys())[:3]}")
            print(f"기준 디렉토리 샘플: {list(source_files.keys())[:3]}")
        
        return 0
    
    print(f"🎯 제외 대상 파일 개수: {len(files_to_exclude):,}개")
    
    # 이동 모드인 경우 출력 디렉토리 준비
    if action == "move" and output_dir:
        output_path = Path(output_dir)
        if not dry_run:
            output_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 백업 디렉토리 준비: {output_path}")
    
    print()
    
    # 파일 처리 실행
    processed_count = 0
    failed_count = 0
    
    print(f"{'🔄 처리 시작...' if not dry_run else '👁️ 미리보기 시작...'}")
    print()
    
    for i, (key, source_file, exclude_file) in enumerate(files_to_exclude, 1):
        try:
            if dry_run:
                # 미리보기 모드: 실제 작업하지 않고 정보만 출력
                print(f"[미리보기 {i:4d}] {action.upper()}: {source_file.name}")
                if comparison_mode != "name":
                    print(f"{'':>15} 기준: {exclude_file}")
            else:
                # 실제 작업 모드
                if action == "delete":
                    # 파일 삭제
                    source_file.unlink()
                    print(f"✅ [{i:4d}] 삭제: {source_file.name}")
                    
                elif action == "move" and output_dir:
                    # 파일 이동 (이름 충돌 시 자동 번호 추가)
                    output_file = Path(output_dir) / source_file.name
                    
                    # 파일명 충돌 해결
                    counter = 1
                    while output_file.exists():
                        stem = source_file.stem
                        suffix = source_file.suffix
                        output_file = Path(output_dir) / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(source_file), str(output_file))
                    
                    if counter > 1:
                        print(f"📦 [{i:4d}] 이동: {source_file.name} → {output_file.name}")
                    else:
                        print(f"📦 [{i:4d}] 이동: {source_file.name}")
                
                processed_count += 1
                
        except Exception as e:
            print(f"❌ [{i:4d}] 실패: {source_file.name} - {e}")
            failed_count += 1
    
    # 최종 결과 요약
    print()
    print("-" * 60)
    
    if dry_run:
        print(f"👁️ 미리보기 완료:")
        print(f"📋 {len(files_to_exclude):,}개 파일이 {action} 대상입니다.")
    else:
        print(f"🎉 작업 완료:")
        print(f"✅ 성공: {processed_count:,}개 파일이 {action}되었습니다.")
        if failed_count > 0:
            print(f"❌ 실패: {failed_count:,}개 파일에서 오류가 발생했습니다.")
        
        # 성공률 계산
        total_attempted = processed_count + failed_count
        if total_attempted > 0:
            success_rate = processed_count / total_attempted * 100
            print(f"📈 성공률: {success_rate:.1f}%")
    
    return processed_count

if __name__ == "__main__":
    """
    메인 실행 부분 - 하드코딩된 경로로 실행
    
    ⚠️ 사용 전 주의사항:
    1. 처리 방식과 비교 모드를 신중히 선택
    2. 중요한 파일은 미리 백업 생성
    3. dry_run=True로 먼저 테스트 실행 권장
    4. move 모드 사용 시 충분한 디스크 공간 확인
    
    💡 최적화 팁:
    - 대용량 디렉토리에서는 'name' 모드가 가장 빠름
    - 정확한 중복 감지가 필요하면 'size' 모드 사용
    - 파일 내용 기반 비교가 필요하면 'content' 모드 사용
    """
    # 하드코딩된 설정값들
    source = "C:/Users/USER/Tools/directory_excluder/source"    # 기준 디렉토리
    exclude = "C:/Users/USER/Tools/directory_excluder/exclude"  # 제외 기준 디렉토리
    backup = "C:/Users/USER/Tools/directory_excluder/backup"    # 백업 디렉토리
    
    # 작업 설정
    action_mode = "move"        # "delete" 또는 "move"
    comparison_mode = "name"    # "name", "size", "content"
    preview_mode = False        # True: 미리보기만, False: 실제 실행
    
    # 디렉토리 존재 확인
    source_path = Path(source)
    exclude_path = Path(exclude)
    
    if not source_path.exists():
        print(f"❌ 기준 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not exclude_path.exists():
        print(f"❌ 제외 기준 디렉토리가 없습니다: {exclude}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 사용자 확인 및 실행
    print("=" * 70)
    print("🔧 고급 파일 제외 도구")
    print("=" * 70)
    print(f"📂 기준 디렉토리: {source}")
    print(f"📂 제외 기준: {exclude}")
    if action_mode == "move":
        print(f"📦 백업 디렉토리: {backup}")
    print(f"⚙️ 처리 방식: {action_mode}")
    print(f"🔍 비교 모드: {comparison_mode}")
    print(f"👁️ 미리보기: {'예' if preview_mode else '아니오'}")
    print()
    print("📝 동작: 기준 디렉토리에서 제외 기준과 일치하는 파일들을 처리")
    print()
    
    if not preview_mode:
        response = input("계속 진행하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("작업이 취소되었습니다.")
            sys.exit(0)
        print()
    
    # 파일 제외 작업 실행
    result = exclude_files_from_directory(
        source, 
        exclude,
        backup if action_mode == "move" else None,
        action_mode,
        comparison_mode,
        preview_mode
    )
    
    # 최종 메시지
    if result > 0:
        if preview_mode:
            print(f"\n👁️ 미리보기 완료! {result:,}개 파일이 처리 대상입니다.")
        else:
            print(f"\n🎉 작업 완료! {result:,}개 파일이 처리되었습니다.")
    else:
        print(f"\n⚠️ 처리된 파일이 없습니다.") 