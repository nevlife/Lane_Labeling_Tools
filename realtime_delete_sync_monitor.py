#!/usr/bin/env python3
"""
⚡ 실시간 삭제 동기화 모니터 (Realtime Delete Sync Monitor)

=== 주요 기능 ===
✅ 디렉토리1을 실시간 모니터링하여 파일 삭제 이벤트 감지
✅ 삭제된 파일과 같은 이름의 파일을 디렉토리2에서 자동 삭제
✅ 양방향 실시간 동기화: 한쪽에서 삭제하면 다른 쪽에서도 자동 삭제
✅ 백그라운드 상시 실행: Ctrl+C로 종료할 때까지 지속적 모니터링

=== 사용 사례 ===
🔸 이미지 데이터셋과 라벨 데이터셋의 실시간 동기화
🔸 원본 파일과 처리된 파일의 일관성 유지
🔸 프로젝트 파일과 백업 파일의 자동 동기화
🔸 멀티 디렉토리 환경에서의 파일 일관성 관리

=== 동기화 시나리오 ===
📂 모니터링 대상: /dataset/annotations/
📂 동기화 대상: /dataset/images/
📝 이벤트: annotations/file001.txt 삭제
⚡ 자동 반응: images/file001.jpg 자동 삭제

=== 기술적 특징 ===
🔧 Watchdog 라이브러리를 사용한 실시간 파일 시스템 이벤트 감지
🔧 이벤트 기반 비동기 처리로 시스템 리소스 효율성
🔧 파일명 매칭을 통한 유연한 확장자 대응
🔧 예외 처리로 안정적인 장시간 실행

⚠️ 필수 의존성: pip install watchdog
"""
import sys
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SyncDeleteHandler(FileSystemEventHandler):
    """
    파일 삭제 이벤트를 처리하는 이벤트 핸들러 클래스
    
    Watchdog의 FileSystemEventHandler를 상속받아 파일 삭제 이벤트만 처리
    """
    
    def __init__(self, source_dir, target_dir):
        """
        핸들러 초기화
        
        Args:
            source_dir (str): 모니터링할 디렉토리 (삭제 이벤트를 감지할 곳)
            target_dir (str): 동기화 대상 디렉토리 (연동 삭제를 수행할 곳)
        """
        super().__init__()
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        
        print(f"📡 모니터링 대상: {self.source_dir}")
        print(f"🎯 동기화 대상: {self.target_dir}")
        print(f"🔗 파일 삭제 동기화가 활성화되었습니다.")
        
    def on_deleted(self, event):
        """
        파일 삭제 이벤트 발생 시 호출되는 메서드
        
        Args:
            event: Watchdog 이벤트 객체 (src_path, is_directory 등 포함)
            
        Processing Flow:
            1. 디렉토리 삭제 이벤트는 무시
            2. 삭제된 파일의 이름 추출
            3. 동기화 대상에서 같은 이름의 파일 검색
            4. 발견되면 자동 삭제, 없으면 로그 출력
        """
        # 디렉토리 삭제는 처리하지 않음 (파일만 처리)
        if event.is_directory:
            return
            
        # 삭제된 파일의 경로 및 이름 추출
        deleted_file_path = Path(event.src_path)
        deleted_filename = deleted_file_path.name
        
        print(f"\n🔍 삭제 감지: {deleted_filename}")
        print(f"   경로: {deleted_file_path}")
        
        # 동기화 대상 디렉토리에서 같은 이름의 파일 찾기
        target_file = self.target_dir / deleted_filename
        
        if target_file.exists():
            try:
                # 동기화 대상에서 파일 삭제
                target_file.unlink()
                print(f"✅ 동기화 삭제 완료: {target_file}")
                print(f"   🔗 {self.source_dir.name} → {self.target_dir.name}")
            except Exception as e:
                print(f"❌ 동기화 삭제 실패: {target_file}")
                print(f"   오류: {e}")
        else:
            print(f"ℹ️ 대상 파일 없음: {target_file}")
            print(f"   (동기화할 파일이 없어 작업 생략)")
        
        print("-" * 40)

def monitor_directory(source_dir, target_dir):
    """
    디렉토리 모니터링을 시작하고 실시간 동기화를 수행하는 메인 함수
    
    Args:
        source_dir (str): 모니터링할 디렉토리 경로
        target_dir (str): 동기화 대상 디렉토리 경로
        
    Features:
        - 24시간 상시 모니터링 가능
        - Ctrl+C로 안전한 종료
        - 멀티스레드 이벤트 처리
        - 시스템 리소스 최적화
        
    Technical Notes:
        - Observer 패턴으로 이벤트 기반 처리
        - recursive=False로 하위 디렉토리는 모니터링하지 않음
        - 1초 간격으로 상태 체크 (CPU 사용량 최소화)
    """
    # 이벤트 핸들러 및 옵저버 설정
    event_handler = SyncDeleteHandler(source_dir, target_dir)
    observer = Observer()
    
    # 모니터링 디렉토리 등록 (하위 디렉토리 제외)
    observer.schedule(event_handler, source_dir, recursive=False)
    
    # 모니터링 시작
    observer.start()
    
    print(f"\n📡 실시간 디렉토리 모니터링 시작...")
    print(f"⏰ 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🛑 종료: Ctrl+C를 눌러주세요")
    print("=" * 50)
    
    try:
        # 무한 루프로 모니터링 유지
        while True:
            time.sleep(1)  # 1초마다 체크 (CPU 효율성)
    except KeyboardInterrupt:
        # Ctrl+C 입력 시 안전한 종료
        print(f"\n⏹️ 모니터링 종료 요청 감지")
        print(f"⏰ 종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        observer.stop()
        print("🔄 관찰자 정리 중...")
    
    # 옵저버 스레드 종료 대기
    observer.join()
    print("✅ 모니터링이 안전하게 종료되었습니다.")

if __name__ == "__main__":
    """
    메인 실행 부분 - 하드코딩된 경로로 실행
    
    ⚠️ 실행 전 확인사항:
    1. watchdog 라이브러리 설치: pip install watchdog
    2. 모니터링 대상 디렉토리가 존재하는지 확인
    3. 동기화 대상 디렉토리가 존재하는지 확인
    4. 파일 삭제 권한이 있는지 확인
    
    💡 사용 팁:
    - 터미널을 항상 열어두고 백그라운드에서 실행
    - 로그를 파일로 저장하려면 출력 리디렉션 사용
    - 여러 디렉토리 쌍을 모니터링하려면 다중 인스턴스 실행
    
    🔧 커스터마이징:
    - recursive=True로 변경하면 하위 디렉토리도 모니터링
    - 다른 이벤트(생성, 수정)도 처리하려면 핸들러 확장
    """
    # 하드코딩된 디렉토리 경로들
    source = "C:/Users/USER/Documents/dataset/ll_seg_annotations/train"  # 모니터링 대상
    target = "C:/Users/USER/Documents/dataset/image/train"               # 동기화 대상
    
    print("=" * 70)
    print("⚡ 실시간 삭제 동기화 모니터")
    print("=" * 70)
    print(f"📡 모니터링: {source}")
    print(f"🎯 동기화: {target}")
    print()
    print("📝 동작: 모니터링 디렉토리에서 파일 삭제 시 동기화 디렉토리에서도 같은 파일 자동 삭제")
    print()
    
    # 필수 의존성 확인
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ watchdog 라이브러리가 설치되지 않았습니다.")
        print("💡 설치 명령어: pip install watchdog")
        sys.exit(1)
    
    # 디렉토리 존재 여부 확인
    source_path = Path(source)
    target_path = Path(target)
    
    if not source_path.exists():
        print(f"❌ 모니터링 디렉토리가 없습니다: {source}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
        
    if not target_path.exists():
        print(f"❌ 동기화 디렉토리가 없습니다: {target}")
        print("디렉토리를 생성하거나 경로를 확인해주세요.")
        sys.exit(1)
    
    # 사용자 확인 (모니터링은 장시간 실행되므로 신중하게)
    print("⚠️ 주의: 이 도구는 실시간으로 파일을 삭제합니다!")
    print("🔄 모니터링이 시작되면 Ctrl+C로만 종료할 수 있습니다.")
    print()
    
    response = input("실시간 모니터링을 시작하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("모니터링이 취소되었습니다.")
        sys.exit(0)
    
    # 모니터링 시작
    monitor_directory(source, target) 