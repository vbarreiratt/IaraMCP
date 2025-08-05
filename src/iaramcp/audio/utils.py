"""
Audio utility functions for file validation and processing.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {
    '.mp3': 'MP3',
    '.wav': 'WAV', 
    '.flac': 'FLAC',
    '.m4a': 'M4A',
    '.ogg': 'OGG',
    '.aac': 'AAC',
    '.wma': 'WMA'
}

def validate_audio_file(file_path: str) -> Dict[str, any]:
    """
    Validate if a file is a supported audio format.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'file_path': file_path,
        'exists': False,
        'format': None,
        'size_bytes': 0,
        'error': None
    }
    
    try:
        file_path_obj = Path(file_path)
        
        # Check if file exists
        if not file_path_obj.exists():
            result['error'] = f"File does not exist: {file_path}"
            return result
        
        result['exists'] = True
        result['size_bytes'] = file_path_obj.stat().st_size
        
        # Check file extension
        file_extension = file_path_obj.suffix.lower()
        if file_extension not in SUPPORTED_FORMATS:
            result['error'] = f"Unsupported file format: {file_extension}. Supported formats: {list(SUPPORTED_FORMATS.keys())}"
            return result
        
        result['format'] = SUPPORTED_FORMATS[file_extension]
        
        # Check file size (basic validation)
        if result['size_bytes'] == 0:
            result['error'] = "File is empty"
            return result
        
        # File size warning for very large files (>100MB)
        if result['size_bytes'] > 100 * 1024 * 1024:
            logger.warning(f"Large file detected: {result['size_bytes']/1024/1024:.2f} MB")
        
        result['valid'] = True
        
    except Exception as e:
        result['error'] = f"Error validating file: {str(e)}"
        logger.error(f"File validation error: {e}")
    
    return result

def get_audio_info(file_path: str) -> Dict[str, any]:
    """
    Get basic information about an audio file without loading it.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary with file information
    """
    validation = validate_audio_file(file_path)
    
    if not validation['valid']:
        return validation
    
    file_path_obj = Path(file_path)
    
    info = {
        'file_name': file_path_obj.name,
        'file_path': str(file_path_obj.absolute()),
        'format': validation['format'],
        'size_bytes': validation['size_bytes'],
        'size_mb': validation['size_bytes'] / (1024 * 1024),
        'extension': file_path_obj.suffix.lower()
    }
    
    return info

def format_duration(duration_seconds: float) -> str:
    """
    Format duration in seconds to a human-readable string.
    
    Args:
        duration_seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "2:34.5")
    """
    minutes = int(duration_seconds // 60)
    seconds = duration_seconds % 60
    return f"{minutes}:{seconds:04.1f}"

def ensure_output_directory(output_path: str) -> str:
    """
    Ensure output directory exists, create if necessary.
    
    Args:
        output_path: Path to output directory or file
        
    Returns:
        Absolute path to the directory
    """
    output_path_obj = Path(output_path)
    
    # If it's a file path, get the directory
    if output_path_obj.suffix:
        output_dir = output_path_obj.parent
    else:
        output_dir = output_path_obj
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return str(output_dir.absolute())