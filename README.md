1. **현재 환경의 패키지 목록 확인 및 저장**
    
    터미널에서 프로젝트 디렉토리로 이동한 후, 다음 명령어를 실행하세요:
    
    ```bash
    pip freeze > requirements.txt
    
    ```
    
    - `pip freeze`: 현재 Python 환경에 설치된 모든 패키지와 버전을 출력합니다.
    - `> requirements.txt`: 출력 결과를 `requirements.txt` 파일로 저장합니다.
2. **결과 확인**
    
    실행 후 `requirements.txt` 파일이 생성되며, 내용은 아래와 비슷할 겁니다:
    
    ```
    numpy==1.21.0
    pandas==1.3.5
    requests==2.28.1
    
    ```
    
    각 줄은 `패키지명==버전` 형식으로 기록됩니다.
    
3. **다른 환경에서 설치하기**
    
    이 파일을 사용해 다른 환경에 동일한 패키지를 설치하려면:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    

### 추가 팁

- **수동 편집**: 필요하면 `requirements.txt`를 열어 불필요한 패키지를 삭제하거나 버전을 수정할 수 있습니다.
- **가상환경 사용 권장**: 프로젝트별로 독립적인 환경을 유지하려면 `venv`나 `virtualenv`를 사용하는 게 좋습니다.
    - 가상환경 생성: `python -m venv venv`
    - 활성화: Windows(`venv\\Scripts\\activate`), macOS/Linux(`source venv/bin/activate`)