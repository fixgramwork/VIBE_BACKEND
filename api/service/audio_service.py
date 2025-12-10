import io
import numpy as np
from scipy.io import wavfile
from scipy import signal
from typing import Tuple, Dict, List
import base64

class AudioService:
    def __init__(self):
        self.categories = {
            "calm": {
                "name": "잔잔",
                "description": "조용하고 편안한 환경입니다. 잔잔한 음악을 추천합니다.",
                "threshold": {"energy": 0.3, "zcr": 0.05}
            },
            "energetic": {
                "name": "활기찬",
                "description": "활기차고 에너지 넘치는 환경입니다. 신나는 음악을 추천합니다.",
                "threshold": {"energy": 0.7, "zcr": 0.15}
            },
            "urban": {
                "name": "도시",
                "description": "도시의 소음이 감지됩니다. 힙합이나 R&B를 추천합니다.",
                "threshold": {"energy": 0.5, "zcr": 0.1}
            },
            "nature": {
                "name": "자연",
                "description": "자연의 소리가 감지됩니다. 어쿠스틱 음악을 추천합니다.",
                "threshold": {"energy": 0.4, "zcr": 0.08}
            },
            "indoor": {
                "name": "실내",
                "description": "실내 환경입니다. 집중할 수 있는 음악을 추천합니다.",
                "threshold": {"energy": 0.2, "zcr": 0.03}
            }
        }

    def analyze_audio_base64(self, audio_base64: str) -> Tuple[str, float]:
        try:
            audio_data = base64.b64decode(audio_base64)

            audio_io = io.BytesIO(audio_data)
            sample_rate, audio_array = wavfile.read(audio_io)

            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)

            audio_array = audio_array.astype(float)
            if np.max(np.abs(audio_array)) > 0:
                audio_array = audio_array / np.max(np.abs(audio_array))

            return self._classify_sound(audio_array, sample_rate)
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return "calm", 0.5

    def _classify_sound(self, audio_array: np.ndarray, sample_rate: int) -> Tuple[str, float]:
        energy = self._calculate_energy(audio_array)
        zcr = self._calculate_zcr(audio_array)
        spectral_centroid = self._calculate_spectral_centroid(audio_array, sample_rate)
        category, confidence = self._determine_category(energy, zcr, spectral_centroid)
        return category, confidence

    def _calculate_energy(self, audio: np.ndarray) -> float:
        return float(np.sqrt(np.mean(audio ** 2)))

    def _calculate_zcr(self, audio: np.ndarray) -> float:
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio)))) / 2
        return float(zero_crossings / len(audio))

    def _calculate_spectral_centroid(self, audio: np.ndarray, sample_rate: int) -> float:
        fft = np.fft.fft(audio)
        magnitude = np.abs(fft[:len(fft)//2])
        freqs = np.fft.fftfreq(len(audio), 1/sample_rate)[:len(fft)//2]
        if np.sum(magnitude) > 0:
            spectral_centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        else:
            spectral_centroid = 0
        return float(spectral_centroid)

    def _determine_category(self, energy: float, zcr: float, spectral_centroid: float) -> Tuple[str, float]:
        scores = {}

        if energy < 0.15:
            scores["indoor"] = 0.8
        elif energy < 0.35:
            scores["calm"] = 0.7
        elif energy < 0.6:
            if zcr < 0.08:
                scores["nature"] = 0.75
            else:
                scores["urban"] = 0.7
        else:
            scores["energetic"] = 0.8

        if zcr > 0.15:
            scores["energetic"] = scores.get("energetic", 0) + 0.1
            scores["urban"] = scores.get("urban", 0) + 0.05
        elif zcr < 0.05:
            scores["calm"] = scores.get("calm", 0) + 0.1
            scores["indoor"] = scores.get("indoor", 0) + 0.05

        if spectral_centroid > 2000:
            scores["energetic"] = scores.get("energetic", 0) + 0.05
        elif spectral_centroid < 1000:
            scores["calm"] = scores.get("calm", 0) + 0.05

        if not scores:
            return "calm", 0.5

        best_category = max(scores.items(), key=lambda x: x[1])
        return best_category[0], min(best_category[1], 1.0)

    def get_category_info(self, category: str) -> Dict:
        return self.categories.get(category, self.categories["calm"])
