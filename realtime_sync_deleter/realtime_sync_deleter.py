#!/usr/bin/env python3
"""
디렉토리 동기화 삭제 도구
디렉토리1에서 파일을 삭제하면 디렉토리2에서도 같은 이름의 파일을 자동 삭제
"""
import sys
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SyncDeleteHandler(FileSystemEventHandler):
    def __init__(self, source_dir, target_dir):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        print(f"모니터링: {self.source_dir}")
        print(f"동기화 대상: {self.target_dir}")
        
    def on_deleted(self, event):
        if event.is_directory:
            return
            
        # 삭제된 파일명 추출
        deleted_file = Path(event.src_path)
        filename = deleted_file.name
        
        # 대상 디렉토리에서 같은 이름의 파일 삭제
        target_file = self.target_dir / filename
        
        if target_file.exists():
            try:
                target_file.unlink()
                print(f"✓ 동기화 삭제: {target_file}")
            except Exception as e:
                print(f"❌ 삭제 실패: {target_file} - {e}")
        else:
            print(f"⚠ 대상 파일 없음: {target_file}")

def monitor_directory(source_dir, target_dir):
    """디렉토리 모니터링 시작"""
    event_handler = SyncDeleteHandler(source_dir, target_dir)
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    
    observer.start()
    print(f"\n📁 디렉토리 모니터링 시작...")
    print(f"Ctrl+C로 종료하세요.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n모니터링 종료")
    
    observer.join()

if __name__ == "__main__":
    # 하드코딩된 디렉토리 경로
    source = "C:/Users/USER/Documents/dataset/ll_seg_annotations/train"
    target = "C:/Users/USER/Documents/dataset/image/train"
    
    # 디렉토리 존재 여부 확인 및 생성
    source_path = Path(source)
    target_path = Path(target)
    
    if not source_path.exists():
        print(f"기준 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not target_path.exists():
        print(f"동기화 디렉토리가 없습니다: {target}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    monitor_directory(source, target)