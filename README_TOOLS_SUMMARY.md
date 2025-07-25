# 🛠️ 파일 관리 도구 모음 (File Management Tools Collection)

`C:\Users\USER\Tools` 디렉토리에 있는 모든 파일 관리 도구들의 기능별 정리 및 권장 파일명입니다.

## 📋 도구 목록 및 권장 파일명

### 1. 🎯 Frame 중복 파일 복사 도구

**권장 파일명**: `frame_overlap_copy_tool.py`
**기존 파일명**: `copy_matching_frame_numbers/copy_matching_frame_numbers.py`

#### 주요 기능

-   Source 디렉토리와 Train 디렉토리에서 같은 frame 번호를 가진 파일들을 찾아서 복사
-   정규식을 사용한 frame 번호 추출 (frame_XXXXXX 패턴)
-   중복된 frame 번호를 가진 Train 파일들만 Output 디렉토리로 선택적 복사

#### 사용 사례

-   머신러닝 데이터셋에서 특정 frame들만 필터링
-   비디오 프레임 데이터에서 중복 프레임 별도 관리
-   대용량 이미지 데이터셋에서 조건부 파일 추출

---

### 2. 📊 데이터셋 5분할 도구

**권장 파일명**: `dataset_split_every_fifth.py`
**기존 파일명**: `dataset_splitter_5th/dataset_splitter_5th.py`

#### 주요 기능

-   정렬된 파일 목록에서 5번째마다 파일을 선택하여 다른 디렉토리로 이동
-   인덱스 기반 순차적 분할 (5, 10, 15, 20... 번째 파일 선택)
-   파일명 순서대로 정렬하여 일관된 분할 결과 보장

#### 사용 사례

-   머신러닝 데이터셋을 Train/Validation으로 분할 (20% 추출)
-   대용량 데이터셋에서 샘플링을 통한 부분집합 생성
-   시계열 데이터에서 주기적 샘플링

---

### 3. 🗂️ 디렉토리 동기화 정리 도구

**권장 파일명**: `directory_sync_cleanup.py`
**기존 파일명**: `dir_sync_cleanup/dir_sync_cleanup.py`

#### 주요 기능

-   기준 디렉토리를 참조하여 정리 대상 디렉토리에서 불필요한 파일들을 삭제
-   파일명 기반 비교로 기준 디렉토리에 없는 파일들을 자동 식별
-   일방향 동기화로 파일 목록 일치화

#### 사용 사례

-   머신러닝 데이터셋의 Label과 Image 파일 동기화
-   백업 디렉토리와 원본 디렉토리의 파일 목록 일치화
-   데이터 전처리 후 매칭되지 않는 파일들 정리

---

### 4. ⚡ 실시간 삭제 동기화 모니터

**권장 파일명**: `realtime_delete_sync_monitor.py`
**기존 파일명**: `realtime_sync_deleter/realtime_sync_deleter.py`

#### 주요 기능

-   디렉토리1을 실시간 모니터링하여 파일 삭제 이벤트 감지
-   삭제된 파일과 같은 이름의 파일을 디렉토리2에서 자동 삭제
-   Watchdog 라이브러리를 사용한 백그라운드 상시 실행

#### 사용 사례

-   이미지 데이터셋과 라벨 데이터셋의 실시간 동기화
-   원본 파일과 처리된 파일의 일관성 유지
-   멀티 디렉토리 환경에서의 파일 일관성 관리

#### 필수 의존성

```bash
pip install watchdog
```

---

### 5. 🔧 고급 파일 제외 도구

**권장 파일명**: `advanced_file_excluder.py`
**기존 파일명**: `directory_excluder/directory_excluder.py`

#### 주요 기능

-   다양한 비교 모드: 파일명, 파일명+크기, 파일크기+이름 기반 비교
-   유연한 처리 방식: 파일 삭제 또는 안전한 폴더로 이동
-   미리보기 기능으로 실제 작업 전 결과 확인

#### 사용 사례

-   머신러닝 데이터셋에서 검증용 파일들을 훈련 세트에서 제외
-   중복 파일 탐지 및 정리 (크기 기반 또는 내용 기반)
-   프로젝트 정리 시 참조 파일 기반 선택적 삭제

---

## 🔧 기술적 특징 요약

### 공통 기술 스택

-   **Python 3.6+** 기반
-   **pathlib.Path** 객체를 사용한 크로스플랫폼 호환성
-   **예외 처리** 및 **상세한 로그**로 안정성 보장
-   **하드코딩된 경로**로 즉시 실행 가능

### 성능 최적화

-   **Set/Dictionary** 자료구조를 활용한 효율적인 파일 비교
-   **정규식 패턴 매칭**으로 빠른 문자열 처리
-   **배치 처리** 방식으로 대용량 파일 처리 지원

### 안전성 기능

-   **파일 존재 여부 확인** 및 **디렉토리 자동 생성**
-   **파일명 충돌 해결** (자동 번호 추가)
-   **사용자 확인 프롬프트**로 실수 방지

## 📁 권장 디렉토리 구조

```
C:/Users/USER/Tools/
├── frame_overlap_copy_tool.py          # Frame 중복 파일 복사
├── dataset_split_every_fifth.py        # 데이터셋 5분할
├── directory_sync_cleanup.py           # 디렉토리 동기화 정리
├── realtime_delete_sync_monitor.py     # 실시간 삭제 동기화
├── advanced_file_excluder.py           # 고급 파일 제외
└── README_TOOLS_SUMMARY.md             # 이 문서
```

## 🚀 사용 가이드

### 1. 일반적인 실행 방법

```bash
cd C:/Users/USER/Tools
python 도구파일명.py
```

### 2. 실행 전 체크리스트

-   [ ] 디렉토리 경로가 올바른지 확인
-   [ ] 필요한 경우 백업 생성
-   [ ] 미리보기 모드로 먼저 테스트 (지원되는 도구의 경우)
-   [ ] 파일 접근 권한 확인

### 3. 도구별 특별 요구사항

-   **실시간 모니터**: `pip install watchdog` 필요
-   **대용량 처리**: 충분한 디스크 공간 확보
-   **네트워크 드라이브**: 로컬 디스크 사용 권장

## ⚠️ 중요 안전 주의사항

1. **백업 필수**: 중요한 데이터는 작업 전 반드시 백업
2. **테스트 실행**: 소량의 테스트 데이터로 먼저 검증
3. **경로 확인**: 하드코딩된 경로를 실제 환경에 맞게 수정
4. **권한 문제**: 관리자 권한이 필요할 수 있음
5. **복구 불가**: 삭제 작업은 되돌릴 수 없으므로 신중히 진행

## 💡 활용 팁

### 데이터 과학 프로젝트에서

-   **1번 도구**: 특정 조건의 이미지만 추출
-   **2번 도구**: Train/Val/Test 데이터셋 분할
-   **3번 도구**: 라벨과 이미지 파일 동기화
-   **4번 도구**: 실시간 데이터 정합성 유지
-   **5번 도구**: 복잡한 조건의 파일 필터링

### 일반 파일 관리에서

-   중복 파일 정리
-   백업 디렉토리 관리
-   프로젝트 파일 구조화
-   자동화된 파일 동기화

---

_이 도구들은 파일 관리 작업을 자동화하고 효율성을 높이기 위해 설계되었습니다. 각 도구의 특성을 이해하고 적절한 상황에서 활용하시기 바랍니다._
