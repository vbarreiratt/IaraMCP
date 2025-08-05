"""
Audio source separation module using Demucs for stem separation.
"""

import asyncio
import os
import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import logging

import torch
import torchaudio
import numpy as np
from demucs import pretrained
from demucs.separate import save_audio
from demucs.apply import apply_model

from .utils import validate_audio_file, get_audio_info, format_duration

logger = logging.getLogger(__name__)

class SourceSeparator:
    """Source separation using Demucs models."""
    
    AVAILABLE_MODELS = {
        'htdemucs_ft': 'Hybrid Transformer Demucs (Fine-tuned) - Best quality',
        'htdemucs': 'Hybrid Transformer Demucs - Good quality, faster',
        'hdemucs_mmi': 'Hybrid Demucs MMI - Good for older songs',
        'mdx': 'MDX - Faster, good for vocals',
        'mdx_extra': 'MDX Extra - Better separation, slower'
    }
    
    STEMS = ['drums', 'bass', 'other', 'vocals']
    
    def __init__(self, model_name: str = 'htdemucs_ft', device: str = 'auto'):
        """
        Initialize the source separator.
        
        Args:
            model_name: Demucs model to use
            device: Device to run on ('auto', 'cpu', 'cuda', 'mps')
        """
        self.model_name = model_name
        self.device = self._get_device(device)
        self.model = None
        self._model_loaded = False
        
    def _get_device(self, device: str) -> str:
        """Determine the best device to use."""
        if device == 'auto':
            if torch.cuda.is_available():
                return 'cuda'
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return 'mps'
            else:
                return 'cpu'
        return device
    
    async def load_model(self) -> bool:
        """Load the Demucs model."""
        if self._model_loaded and self.model is not None:
            return True
            
        try:
            logger.info(f"Loading Demucs model: {self.model_name}")
            # Run model loading in thread to avoid blocking
            loop = asyncio.get_event_loop()
            self.model = await loop.run_in_executor(
                None, 
                pretrained.get_model, 
                self.model_name
            )
            self.model.to(self.device)
            self.model.eval()
            self._model_loaded = True
            logger.info(f"Model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            return False
    
    async def separate_audio(
        self, 
        file_path: str, 
        output_dir: Optional[str] = None,
        format: str = 'wav',
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Separate audio file into stems.
        
        Args:
            file_path: Path to input audio file
            output_dir: Directory to save stems (None for temp dir)
            format: Output format ('wav', 'mp3', 'flac')
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with separation results and stem paths
        """
        start_time = time.time()
        
        try:
            # Validate input file
            validation = validate_audio_file(file_path)
            if not validation['valid']:
                return {'error': f"Invalid audio file: {validation['error']}"}
            
            # Progress update
            if progress_callback:
                await progress_callback("Validating audio file", 10)
            
            # Load model if not loaded
            if not await self.load_model():
                return {'error': f"Failed to load model {self.model_name}"}
                
            if progress_callback:
                await progress_callback("Model loaded", 20)
            
            # Setup output directory
            if output_dir is None:
                output_dir = tempfile.mkdtemp(prefix='demucs_separation_')
                temp_dir = True
            else:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                temp_dir = False
            
            # Load audio
            if progress_callback:
                await progress_callback("Loading audio", 30)
                
            loop = asyncio.get_event_loop()
            audio, sr = await loop.run_in_executor(
                None, 
                torchaudio.load,
                file_path
            )
            
            # Ensure audio is the right format for the model
            if audio.shape[0] == 1:  # Mono to stereo
                audio = audio.repeat(2, 1)
            elif audio.shape[0] > 2:  # Multi-channel to stereo
                audio = audio[:2]
            
            # Move audio to device
            audio = audio.to(self.device)
            
            if progress_callback:
                await progress_callback("Separating audio sources", 50)
            
            # Apply separation
            with torch.no_grad():
                def apply_model_sync():
                    return apply_model(self.model, audio.unsqueeze(0), device=self.device)
                
                separated = await loop.run_in_executor(
                    None,
                    apply_model_sync
                )
            
            separated = separated.squeeze(0)  # Remove batch dimension
            
            if progress_callback:
                await progress_callback("Saving stems", 70)
            
            # Save stems
            stem_paths = {}
            quality_metrics = {}
            
            for i, stem_name in enumerate(self.STEMS):
                stem_audio = separated[i]
                
                # Calculate quality metrics
                rms_energy = torch.sqrt(torch.mean(stem_audio ** 2)).item()
                max_amplitude = torch.max(torch.abs(stem_audio)).item()
                
                quality_metrics[stem_name] = {
                    'rms_energy': float(rms_energy),
                    'max_amplitude': float(max_amplitude),
                    'confidence': self._calculate_stem_confidence(stem_audio, stem_name),
                    'duration_seconds': stem_audio.shape[-1] / sr
                }
                
                # Save stem - move to CPU first to avoid MPS/CUDA issues
                stem_filename = f"{Path(file_path).stem}_{stem_name}.{format}"
                stem_path = os.path.join(output_dir, stem_filename)
                
                # Move tensor to CPU before saving
                stem_audio_cpu = stem_audio.cpu()
                
                await loop.run_in_executor(
                    None,
                    save_audio,
                    stem_audio_cpu,
                    stem_path,
                    sr,
                    format
                )
                
                stem_paths[stem_name] = {
                    'path': stem_path,
                    'size_bytes': os.path.getsize(stem_path) if os.path.exists(stem_path) else 0,
                    'format': format
                }
            
            if progress_callback:
                await progress_callback("Separation complete", 100)
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'metadata': {
                    'input_file': file_path,
                    'output_directory': output_dir,
                    'temporary_directory': temp_dir,
                    'model_used': self.model_name,
                    'device': self.device,
                    'processing_time_seconds': processing_time,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'output_format': format
                },
                'separation': {
                    'method': 'demucs',
                    'model': self.model_name,
                    'stems': stem_paths,
                    'quality_metrics': quality_metrics
                },
                'file_info': get_audio_info(file_path)
            }
            
        except Exception as e:
            import traceback
            logger.error(f"Separation failed: {e}")
            return {
                'error': f"Audio separation failed: {str(e)}",
                'traceback': traceback.format_exc(),
                'processing_time_seconds': time.time() - start_time
            }
    
    def _calculate_stem_confidence(self, stem_audio: torch.Tensor, stem_name: str) -> float:
        """Calculate confidence score for a separated stem."""
        try:
            # Convert to numpy for analysis
            audio_np = stem_audio.cpu().numpy()
            
            # Basic confidence based on energy and spectral characteristics
            rms_energy = np.sqrt(np.mean(audio_np ** 2))
            
            # Different stems have different expected characteristics
            if stem_name == 'vocals':
                # Vocals typically have mid-frequency energy
                confidence = min(1.0, rms_energy * 10)  # Scale for vocals
            elif stem_name == 'drums':
                # Drums have high transients and broad spectrum
                confidence = min(1.0, rms_energy * 8)
            elif stem_name == 'bass':
                # Bass has low-frequency energy
                confidence = min(1.0, rms_energy * 12)
            else:  # other
                # Other instruments
                confidence = min(1.0, rms_energy * 6)
            
            # Ensure minimum confidence for any non-silent stem
            if rms_energy > 0.001:
                confidence = max(0.1, confidence)
            
            return float(confidence)
            
        except Exception as e:
            logger.warning(f"Failed to calculate confidence for {stem_name}: {e}")
            return 0.5  # Default confidence
    
    async def analyze_stem_quality(self, stem_path: str) -> Dict[str, Any]:
        """Analyze the quality of a separated stem."""
        try:
            if not os.path.exists(stem_path):
                return {'error': f"Stem file not found: {stem_path}"}
            
            # Load stem audio
            audio, sr = torchaudio.load(stem_path)
            audio_np = audio.cpu().numpy()
            
            # Calculate quality metrics
            rms_energy = np.sqrt(np.mean(audio_np ** 2))
            max_amplitude = np.max(np.abs(audio_np))
            dynamic_range = max_amplitude - np.min(np.abs(audio_np[audio_np != 0]))
            
            # Spectral analysis
            fft = np.fft.rfft(audio_np.flatten())
            magnitude = np.abs(fft)
            freqs = np.fft.rfftfreq(len(audio_np.flatten()), 1/sr)
            
            # Frequency band analysis
            low_band = np.mean(magnitude[(freqs >= 20) & (freqs <= 200)])
            mid_band = np.mean(magnitude[(freqs >= 200) & (freqs <= 2000)])
            high_band = np.mean(magnitude[(freqs >= 2000) & (freqs <= 8000)])
            
            return {
                'file_path': stem_path,
                'quality_metrics': {
                    'rms_energy': float(rms_energy),
                    'max_amplitude': float(max_amplitude),
                    'dynamic_range': float(dynamic_range),
                    'spectral_balance': {
                        'low_freq_energy': float(low_band),
                        'mid_freq_energy': float(mid_band),
                        'high_freq_energy': float(high_band)
                    },
                    'duration_seconds': len(audio_np.flatten()) / sr,
                    'sample_rate': sr,
                    'channels': audio.shape[0]
                }
            }
            
        except Exception as e:
            import traceback
            return {
                'error': f"Stem quality analysis failed: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    @classmethod
    def get_available_models(cls) -> Dict[str, str]:
        """Get list of available Demucs models."""
        return cls.AVAILABLE_MODELS.copy()
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Get list of supported output formats."""
        return ['wav', 'mp3', 'flac']
    
    def cleanup_temp_files(self, output_dir: str) -> bool:
        """Clean up temporary files."""
        try:
            if os.path.exists(output_dir) and 'demucs_separation_' in output_dir:
                shutil.rmtree(output_dir)
                return True
        except Exception as e:
            logger.warning(f"Failed to cleanup temp directory {output_dir}: {e}")
        return False