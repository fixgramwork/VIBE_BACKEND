from typing import List, Dict
import random
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from api.model.schemas import Track

load_dotenv()

class MusicService:
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            self.client = Anthropic(api_key=api_key)
        else:
            print("Warning: ANTHROPIC_API_KEY not found in environment")
            self.client = None

        self.music_database = {
            "calm": [
                Track(
                    id="calm_1",
                    title="입춘",
                    artist="한로로",
                    album="입춘",
                    coverUrl="/images/hanroro.jpg",
                    audioUrl="/music/한로로-입춘.mp3",
                    duration=372
                ),
                Track(
                    id="calm_2",
                    title="처음 마주쳤을 때처럼",
                    artist="TOIL",
                    album="TOIL 1집",
                    coverUrl="/images/toil.jpg",
                    audioUrl="/music/TOIL-처음마주쳤을때처럼.mp3",
                    duration=245
                ),
                Track(
                    id="calm_3",
                    title="Autumn Leaves",
                    artist="Various Artists",
                    album="Calm Piano",
                    coverUrl="/images/calm-piano.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                    duration=360
                ),
                Track(
                    id="calm_4",
                    title="Peaceful Morning",
                    artist="한로로",
                    album="Peaceful Collection",
                    coverUrl="/images/peaceful.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
                    duration=320
                ),
                Track(
                    id="calm_5",
                    title="Moonlight Sonata",
                    artist="TOIL",
                    album="Classical Moods",
                    coverUrl="/images/moonlight.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
                    duration=295
                ),
                Track(
                    id="calm_6",
                    title="Serenity",
                    artist="Various Artists",
                    album="Meditation Music",
                    coverUrl="/images/serenity.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
                    duration=340
                ),
                Track(
                    id="calm_7",
                    title="Gentle Breeze",
                    artist="한로로",
                    album="Nature Sounds",
                    coverUrl="/images/breeze.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
                    duration=310
                ),
                Track(
                    id="calm_8",
                    title="Starlight",
                    artist="TOIL",
                    album="Night Sky",
                    coverUrl="/images/starlight.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
                    duration=285
                ),
            ],
            "energetic": [
                Track(
                    id="energetic_1",
                    title="에너지 부스트",
                    artist="김하온",
                    album="Energy Vol.1",
                    coverUrl="/images/energy.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                    duration=215
                ),
                Track(
                    id="energetic_2",
                    title="Run Run Run",
                    artist="릴러말즈",
                    album="Run",
                    coverUrl="/images/run.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                    duration=198
                ),
                Track(
                    id="energetic_3",
                    title="Party Time",
                    artist="폴블랑코",
                    album="Party",
                    coverUrl="/images/party.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
                    duration=207
                ),
            ],
            "urban": [
                Track(
                    id="urban_1",
                    title="City Lights",
                    artist="비오",
                    album="Urban Beats",
                    coverUrl="/images/city.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
                    duration=234
                ),
                Track(
                    id="urban_2",
                    title="Seoul Vibes",
                    artist="김하온",
                    album="Seoul",
                    coverUrl="/images/seoul.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
                    duration=256
                ),
                Track(
                    id="urban_3",
                    title="Night Drive",
                    artist="폴블랑코",
                    album="Drive",
                    coverUrl="/images/drive.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
                    duration=289
                ),
            ],
            "nature": [
                Track(
                    id="nature_1",
                    title="Forest Walk",
                    artist="한로로",
                    album="Nature Sounds",
                    coverUrl="/images/forest.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
                    duration=312
                ),
                Track(
                    id="nature_2",
                    title="Ocean Waves",
                    artist="TOIL",
                    album="Seaside",
                    coverUrl="/images/ocean.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
                    duration=278
                ),
                Track(
                    id="nature_3",
                    title="Mountain Breeze",
                    artist="Various Artists",
                    album="Nature Collection",
                    coverUrl="/images/mountain.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
                    duration=301
                ),
            ],
            "indoor": [
                Track(
                    id="indoor_1",
                    title="Study Time",
                    artist="릴러말즈",
                    album="Focus",
                    coverUrl="/images/study.jpg",
                    audioUrl="/music/한로로-입춘.mp3",
                    duration=372
                ),
                Track(
                    id="indoor_2",
                    title="Coffee Shop",
                    artist="TOIL",
                    album="Cafe Vibes",
                    coverUrl="/images/coffee.jpg",
                    audioUrl="/music/TOIL-처음마주쳤을때처럼.mp3",
                    duration=245
                ),
                Track(
                    id="indoor_3",
                    title="Work Mode",
                    artist="Various Artists",
                    album="Productivity",
                    coverUrl="/images/work.jpg",
                    audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
                    duration=267
                ),
            ],
        }

    def get_recommendations_by_category(self, category: str, limit: int = 1) -> List[Track]:
        tracks = self.music_database.get(category, self.music_database["calm"])
        if len(tracks) <= limit:
            return tracks
        return random.sample(tracks, limit)

    def get_recommendations_by_emotion_with_claude(self, emotion: str, emotion_details: Dict) -> Dict:
        if not self.client:
            return self._get_default_recommendation(emotion)

        try:
            emotion_to_category = {
                'happy': 'energetic',
                'sad': 'calm',
                'angry': 'energetic',
                'calm': 'nature',
                'energetic': 'urban',
                'anxious': 'indoor',
            }

            category = emotion_to_category.get(emotion, 'calm')
            recommended_tracks = self.get_recommendations_by_category(category, limit=1)

            prompt = f"""
사용자의 현재 감정 상태: {emotion}
감정 분석 상세 정보:
- 주요 감지된 소리: {', '.join([c['name'] for c in emotion_details.get('top_classes', [])][:3])}

이 감정 상태의 사용자에게 다음 음악들을 추천합니다:
{chr(10).join([f"- {track.title} by {track.artist}" for track in recommended_tracks])}

1. 이 감정 상태에 대한 공감 메시지 (2-3문장, 따뜻하고 친근하게)
2. 왜 이 음악들이 현재 감정에 도움이 되는지 설명 (2-3문장)
3. 음악을 들으면서 할 수 있는 간단한 활동 추천 (1-2문장)

응답은 한국어로 작성해주세요. 각 섹션을 명확히 구분하되, 자연스럽게 연결해주세요.
"""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            recommendation_text = message.content[0].text

            return {
                'emotion': emotion,
                'tracks': recommended_tracks,
                'recommendation_message': recommendation_text,
                'emotion_details': emotion_details
            }

        except Exception as e:
            print(f"Error calling Claude API: {e}")
            import traceback
            traceback.print_exc()
            return self._get_default_recommendation(emotion)

    def _get_default_recommendation(self, emotion: str) -> Dict:
        emotion_to_category = {
            'happy': 'energetic',
            'sad': 'calm',
            'angry': 'calm',
            'calm': 'calm',
            'energetic': 'energetic',
            'anxious': 'calm',
        }

        category = emotion_to_category.get(emotion, 'calm')
        recommended_tracks = self.get_recommendations_by_category(category, limit=1)

        default_messages = {
            'happy': '행복한 기분이시군요! 이 즐거운 순간을 더욱 특별하게 만들어줄 신나는 음악을 추천합니다.',
            'sad': '힘든 시간을 보내고 계시는군요. 이 차분한 음악들이 마음을 위로해줄 거예요.',
            'angry': '감정이 격해져 있으시네요. 이 음악들이 마음을 진정시키는데 도움이 될 거예요.',
            'calm': '평온한 상태시군요. 이 분위기를 유지할 수 있는 음악을 추천합니다.',
            'energetic': '활기찬 에너지가 느껴집니다! 이 기세를 이어갈 음악을 준비했어요.',
            'anxious': '불안하신 것 같네요. 이 음악들이 긴장을 풀어주는데 도움이 될 거예요.',
        }

        return {
            'emotion': emotion,
            'tracks': recommended_tracks,
            'recommendation_message': default_messages.get(emotion, '음악을 추천합니다.'),
            'emotion_details': {}
        }
