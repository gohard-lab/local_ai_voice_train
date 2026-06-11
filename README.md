# 🎙️ 로컬 AI 성우 트레이너 (RVC 데이터셋 전처리 자동화 파일 변환기)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="파이썬 버전">
  <img src="https://img.shields.io/badge/패키지_매니저-uv-FF6F61?style=for-the-badge" alt="패키지 매니저 uv">
  <img src="https://img.shields.io/badge/라이선스-MIT-green?style=for-the-badge" alt="MIT 라이선스">
</div>

---

이 저장소는 로컬 환경에서 RVC(인공지능 목소리 변환) 모델을 학습시킬 때, 비디오나 통파일 오디오를 GPU VRAM 과부하 없이 효율적으로 학습할 수 있도록 **가장 최적의 단위(3~5초)로 음성을 자동 절단하고 변환해 주는 파이썬 자동화 솔루션**을 제공합니다.

## ✨ 핵심 기능
* **무음 기반 자동 슬라이싱:** `pydub` 라이브러리를 활용해 목소리가 잠시 쉬어가는 호흡 구간을 똑똑하게 감지하여 칼같이 잘라냅니다.
* **VRAM 부족 및 OOM 에러 방지:** 조각 파일의 길이를 인공지능이 가장 좋아하는 최적의 규격으로 맞춰, RTX 2060 같은 보급형 그래픽카드에서도 학습 도중 튕기는 현상을 완벽히 방지합니다.
* **현대적인 파이썬 표준 도입:** 구형 `requirements.txt` 대신, 요즘 파이썬 생태계의 표준인 `pyproject.toml`과 초고속 매니저 `uv`를 활용해 의존성을 세련되게 제어합니다.

---

## 🛠️ 프로젝트 세팅 및 설치 방법

본 프로젝트는 최신 파이썬 의존성 표준을 준수합니다. 번거로운 가상환경 관리나 코덱 충돌 없이 `uv` 명령어로 1초 만에 빌드 환경을 구축할 수 있습니다.

### 1. `uv` 설치 (가장 빠른 파키지 매니저)
```bash
# 윈도우 (PowerShell에서 실행)
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

### 2. 프로젝트 의존성 자동 동기화
프로젝트 폴더 경로에서 아래 명령어를 실행하면, pyproject.toml을 분석하여 학습용 오디오 라이브러리(pydub)와 가상환경을 알아서 세팅해 줍니다.

```python
uv sync
```

### 🚀 사용 가이드
데이터셋 슬라이싱 매크로 스크립트
참고: pydub은 음향 파형을 정밀 디코딩하기 위해 시스템에 FFmpeg 코덱 설치가 필요합니다. 환경 변수 등록을 확인해 주세요.

```python
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def slice_audio_for_rvc(source_path, output_dir):
    # 클립챔프 등에서 뽑아낸 무손실 원본 WAV 오디오 파일 로드
    audio = AudioSegment.from_file(source_path, format="wav")
    
    # 0.5초(500ms) 이상 소리가 나지 않고 -40dB 이하인 무음 구간을 절단선으로 지정
    chunks = split_on_silence(
        audio,
        min_silence_len=500,    # 분할을 결정할 최소 무음 길이
        silence_thresh=-40      # 무음으로 판단할 데시벨 기준치
    )
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 5초 내외로 쪼개진 깨끗한 목소리 슬라이스 조각들을 순차적으로 저장
    for i, chunk in enumerate(chunks):
        chunk.export(f"{output_dir}/slice_{i:03d}.wav", format="wav")
        
    print(f"[성공] 총 {len(chunks)}개의 데이터셋 오디오 조각이 '{output_dir}' 방에 생성되었습니다.")

if __name__ == "__main__":
    # 로컬 AI 목소리 학습을 위한 표준 경로 설정
    SOURCE = "assets/audios/raw_source.wav"
    TARGET_DIR = "dataset/voice_slices"
    slice_audio_for_rvc(SOURCE, TARGET_DIR)
```

### 📊 인공지능 학습의 현실 (교과서 이론 vs 실제 현업)
교과서적인 탁상공론: "에포크(Epoch) 복습 횟수를 무작정 높이고 오랫동안 컴퓨터를 돌릴수록 오답률(Loss)이 떨어져 인간과 똑같은 완벽한 목소리가 완성된다."

실제 개발 현업의 현실: 데이터 분량이 10분 내외일 때 300 에포크 이상 과하게 학습시키면 모델이 데이터를 통째로 외워버리는 과적합(Overfitting)이 발생합니다. 후반부 파일은 억양이 딱딱하게 굳거나 쇳소리가 섞이게 되며, 실제 가장 사람 같고 호흡이 자연스러운 리즈 시절의 황금 파일은 140~160 에포크 사이(전체 학습량의 70~80% 지점)에 위치합니다. 데이터의 흐름을 직접 귀로 확인하는 것이 진짜 실력입니다.

### 📢 채널 안내 및 커뮤니티
유튜브 채널: 잡학다식 개발자 PolymathDev_KR - 본 파이프라인의 구축 전 과정과 요리 프로그램 컨셉의 실전 구동 영상을 확인해 보세요!

버그 제보 및 문의: 코드 개선안이나 인퍼런스 에러 관련 제보는 언제든 Issue나 Pull Request를 남겨주시면 솔직 담백하게 답변해 드리겠습니다.

### ⭐ 잊지 말고 Star를 눌러주세요!
이 코드가 대표님의 독점 AI 성우를 구워내는 데 도움을 드렸다면 우측 상단의 Star(⭐) 버튼을 눌러서 마음을 표현해 주세요. 여러분의 작은 성의 하나가 더 유익하고 지적인 파이썬 콘텐츠를 지속해서 만들어 나가는 가장 큰 원동력이 됩니다! 감사합니다.
