import io
import numpy as np
import ssl
import os
import urllib.request
import tensorflow as tf
import tensorflow_hub as hub
from scipy.io import wavfile
import base64
import resampy
from typing import Tuple, Dict

_original_urlopen = urllib.request.urlopen

def _patched_urlopen(url, data=None, timeout=None, **kwargs):
    kwargs['context'] = ssl._create_unverified_context()
    return _original_urlopen(url, data, timeout, **kwargs)

urllib.request.urlopen = _patched_urlopen
ssl._create_default_https_context = ssl._create_unverified_context

class EmotionService:
    def __init__(self):
        self.model = None
        self.class_names = None

        self.emotion_mapping = {

            'Music': 'happy',
            'Laughter': 'happy',
            'Giggle': 'happy',
            'Chuckle, chortle': 'happy',
            'Belly laugh': 'happy',
            'Cheer': 'happy',
            'Applause': 'happy',
            'Musical instrument': 'happy',

            'Crying, sobbing': 'sad',
            'Whimper': 'sad',
            'Wail, moan': 'sad',
            'Sigh': 'sad',

            'Screaming': 'angry',
            'Shout': 'angry',
            'Yell': 'angry',
            'Battle cry': 'angry',
            'Crowd': 'angry',

            'Silence': 'calm',
            'White noise': 'calm',
            'Pink noise': 'calm',
            'Rain': 'calm',
            'Raindrop': 'calm',
            'Rain on surface': 'calm',
            'Stream': 'calm',
            'Wind': 'calm',
            'Rustle': 'calm',
            'Ocean': 'calm',
            'Waves, surf': 'calm',
            'Water': 'calm',
            'Waterfall': 'calm',
            'Pour': 'calm',
            'Trickle, dribble': 'calm',
            'Gurgling': 'calm',
            'Slosh': 'calm',
            'Splash, splatter': 'calm',
            'Fill (with liquid)': 'calm',
            'Drip': 'calm',
            'Liquid': 'calm',

            'Speech': 'energetic',
            'Conversation': 'energetic',
            'Inside, small room': 'energetic',
            'Inside, large room or hall': 'energetic',
            'Inside, public space': 'energetic',
            'Clapping': 'energetic',
            'Traffic noise, roadway noise': 'energetic',
            'Vehicle': 'energetic',
            'Car': 'energetic',
            'Bus': 'energetic',
            'Truck': 'energetic',

            'Alarm': 'anxious',
            'Siren': 'anxious',
            'Emergency vehicle': 'anxious',
            'Fire alarm': 'anxious',
            'Smoke alarm': 'anxious',
            'Doorbell': 'anxious',
            'Knock': 'anxious',
        }

        self.emotion_descriptions = {
            'happy': '행복하고 즐거운 기분입니다',
            'sad': '슬프거나 우울한 기분입니다',
            'angry': '화나거나 짜증난 상태입니다',
            'calm': '차분하고 평온한 상태입니다',
            'energetic': '활기차고 에너지 넘치는 상태입니다',
            'anxious': '불안하거나 긴장된 상태입니다',
        }

    def _ensure_model_loaded(self):
        if self.model is None:
            print("Loading YAMNet model...")
            self.model = hub.load('https://tfhub.dev/google/yamnet/1')
            self.class_names = self._load_class_names()
            print("YAMNet model loaded successfully!")

    def _load_class_names(self):
        class_map_path = self.model.class_map_path().numpy()
        class_names = []

        with tf.io.gfile.GFile(class_map_path) as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    class_names.append(parts[2])

        return class_names

    def analyze_emotion_from_base64(self, audio_base64: str) -> Tuple[str, float, Dict]:
        self._ensure_model_loaded()

        try:
            audio_data = base64.b64decode(audio_base64)

            audio_io = io.BytesIO(audio_data)
            sample_rate, audio_array = wavfile.read(audio_io)

            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)

            audio_array = audio_array.astype(np.float32)
            if np.max(np.abs(audio_array)) > 0:
                audio_array = audio_array / np.max(np.abs(audio_array))

            if sample_rate != 16000:
                audio_array = resampy.resample(audio_array, sample_rate, 16000)

            scores, embeddings, spectrogram = self.model(audio_array)

            class_scores = tf.reduce_mean(scores, axis=0)
            top_class_indices = tf.argsort(class_scores, direction='DESCENDING')[:10]

            emotion_scores = self._calculate_emotion_scores(class_scores, top_class_indices)

            if emotion_scores:
                best_emotion = max(emotion_scores.items(), key=lambda x: x[1])
                emotion = best_emotion[0]
                confidence = float(best_emotion[1])
            else:
                emotion = 'calm'
                confidence = 0.5

            details = {
                'top_classes': [
                    {
                        'name': self.class_names[i.numpy()],
                        'score': float(class_scores[i].numpy())
                    }
                    for i in top_class_indices[:5]
                ],
                'all_emotion_scores': emotion_scores
            }

            return emotion, confidence, details

        except Exception as e:
            print(f"Error in emotion analysis: {e}")
            import traceback
            traceback.print_exc()
            return 'calm', 0.5, {'error': str(e)}

    def _calculate_emotion_scores(self, class_scores, top_class_indices) -> Dict[str, float]:
        emotion_scores = {
            'happy': 0.0,
            'sad': 0.0,
            'angry': 0.0,
            'calm': 0.0,
            'energetic': 0.0,
            'anxious': 0.0,
        }

        for idx in top_class_indices:
            class_name = self.class_names[idx.numpy()]
            score = float(class_scores[idx].numpy())

            if class_name in self.emotion_mapping:
                emotion = self.emotion_mapping[class_name]
                emotion_scores[emotion] += score

        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v / total for k, v in emotion_scores.items()}

        return emotion_scores

    def get_emotion_description(self, emotion: str) -> str:
        return self.emotion_descriptions.get(emotion, '알 수 없는 감정 상태입니다')
