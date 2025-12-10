from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.model.schemas import EmotionMusicRecommendationResponse
from api.service.music_service import MusicService
from api.service.emotion_service import EmotionService

router = APIRouter()
music_service = MusicService()
emotion_service = EmotionService()

class AudioAnalysisRequest(BaseModel):
    audioData: str

@router.post("/analyze-emotion", response_model=EmotionMusicRecommendationResponse)
async def analyze_emotion(request: AudioAnalysisRequest):
    try:
        print("[Step 1] YAMNet으로 감정 분석 중...")
        emotion, confidence, emotion_details = emotion_service.analyze_emotion_from_base64(request.audioData)

        print(f"[감정 분석 완료] 감정: {emotion}, 신뢰도: {confidence:.2f}")
        print(f"[감지된 소리] {', '.join([c['name'] for c in emotion_details.get('top_classes', [])][:3])}")

        print("[Step 2] Claude API로 음악 추천 중...")
        recommendation_result = music_service.get_recommendations_by_emotion_with_claude(
            emotion,
            emotion_details
        )

        print(f"[추천 완료] {len(recommendation_result['tracks'])}개의 음악 추천")
        print(f"[추천 메시지 미리보기] {recommendation_result['recommendation_message'][:100]}...")

        return EmotionMusicRecommendationResponse(
            emotion=emotion,
            confidence=confidence,
            emotion_description=emotion_service.get_emotion_description(emotion),
            recommendation_message=recommendation_result['recommendation_message'],
            recommendations=recommendation_result['tracks'],
            emotion_details=emotion_details
        )

    except Exception as e:
        print(f"Error in analyze_emotion: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emotions")
async def get_emotions():
    return {
        "emotions": [
            {"id": emotion_id, "description": description}
            for emotion_id, description in emotion_service.emotion_descriptions.items()
        ]
    }
