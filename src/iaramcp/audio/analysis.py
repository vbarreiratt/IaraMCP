"""
Audio analysis module using librosa for comprehensive musical feature extraction.
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Any
import logging
from pathlib import Path

import numpy as np
import librosa
import soundfile as sf
from scipy import stats

from .utils import validate_audio_file, get_audio_info, format_duration

logger = logging.getLogger(__name__)

class AudioAnalyzer:
    """Main class for audio analysis using librosa."""
    
    def __init__(self, sr: int = 22050):
        """
        Initialize the audio analyzer.
        
        Args:
            sr: Sample rate for analysis (default: 22050 Hz)
        """
        self.sr = sr
        self.hop_length = 512
        self.n_fft = 2048
        
    async def analyze_basic(self, file_path: str) -> Dict[str, Any]:
        """
        Perform basic audio analysis.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with basic analysis results
        """
        start_time = time.time()
        
        # Validate file
        validation = validate_audio_file(file_path)
        if not validation['valid']:
            raise ValueError(f"Invalid audio file: {validation['error']}")
        
        # Load audio
        y, sr = librosa.load(file_path, sr=self.sr)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Basic tempo analysis
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        # Basic spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        # RMS energy
        rms = librosa.feature.rms(y=y)[0]
        
        processing_time = time.time() - start_time
        
        result = {
            'metadata': {
                'file_info': get_audio_info(file_path),
                'processing_time_seconds': processing_time,
                'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_type': 'basic',
                'sample_rate': sr,
                'duration_seconds': duration,
                'duration_formatted': format_duration(duration)
            },
            'basic_features': {
                'tempo_bpm': float(tempo),
                'duration_seconds': duration,
                'spectral_centroid_mean': float(np.mean(spectral_centroids)),
                'spectral_centroid_std': float(np.std(spectral_centroids)),
                'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
                'rms_energy_mean': float(np.mean(rms)),
                'rms_energy_std': float(np.std(rms))
            }
        }
        
        return result
    
    async def analyze_complete(self, file_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive audio analysis.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with complete analysis results
        """
        start_time = time.time()
        
        # Validate file
        validation = validate_audio_file(file_path)
        if not validation['valid']:
            raise ValueError(f"Invalid audio file: {validation['error']}")
        
        # Load audio
        y, sr = librosa.load(file_path, sr=self.sr)
        duration = librosa.get_duration(y=y, sr=sr)

        # --- Spectral analysis for plot_type='spectral' ---
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()

        # We'll add these to the 'spectral' features dictionary below
        spectral_summary = {
            "centroid": float(spectral_centroid),
            "rolloff": float(spectral_rolloff),
            "bandwidth": float(spectral_bandwidth),
        }
        # --- End spectral analysis block ---
        
        # Run analysis in chunks to avoid blocking
        temporal_features = await self._analyze_temporal_features(y, sr)
        spectral_features = await self._analyze_spectral_features(y, sr)
        harmonic_features = await self._analyze_harmonic_features(y, sr)
        rhythmic_features = await self._analyze_rhythmic_features(y, sr)

        # Ensure spectral_summary is included in the 'spectral' dict
        if isinstance(spectral_features, dict):
            spectral_features = dict(spectral_features)  # shallow copy
            spectral_features["centroid"] = spectral_summary["centroid"]
            spectral_features["rolloff"] = spectral_summary["rolloff"]
            spectral_features["bandwidth"] = spectral_summary["bandwidth"]

        processing_time = time.time() - start_time
        
        result = {
            'metadata': {
                'file_info': get_audio_info(file_path),
                'processing_time_seconds': processing_time,
                'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_type': 'complete',
                'sample_rate': sr,
                'duration_seconds': duration,
                'duration_formatted': format_duration(duration)
            },
            'analysis': {
                'temporal': temporal_features,
                'spectral': spectral_features,
                'harmonic': harmonic_features,
                'rhythmic': rhythmic_features
            }
        }
        
        return result
    
    async def _analyze_temporal_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze temporal features like tempo and beats."""
        # Allow other tasks to run
        await asyncio.sleep(0.001)
        
        # Tempo and beat tracking
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        
        # Onset detection
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=self.hop_length)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)
        
        # Beat consistency
        beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=self.hop_length)
        if len(beat_times) > 1:
            beat_intervals = np.diff(beat_times)
            beat_consistency = 1.0 - (np.std(beat_intervals) / np.mean(beat_intervals))
        else:
            beat_consistency = 0.0
        
        return {
            'tempo_bpm': float(tempo),
            'beat_count': len(beats),
            'beat_consistency': float(beat_consistency),
            'onset_count': len(onset_frames),
            'onset_rate_per_second': len(onset_frames) / (len(y) / sr),
            'estimated_time_signature': '4/4'  # Simplified for now
        }
    
    async def _analyze_spectral_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze spectral features like MFCC, spectral centroid, etc."""
        # Allow other tasks to run
        await asyncio.sleep(0.001)
        
        # MFCC features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=self.hop_length)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=self.hop_length)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=self.hop_length)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=self.hop_length)[0]
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=self.hop_length)[0]
        
        # RMS energy
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        
        return {
            'mfcc': {
                'mean': [float(x) for x in np.mean(mfccs, axis=1)],
                'std': [float(x) for x in np.std(mfccs, axis=1)]
            },
            'spectral_centroid': {
                'mean': float(np.mean(spectral_centroids)),
                'std': float(np.std(spectral_centroids)),
                'median': float(np.median(spectral_centroids))
            },
            'spectral_bandwidth': {
                'mean': float(np.mean(spectral_bandwidth)),
                'std': float(np.std(spectral_bandwidth))
            },
            'spectral_rolloff': {
                'mean': float(np.mean(spectral_rolloff)),
                'std': float(np.std(spectral_rolloff))
            },
            'zero_crossing_rate': {
                'mean': float(np.mean(zcr)),
                'std': float(np.std(zcr))
            },
            'rms_energy': {
                'mean': float(np.mean(rms)),
                'std': float(np.std(rms)),
                'max': float(np.max(rms)),
                'dynamic_range': float(np.max(rms) - np.min(rms))
            }
        }
    
    async def _analyze_harmonic_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze harmonic features like chroma and key detection."""
        # Allow other tasks to run
        await asyncio.sleep(0.001)
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=self.hop_length)
        chroma_mean = np.mean(chroma, axis=1)
        
        # Key detection (simplified approach)
        key_profiles = {
            'C': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            'C#': [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            'D': [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            'D#': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            'E': [0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            'F': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
            'F#': [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
            'G': [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            'G#': [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            'A': [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            'A#': [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
            'B': [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
        }
        
        # Find best matching key
        best_key = 'C'
        best_score = 0
        for key, profile in key_profiles.items():
            score = np.corrcoef(chroma_mean, profile)[0, 1]
            if not np.isnan(score) and score > best_score:
                best_score = score
                best_key = key
        
        # Harmonic-percussive separation
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        harmonic_energy = np.mean(librosa.feature.rms(y=y_harmonic)[0])
        percussive_energy = np.mean(librosa.feature.rms(y=y_percussive)[0])
        
        return {
            'chroma_vector': [float(x) for x in chroma_mean],
            'estimated_key': best_key,
            'key_confidence': float(best_score) if not np.isnan(best_score) else 0.0,
            'harmonic_energy': float(harmonic_energy),
            'percussive_energy': float(percussive_energy),
            'harmonic_percussive_ratio': float(harmonic_energy / (percussive_energy + 1e-8))
        }
    
    async def _analyze_rhythmic_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze rhythmic features and patterns."""
        # Allow other tasks to run
        await asyncio.sleep(0.001)
        
        # Tempo and beats
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        
        # Tempogram for tempo stability analysis
        tempogram = librosa.feature.tempogram(y=y, sr=sr, hop_length=self.hop_length)
        tempo_stability = float(1.0 - (np.std(tempogram) / (np.mean(tempogram) + 1e-8)))
        
        # Rhythm patterns (simplified)
        # Analyze energy in different frequency bands
        stft = librosa.stft(y, hop_length=self.hop_length, n_fft=self.n_fft)
        magnitude = np.abs(stft)
        
        # Define frequency bands for rhythm analysis
        freqs = librosa.fft_frequencies(sr=sr, n_fft=self.n_fft)
        low_band = np.where((freqs >= 20) & (freqs <= 200))[0]  # Bass/kick
        mid_band = np.where((freqs >= 200) & (freqs <= 2000))[0]  # Snare/mid
        high_band = np.where((freqs >= 2000) & (freqs <= 8000))[0]  # Hi-hats/cymbals
        
        low_energy = np.mean(magnitude[low_band, :], axis=0)
        mid_energy = np.mean(magnitude[mid_band, :], axis=0)
        high_energy = np.mean(magnitude[high_band, :], axis=0)
        
        return {
            'tempo_bpm': float(tempo),
            'tempo_stability': tempo_stability,
            'beat_count': len(beats),
            'rhythm_complexity': float(np.std(np.diff(beats)) / np.mean(np.diff(beats)) if len(beats) > 1 else 0),
            'low_freq_energy': float(np.mean(low_energy)),
            'mid_freq_energy': float(np.mean(mid_energy)),
            'high_freq_energy': float(np.mean(high_energy)),
            'rhythm_balance': {
                'bass_prominence': float(np.mean(low_energy) / (np.mean(low_energy + mid_energy + high_energy) + 1e-8)),
                'mid_prominence': float(np.mean(mid_energy) / (np.mean(low_energy + mid_energy + high_energy) + 1e-8)),
                'high_prominence': float(np.mean(high_energy) / (np.mean(low_energy + mid_energy + high_energy) + 1e-8))
            }
        }