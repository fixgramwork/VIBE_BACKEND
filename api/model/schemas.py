from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AudioAnalysisResponse(BaseModel):
    category: str
    confidence: float
    description: str

class Track(BaseModel):
    id: str
    title: str
    artist: str
    album: str
    coverUrl: str
    audioUrl: str
    duration: int

class MusicRecommendationResponse(BaseModel):
    category: str
    description: str
    recommendations: List[Track]

class EmotionAnalysisResponse(BaseModel):
    emotion: str
    confidence: float
    description: str
    details: Dict[str, Any]

class EmotionMusicRecommendationResponse(BaseModel):
    emotion: str
    confidence: float
    emotion_description: str
    recommendation_message: str
    recommendations: List[Track]
    emotion_details: Optional[Dict[str, Any]] = None
