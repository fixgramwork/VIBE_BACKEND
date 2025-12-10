# VIBE Music Recommendation API

근처 소리를 분석하여 음악을 추천하는 FastAPI 백엔드 서버입니다.

## 설치 및 실행

### 1. 의존성 설치

```bash
cd fastapi
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버가 http://localhost:8000 에서 실행됩니다.

## API 엔드포인트

### POST /api/analyze-sound
근처 소리를 분석하여 카테고리를 결정하고 음악을 추천합니다.

**Request Body:**
```json
{
  "audioData": "base64_encoded_wav_audio"
}
```

**Response:**
```json
{
  "category": "잔잔",
  "description": "조용하고 편안한 환경입니다. 잔잔한 음악을 추천합니다.",
  "recommendations": [
    {
      "id": "calm_1",
      "title": "입춘",
      "artist": "한로로",
      "album": "입춘",
      "coverUrl": "/images/hanroro.jpg",
      "audioUrl": "/music/한로로-입춘.mp3",
      "duration": 372
    }
  ]
}
```

### GET /api/categories
사용 가능한 카테고리 목록을 반환합니다.

**Response:**
```json
{
  "categories": [
    {
      "id": "calm",
      "name": "잔잔",
      "description": "조용하고 편안한 환경입니다. 잔잔한 음악을 추천합니다."
    }
  ]
}
```

## 음향 분석 카테고리

- **잔잔 (calm)**: 조용하고 편안한 환경
- **활기찬 (energetic)**: 활기차고 에너지 넘치는 환경
- **도시 (urban)**: 도시의 소음
- **자연 (nature)**: 자연의 소리
- **실내 (indoor)**: 실내 환경

## 기술 스택

- FastAPI
- NumPy & SciPy (오디오 분석)
- Pydantic (데이터 검증)
- Uvicorn (ASGI 서버)
