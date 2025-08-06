"""
Audio visualization module for creating spectrograms, waveforms, and feature plots.
"""

import asyncio
import io
import base64
import time
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
from pathlib import Path

import numpy as np
import librosa
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from PIL import Image

logger = logging.getLogger(__name__)

class AudioVisualizer:
    """Advanced audio visualizer for spectrograms, waveforms, and musical features."""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8), dpi: int = 100):
        """
        Initialize the audio visualizer.
        
        Args:
            figsize: Figure size in inches (width, height)
            dpi: Resolution in dots per inch
        """
        self.figsize = figsize
        self.dpi = dpi
        plt.style.use('dark_background')
        
        # Create custom colormap for spectrograms
        self.spectrogram_cmap = LinearSegmentedColormap.from_list(
            'audio_spectrogram',
            ['#0c0c1e', '#1e1e3f', '#3f1e5f', '#5f1e3f', '#7f3f1e', '#ff5f1e', '#ffff5f'],
            N=256
        )
    
    async def create_waveform(
        self, 
        file_path: str, 
        output_path: Optional[str] = None,
        show_envelope: bool = True,
        normalize: bool = True,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create waveform visualization.
        
        Args:
            file_path: Path to audio file
            output_path: Optional path to save the plot
            show_envelope: Whether to show amplitude envelope
            normalize: Whether to normalize amplitude
            
        Returns:
            Dictionary with plot info and base64 encoded image
        """
        try:
            start_time = time.time()
            
            # Load audio
            y, sr = librosa.load(file_path, sr=None)
            duration = len(y) / sr
            time_axis = np.linspace(0, duration, len(y))
            
            if normalize:
                y = y / np.max(np.abs(y))

            # Reduz a densidade de pontos para evitar OverflowError
            max_points = 10000
            step = max(1, len(y) // max_points)
            y = y[::step]
            x = time_axis[::step]
            
            # Create figure
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            fig.patch.set_facecolor('#0c0c1e')
            
            # Plot waveform
            ax.plot(x, y, color='#00ff88', linewidth=0.5, alpha=0.8)
            
            if show_envelope:
                # Calculate and plot envelope
                envelope = np.abs(y)
                ax.fill_between(x, envelope, alpha=0.3, color='#00ff88')
                ax.fill_between(x, -envelope, alpha=0.3, color='#00ff88')
            
            # Styling
            ax.set_xlabel('Time (seconds)', color='white', fontsize=12)
            ax.set_ylabel('Amplitude', color='white', fontsize=12)
            ax.set_title(f'Waveform - {Path(file_path).name}', color='white', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#0c0c1e')
            
            # Tight layout
            plt.tight_layout()
            
            # Save or encode
            if output_path:
                # Determine output_dir: if output_dir param is not None, use it; else use output_path's dirname
                import os
                # If output_dir is not provided, use the directory of output_path
                dir_to_use = output_dir if output_dir is not None else os.path.dirname(output_path)
                output_filename = f"waveform_{os.path.splitext(os.path.basename(file_path))[0]}.png"
                output_path_final = os.path.join(dir_to_use, output_filename)
                plt.savefig(output_path_final, dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                print(f"📤 Imagem salva em: {output_path_final}")
                image_data = None
                output_path = output_path_final
            else:
                # Encode to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                buffer.seek(0)
                image_data = base64.b64encode(buffer.getvalue()).decode()
                buffer.close()
            
            plt.close()
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'plot_type': 'waveform',
                'file_path': file_path,
                'output_path': output_path,
                'image_base64': image_data,
                'metadata': {
                    'duration_seconds': duration,
                    'sample_rate': sr,
                    'processing_time_seconds': processing_time,
                    'normalized': normalize,
                    'envelope_shown': show_envelope
                }
            }
            
        except Exception as e:
            import traceback
            plt.close('all')  # Clean up any open figures
            return {
                'error': f"Waveform visualization failed: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    async def create_spectrogram(
        self, 
        file_path: str,
        output_path: Optional[str] = None,
        spectrogram_type: str = "stft",
        hop_length: int = 512,
        n_fft: int = 2048
    ) -> Dict[str, Any]:
        """
        Create spectrogram visualization.
        
        Args:
            file_path: Path to audio file
            output_path: Optional path to save the plot
            spectrogram_type: Type of spectrogram ('stft', 'mel', 'cqt')
            hop_length: Hop length for analysis
            n_fft: FFT window size
            
        Returns:
            Dictionary with plot info and base64 encoded image
        """
        try:
            start_time = time.time()
            
            # Load audio
            y, sr = librosa.load(file_path, sr=22050)
            
            # Calculate spectrogram based on type
            if spectrogram_type == "mel":
                S = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length, n_fft=n_fft)
                S_db = librosa.power_to_db(S, ref=np.max)
                title = f"Mel Spectrogram - {Path(file_path).name}"
                ylabel = "Mel Frequency"
            elif spectrogram_type == "cqt":
                S = np.abs(librosa.cqt(y=y, sr=sr, hop_length=hop_length))
                S_db = librosa.amplitude_to_db(S, ref=np.max)
                title = f"Constant-Q Transform - {Path(file_path).name}"
                ylabel = "CQT Frequency"
            else:  # stft
                S = np.abs(librosa.stft(y, hop_length=hop_length, n_fft=n_fft))
                S_db = librosa.amplitude_to_db(S, ref=np.max)
                title = f"STFT Spectrogram - {Path(file_path).name}"
                ylabel = "Frequency (Hz)"
            
            # Create figure
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            fig.patch.set_facecolor('#0c0c1e')

            # Choose y_axis parameter for specshow
            tipo_espectrograma = spectrogram_type
            y_axis = (
                "log" if tipo_espectrograma == "mel"
                else "cqt_note" if tipo_espectrograma == "cqt"
                else "linear"
            )
            # Plot spectrogram
            img = librosa.display.specshow(
                S_db, 
                sr=sr, 
                hop_length=hop_length,
                x_axis='time', 
                y_axis=y_axis,
                ax=ax,
                cmap=self.spectrogram_cmap
            )
            
            # Add colorbar
            cbar = plt.colorbar(img, ax=ax, format='%+2.0f dB')
            cbar.ax.yaxis.set_tick_params(color='white')
            cbar.ax.yaxis.label.set_color('white')
            
            # Styling
            ax.set_xlabel('Time (seconds)', color='white', fontsize=12)
            ax.set_ylabel(ylabel, color='white', fontsize=12)
            ax.set_title(title, color='white', fontsize=14, fontweight='bold')
            ax.set_facecolor('#0c0c1e')
            
            plt.tight_layout()
            
            # Save or encode
            if output_path:
                plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                image_data = None
            else:
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                buffer.seek(0)
                image_data = base64.b64encode(buffer.getvalue()).decode()
                buffer.close()
            
            plt.close()
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'plot_type': f'{spectrogram_type}_spectrogram',
                'file_path': file_path,
                'output_path': output_path,
                'image_base64': image_data,
                'metadata': {
                    'spectrogram_type': spectrogram_type,
                    'hop_length': hop_length,
                    'n_fft': n_fft,
                    'sample_rate': sr,
                    'processing_time_seconds': processing_time
                }
            }
            
        except Exception as e:
            import traceback
            plt.close('all')
            return {
                'error': f"Spectrogram visualization failed: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    async def create_feature_analysis_plot(
        self, 
        features: Dict[str, Any],
        output_path: Optional[str] = None,
        plot_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Create visualization of extracted musical features.
        
        Args:
            features: Feature dictionary from analysis
            output_path: Optional path to save the plot
            plot_type: Type of feature plot ('comprehensive', 'spectral', 'rhythmic')
            
        Returns:
            Dictionary with plot info and base64 encoded image
        """
        try:
            start_time = time.time()
            axes = []
            if plot_type == "comprehensive":
                fig, axes_arr = plt.subplots(2, 2, figsize=(16, 12), dpi=self.dpi)
                fig.patch.set_facecolor('#0c0c1e')
                axes = axes_arr.flatten()
                
                # MFCC visualization
                if 'spectral' in features and 'mfcc' in features['spectral']:
                    mfcc_mean = features['spectral']['mfcc']['mean']
                    axes[0].bar(range(len(mfcc_mean)), mfcc_mean, color='#ff6b35', alpha=0.8)
                    axes[0].set_title('MFCC Coefficients', color='white', fontweight='bold')
                    axes[0].set_xlabel('Coefficient Index', color='white')
                    axes[0].set_ylabel('Mean Value', color='white')
                    axes[0].set_facecolor('#0c0c1e')
                    axes[0].grid(True, alpha=0.3)
                
                # Chroma visualization
                if 'harmonic' in features and 'chroma_vector' in features['harmonic']:
                    chroma = features['harmonic']['chroma_vector']
                    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                    axes[1].bar(range(len(chroma)), chroma, color='#4ecdc4', alpha=0.8)
                    axes[1].set_title('Chroma Features', color='white', fontweight='bold')
                    axes[1].set_xlabel('Pitch Class', color='white')
                    axes[1].set_ylabel('Chroma Energy', color='white')
                    axes[1].set_xticks(range(12))
                    axes[1].set_xticklabels(note_names, color='white')
                    axes[1].set_facecolor('#0c0c1e')
                    axes[1].grid(True, alpha=0.3)
                
                # Frequency bands
                if 'rhythmic' in features:
                    rhythmic = features['rhythmic']
                    bands = ['Low', 'Mid', 'High']
                    energies = [
                        rhythmic.get('low_freq_energy', 0),
                        rhythmic.get('mid_freq_energy', 0),
                        rhythmic.get('high_freq_energy', 0)
                    ]
                    colors = ['#ff6b35', '#4ecdc4', '#45b7d1']
                    axes[2].pie(energies, labels=bands, colors=colors, autopct='%1.1f%%', startangle=90)
                    axes[2].set_title('Frequency Band Distribution', color='white', fontweight='bold')
                    axes[2].set_facecolor('#0c0c1e')
                
                # Tempo and rhythm info
                tempo_info = []
                if 'temporal' in features:
                    tempo_info.append(f"Tempo: {features['temporal'].get('tempo_bpm', 0):.1f} BPM")
                    tempo_info.append(f"Beat Consistency: {features['temporal'].get('beat_consistency', 0):.2f}")
                if 'harmonic' in features:
                    tempo_info.append(f"Key: {features['harmonic'].get('estimated_key', 'Unknown')}")
                    tempo_info.append(f"Key Confidence: {features['harmonic'].get('key_confidence', 0):.2f}")
                
                axes[3].text(0.1, 0.7, '\n'.join(tempo_info), color='white', fontsize=14, 
                           transform=axes[3].transAxes, verticalalignment='top')
                axes[3].set_title('Musical Properties', color='white', fontweight='bold')
                axes[3].axis('off')
                axes[3].set_facecolor('#0c0c1e')
                
                title = "Comprehensive Feature Analysis"
            elif plot_type == "spectral":
                spectral_data = {}
                spectral_features = features.get("spectral", {})
                if "centroid" in spectral_features:
                    spectral_data["Spectral Centroid"] = np.mean(spectral_features["centroid"])
                if "bandwidth" in spectral_features:
                    spectral_data["Spectral Bandwidth"] = np.mean(spectral_features["bandwidth"])
                if "rolloff" in spectral_features:
                    spectral_data["Spectral Rolloff"] = np.mean(spectral_features["rolloff"])
                if "flatness" in spectral_features:
                    spectral_data["Spectral Flatness"] = np.mean(spectral_features["flatness"])

                if spectral_data:
                    plt.figure(figsize=(10, 4))
                    bars = plt.bar(spectral_data.keys(), spectral_data.values(), color="#80cbc4")
                    plt.title("Spectral Feature Analysis", fontsize=14, weight="bold")
                    plt.ylabel("Mean Value")
                    plt.gca().set_facecolor("#000000")
                    plt.gcf().patch.set_facecolor("#0c0c1e")
                    plt.tight_layout()
                    # Ensure title is set before suptitle usage
                    title = "Spectral Feature Analysis"
                else:
                    raise ValueError("No spectral features found in analysis result.")
            elif plot_type == "rhythmic":
                fig, ax = plt.subplots(figsize=(10, 4))
                rhythmic_data = features.get("rhythmic", {})

                stability = rhythmic_data.get("tempo_stability", 0)
                complexity = rhythmic_data.get("rhythm_complexity", 0)
                bass = rhythmic_data.get("rhythm_balance", {}).get("bass_prominence", 0)
                mid = rhythmic_data.get("rhythm_balance", {}).get("mid_prominence", 0)
                high = rhythmic_data.get("rhythm_balance", {}).get("high_prominence", 0)
                tempo = rhythmic_data.get("tempo_bpm", 0)

                labels = ["Stability", "Complexity", "Bass", "Mid", "High"]
                values = [stability, complexity, bass, mid, high]

                ax.bar(labels, values, color="#77d9d9")
                ax.set_title("Rhythmic Features")
                ax.set_ylabel("Value")

                # Exibe o tempo em texto ao lado
                ax.text(
                    1.05, 0.9,
                    f"Tempo: {tempo:.1f} BPM",
                    transform=ax.transAxes,
                    color="white",
                    fontsize=12,
                    verticalalignment='top',
                    bbox=dict(boxstyle="round", facecolor="black", edgecolor="white")
                )

                axes.append(ax)
                title = "Rhythmic Feature Analysis"
            # Style all axes
            for ax in axes:
                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('white')
            
            plt.suptitle(title, color='white', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            # Save or encode
            if output_path:
                plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                image_data = None
            else:
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                buffer.seek(0)
                image_data = base64.b64encode(buffer.getvalue()).decode()
                buffer.close()
            
            plt.close()
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'plot_type': 'feature_analysis',
                'output_path': output_path,
                'image_base64': image_data,
                'metadata': {
                    'plot_type': plot_type,
                    'processing_time_seconds': processing_time
                }
            }
            
        except Exception as e:
            import traceback
            plt.close('all')
            return {
                'error': f"Feature analysis plot failed: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    async def create_stems_comparison(
        self, 
        stems_data: Dict[str, str],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create comparison visualization of separated stems.
        
        Args:
            stems_data: Dictionary mapping stem names to file paths
            output_path: Optional path to save the plot
            
        Returns:
            Dictionary with plot info and base64 encoded image
        """
        try:
            start_time = time.time()
            
            stem_names = list(stems_data.keys())
            n_stems = len(stem_names)
            
            if n_stems == 0:
                raise ValueError("No stems provided for visualization")
            
            # Create subplots
            fig, axes = plt.subplots(n_stems, 1, figsize=(self.figsize[0], 3 * n_stems), dpi=self.dpi)
            fig.patch.set_facecolor('#0c0c1e')
            
            if n_stems == 1:
                axes = [axes]
            
            colors = ['#ff6b35', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b']
            
            for i, (stem_name, stem_path) in enumerate(stems_data.items()):
                if not Path(stem_path).exists():
                    continue
                
                # Load stem audio
                y, sr = librosa.load(stem_path, sr=22050)
                duration = len(y) / sr
                time_axis = np.linspace(0, duration, len(y))
                
                # Normalize
                y = y / (np.max(np.abs(y)) + 1e-8)
                
                # Plot waveform
                color = colors[i % len(colors)]
                axes[i].plot(time_axis, y, color=color, linewidth=0.8, alpha=0.9)
                axes[i].fill_between(time_axis, y, alpha=0.3, color=color)
                
                # Styling
                axes[i].set_title(f'{stem_name.capitalize()} Stem', color='white', fontweight='bold')
                axes[i].set_ylabel('Amplitude', color='white')
                axes[i].grid(True, alpha=0.3)
                axes[i].set_facecolor('#0c0c1e')
                axes[i].tick_params(colors='white')
                for spine in axes[i].spines.values():
                    spine.set_color('white')
            
            # Only add x-label to bottom plot
            axes[-1].set_xlabel('Time (seconds)', color='white')
            
            plt.suptitle('Separated Audio Stems Comparison', color='white', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            # Save or encode
            if output_path:
                plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                image_data = None
            else:
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight', facecolor='#0c0c1e')
                buffer.seek(0)
                image_data = base64.b64encode(buffer.getvalue()).decode()
                buffer.close()
            
            plt.close()
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'plot_type': 'stems_comparison',
                'stems_analyzed': list(stems_data.keys()),
                'output_path': output_path,
                'image_base64': image_data,
                'metadata': {
                    'stems_count': n_stems,
                    'processing_time_seconds': processing_time
                }
            }
            
        except Exception as e:
            import traceback
            plt.close('all')
            return {
                'error': f"Stems comparison visualization failed: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    @classmethod
    def get_supported_plot_types(cls) -> List[str]:
        """Get list of supported plot types."""
        return [
            'waveform',
            'stft_spectrogram', 
            'mel_spectrogram',
            'cqt_spectrogram',
            'feature_analysis',
            'stems_comparison'
        ]
    
    @classmethod
    def get_plot_descriptions(cls) -> Dict[str, str]:
        """Get descriptions of available plot types."""
        return {
            'waveform': 'Time-domain waveform with optional amplitude envelope',
            'stft_spectrogram': 'Short-Time Fourier Transform spectrogram',
            'mel_spectrogram': 'Mel-scale spectrogram (perceptually motivated)',
            'cqt_spectrogram': 'Constant-Q Transform spectrogram (musical pitch)',
            'feature_analysis': 'Comprehensive musical feature visualization',
            'stems_comparison': 'Side-by-side comparison of separated audio stems'
        }