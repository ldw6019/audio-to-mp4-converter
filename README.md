# 🎵 Minimal Audio to MP4 Converter

오디오 파일(MP3, WAV 등)을 1fps의 초저용량 MP4 영상으로 변환해주는 도구입니다. 
다크 모드 GUI와 오디오 파형(Waveform) 시각화 기능을 지원합니다.

## ✨ 주요 기능
- **초저용량 변환**: 1fps 및 480p 설정으로 비디오 용량 최소화
- **일괄 변환**: 여러 파일을 한꺼번에 드래그 앤 드롭으로 처리
- **시각화**: 오디오 파형 생성 옵션 제공

## 🛠 필수 준비물
이 프로그램은 **FFmpeg** 엔진을 사용합니다.
1. [FFmpeg](https://ffmpeg.org/download.html)를 설치하세요.
2. `ffmpeg.exe`가 환경 변수(Path)에 등록되어 있어야 합니다.

## 🚀 실행 방법
1. 필수 라이브러리 설치:
   `pip install tkinterdnd2`
2. 프로그램 실행:
   `python converter.py`
