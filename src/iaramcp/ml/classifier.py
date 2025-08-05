"""
Instrument classification module using machine learning and heuristic analysis.
"""

import asyncio
import numpy as np
import librosa
from typing import Dict, List, Optional, Tuple, Any
import logging
from pathlib import Path

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

class InstrumentClassifier:
    """
    Advanced instrument classification using both heuristic and ML approaches.
    """
    
    # Instrument categories as specified in project requirements
    INSTRUMENTS = [
        'vocals', 'drums', 'bass', 'guitar', 'piano', 
        'strings', 'brass', 'woodwinds', 'synth', 'other'
    ]
    
    # Sub-categories for more precise detection
    INSTRUMENT_SUBCATEGORIES = {
        'vocals': ['lead_vocals', 'backing_vocals', 'rap_vocals', 'choir'],
        'drums': ['acoustic_drums', 'electronic_drums', 'trap_kit', 'latin_percussion'],
        'bass': ['electric_bass', 'acoustic_bass', '808_bass', 'synth_bass'],
        'guitar': ['electric_guitar', 'acoustic_guitar', 'distorted_guitar', 'clean_guitar'],
        'piano': ['acoustic_piano', 'electric_piano', 'digital_piano'],
        'strings': ['violin', 'cello', 'orchestral_strings', 'synthesized_strings'],
        'brass': ['trumpet', 'trombone', 'french_horn', 'synthesized_brass'],
        'woodwinds': ['flute', 'clarinet', 'saxophone', 'synthesized_woodwinds'],
        'synth': ['lead_synth', 'pad_synth', 'bass_synth', 'arp_synth'],
        'other': ['unknown', 'mixed', 'ambient', 'effects']
    }
    
    def __init__(self):
        """Initialize the instrument classifier."""
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42) if SKLEARN_AVAILABLE else None
        self._is_trained = False
        
    async def identify_instruments(
        self, 
        file_path: str, 
        use_separation: bool = True,
        confidence_threshold: float = 0.7,
        method: str = "heuristic"
    ) -> Dict[str, Any]:
        """
        Identify instruments in an audio file.
        
        Args:
            file_path: Path to audio file
            use_separation: Whether to use separated stems for better accuracy
            confidence_threshold: Minimum confidence for instrument detection
            method: Detection method ('heuristic', 'ml', 'hybrid')
            
        Returns:
            Dictionary with detected instruments and confidence scores
        """
        try:
            if not Path(file_path).exists():
                return {"error": f"File not found: {file_path}"}
            
            results = {
                "file_path": file_path,
                "method": method,
                "confidence_threshold": confidence_threshold,
                "detected_instruments": [],
                "instrument_analysis": {},
                "overall_confidence": 0.0
            }
            
            if use_separation:
                # Use stem-based analysis for higher accuracy
                results = await self._analyze_with_separation(file_path, confidence_threshold, method)
            else:
                # Analyze full mix
                results = await self._analyze_full_mix(file_path, confidence_threshold, method)
            
            return results
            
        except Exception as e:
            import traceback
            return {
                "error": f"Instrument identification failed: {str(e)}",
                "traceback": traceback.format_exc()
            }
    
    async def _analyze_with_separation(
        self, 
        file_path: str, 
        confidence_threshold: float,
        method: str
    ) -> Dict[str, Any]:
        """Analyze instruments using separated stems."""
        # This would integrate with the separation module
        # For now, implement basic analysis
        return await self._analyze_full_mix(file_path, confidence_threshold, method)
    
    async def _analyze_full_mix(
        self, 
        file_path: str, 
        confidence_threshold: float,
        method: str
    ) -> Dict[str, Any]:
        """Analyze instruments in the full mix."""
        try:
            # Load audio
            y, sr = librosa.load(file_path, sr=22050)
            
            # Extract comprehensive features
            features = await self._extract_instrument_features(y, sr)
            
            # Apply detection method
            if method == "heuristic":
                detections = await self._heuristic_detection(features, confidence_threshold)
            elif method == "ml" and SKLEARN_AVAILABLE and self._is_trained:
                detections = await self._ml_detection(features, confidence_threshold)
            else:
                # Fallback to heuristic
                detections = await self._heuristic_detection(features, confidence_threshold)
            
            # Calculate overall confidence
            confidences = [d["confidence"] for d in detections]
            overall_confidence = np.mean(confidences) if confidences else 0.0
            
            return {
                "file_path": file_path,
                "method": method,
                "confidence_threshold": confidence_threshold,
                "detected_instruments": detections,
                "instrument_analysis": features,
                "overall_confidence": float(overall_confidence),
                "ml_available": SKLEARN_AVAILABLE,
                "model_trained": self._is_trained
            }
            
        except Exception as e:
            import traceback
            return {
                "error": f"Full mix analysis failed: {str(e)}",
                "traceback": traceback.format_exc()
            }
    
    async def _extract_instrument_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Extract features relevant for instrument classification."""
        try:
            # Allow other tasks to run
            await asyncio.sleep(0.001)
            
            features = {}
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            features["spectral"] = {
                "centroid_mean": float(np.mean(spectral_centroids)),
                "centroid_std": float(np.std(spectral_centroids)),
                "bandwidth_mean": float(np.mean(spectral_bandwidth)),
                "rolloff_mean": float(np.mean(spectral_rolloff))
            }
            
            # MFCC features (important for instrument timbre)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features["mfcc"] = {
                "mean": [float(x) for x in np.mean(mfccs, axis=1)],
                "std": [float(x) for x in np.std(mfccs, axis=1)]
            }
            
            # Chroma features (harmonic content)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            features["chroma"] = {
                "mean": [float(x) for x in np.mean(chroma, axis=1)],
                "std": [float(x) for x in np.std(chroma, axis=1)]
            }
            
            # Tempo and rhythm
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            features["rhythm"] = {
                "tempo": float(tempo),
                "beat_count": len(beats)
            }
            
            # Zero crossing rate (useful for distinguishing percussive vs harmonic)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            features["zcr"] = {
                "mean": float(np.mean(zcr)),
                "std": float(np.std(zcr))
            }
            
            # RMS energy
            rms = librosa.feature.rms(y=y)[0]
            features["energy"] = {
                "rms_mean": float(np.mean(rms)),
                "rms_std": float(np.std(rms)),
                "dynamic_range": float(np.max(rms) - np.min(rms))
            }
            
            # Frequency band analysis
            stft = librosa.stft(y)
            magnitude = np.abs(stft)
            freqs = librosa.fft_frequencies(sr=sr)
            
            # Define frequency bands for different instruments
            bass_band = np.mean(magnitude[(freqs >= 20) & (freqs <= 200)], axis=0)
            low_mid_band = np.mean(magnitude[(freqs >= 200) & (freqs <= 800)], axis=0)
            mid_band = np.mean(magnitude[(freqs >= 800) & (freqs <= 3200)], axis=0)
            high_mid_band = np.mean(magnitude[(freqs >= 3200) & (freqs <= 8000)], axis=0)
            high_band = np.mean(magnitude[(freqs >= 8000) & (freqs <= 16000)], axis=0)
            
            features["frequency_bands"] = {
                "bass_energy": float(np.mean(bass_band)),
                "low_mid_energy": float(np.mean(low_mid_band)),
                "mid_energy": float(np.mean(mid_band)),
                "high_mid_energy": float(np.mean(high_mid_band)),
                "high_energy": float(np.mean(high_band))
            }
            
            # Harmonic-percussive separation
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            features["hpss"] = {
                "harmonic_energy": float(np.mean(librosa.feature.rms(y=y_harmonic)[0])),
                "percussive_energy": float(np.mean(librosa.feature.rms(y=y_percussive)[0]))
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            return {"error": str(e)}
    
    async def _heuristic_detection(
        self, 
        features: Dict[str, Any], 
        confidence_threshold: float
    ) -> List[Dict[str, Any]]:
        """Detect instruments using heuristic rules."""
        try:
            detections = []
            
            if "error" in features:
                return detections
            
            spectral = features.get("spectral", {})
            freq_bands = features.get("frequency_bands", {})
            hpss = features.get("hpss", {})
            energy = features.get("energy", {})
            zcr = features.get("zcr", {})
            rhythm = features.get("rhythm", {})
            
            # Vocals detection (mid-frequency, harmonic content)
            vocals_confidence = 0.0
            if spectral.get("centroid_mean", 0) > 1000 and spectral.get("centroid_mean", 0) < 4000:
                vocals_confidence += 0.3
            if hpss.get("harmonic_energy", 0) > hpss.get("percussive_energy", 0):
                vocals_confidence += 0.2
            if freq_bands.get("mid_energy", 0) > freq_bands.get("bass_energy", 0):
                vocals_confidence += 0.2
            
            # Adjust for typical vocal characteristics
            if 500 <= spectral.get("centroid_mean", 0) <= 3000:
                vocals_confidence += 0.3
            
            if vocals_confidence >= confidence_threshold:
                detections.append({
                    "type": "vocals",
                    "subtype": self._determine_vocal_subtype(features),
                    "confidence": min(1.0, vocals_confidence)
                })
            
            # Drums detection (high percussive energy, broad spectrum)
            drums_confidence = 0.0
            if hpss.get("percussive_energy", 0) > hpss.get("harmonic_energy", 0):
                drums_confidence += 0.4
            if zcr.get("mean", 0) > 0.1:  # High zero crossing rate
                drums_confidence += 0.2
            if energy.get("dynamic_range", 0) > 0.1:  # High dynamic range
                drums_confidence += 0.2
            if freq_bands.get("high_energy", 0) > 0.05:  # Cymbal/hi-hat energy
                drums_confidence += 0.2
            
            if drums_confidence >= confidence_threshold:
                detections.append({
                    "type": "drums",
                    "subtype": self._determine_drum_subtype(features, rhythm),
                    "confidence": min(1.0, drums_confidence)
                })
            
            # Bass detection (low frequency dominance)
            bass_confidence = 0.0
            if freq_bands.get("bass_energy", 0) > freq_bands.get("mid_energy", 0):
                bass_confidence += 0.4
            if spectral.get("centroid_mean", 0) < 500:
                bass_confidence += 0.3
            if hpss.get("harmonic_energy", 0) > 0.05:  # Some harmonic content
                bass_confidence += 0.3
            
            if bass_confidence >= confidence_threshold:
                detections.append({
                    "type": "bass",
                    "subtype": self._determine_bass_subtype(features),
                    "confidence": min(1.0, bass_confidence)
                })
            
            # Synth detection (electronic characteristics)
            synth_confidence = 0.0
            if spectral.get("bandwidth_mean", 0) > 2000:  # Wide spectral content
                synth_confidence += 0.2
            if energy.get("rms_mean", 0) > 0.1:  # Sustained energy
                synth_confidence += 0.2
            # Additional synth characteristics would be added here
            
            if synth_confidence >= confidence_threshold:
                detections.append({
                    "type": "synth",
                    "subtype": self._determine_synth_subtype(features),
                    "confidence": min(1.0, synth_confidence)
                })
            
            # If no specific instruments detected above threshold, mark as "other"
            if not detections:
                detections.append({
                    "type": "other",
                    "subtype": "mixed",
                    "confidence": 0.5
                })
            
            return detections
            
        except Exception as e:
            logger.error(f"Heuristic detection failed: {e}")
            return []
    
    async def _ml_detection(
        self, 
        features: Dict[str, Any], 
        confidence_threshold: float
    ) -> List[Dict[str, Any]]:
        """Detect instruments using machine learning (placeholder for now)."""
        # This would use the trained ML model
        # For now, fallback to heuristic
        return await self._heuristic_detection(features, confidence_threshold)
    
    def _determine_vocal_subtype(self, features: Dict[str, Any]) -> str:
        """Determine vocal subtype based on features."""
        spectral = features.get("spectral", {})
        centroid = spectral.get("centroid_mean", 0)
        
        if centroid > 2000:
            return "lead_vocals"
        elif centroid > 1000:
            return "backing_vocals"
        else:
            return "rap_vocals"
    
    def _determine_drum_subtype(self, features: Dict[str, Any], rhythm: Dict[str, Any]) -> str:
        """Determine drum subtype based on features."""
        tempo = rhythm.get("tempo", 0)
        
        if 130 <= tempo <= 150:
            return "trap_kit"
        elif tempo > 150:
            return "electronic_drums"
        else:
            return "acoustic_drums"
    
    def _determine_bass_subtype(self, features: Dict[str, Any]) -> str:
        """Determine bass subtype based on features."""
        freq_bands = features.get("frequency_bands", {})
        bass_energy = freq_bands.get("bass_energy", 0)
        
        if bass_energy > 0.2:
            return "808_bass"
        else:
            return "electric_bass"
    
    def _determine_synth_subtype(self, features: Dict[str, Any]) -> str:
        """Determine synth subtype based on features."""
        energy = features.get("energy", {})
        
        if energy.get("rms_mean", 0) > 0.15:
            return "lead_synth"
        else:
            return "pad_synth"
    
    @classmethod
    def get_supported_instruments(cls) -> Dict[str, List[str]]:
        """Get list of supported instruments and their subcategories."""
        return cls.INSTRUMENT_SUBCATEGORIES.copy()
    
    @classmethod
    def get_feature_importance(cls) -> Dict[str, str]:
        """Get information about feature importance for classification."""
        return {
            "spectral_centroid": "Brightness/timbre of the sound",
            "mfcc": "Timbral characteristics and texture",
            "chroma": "Harmonic content and pitch classes",
            "frequency_bands": "Energy distribution across frequency spectrum",
            "hpss": "Harmonic vs percussive content ratio",
            "zcr": "Useful for distinguishing percussive sounds",
            "rhythm": "Tempo and rhythmic patterns"
        }