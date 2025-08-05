#!/usr/bin/env python3
"""
Basic test script to verify the IaraMCP server functionality
without running the full MCP protocol.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from iaramcp.audio.analysis import AudioAnalyzer
from iaramcp.audio.utils import validate_audio_file

async def test_audio_analysis():
    """Test the audio analysis functionality."""
    
    # Test file path
    test_file = "/Users/vitor/Desktop/NA ONDA DA BABYLON.m4a"
    
    print("🎵 Testing IaraMCP Analysis Server")
    print("=" * 50)
    
    # Test 1: File validation
    print("\n1. Testing file validation...")
    validation_result = validate_audio_file(test_file)
    print(f"   File valid: {validation_result['valid']}")
    if validation_result['valid']:
        print(f"   Format: {validation_result['format']}")
        print(f"   Size: {validation_result['size_bytes'] / (1024*1024):.2f} MB")
    else:
        print(f"   Error: {validation_result['error']}")
        return
    
    # Test 2: Basic analysis
    print("\n2. Testing basic audio analysis...")
    try:
        analyzer = AudioAnalyzer()
        basic_result = await analyzer.analyze_basic(test_file)
        
        print("   ✅ Basic analysis completed!")
        print(f"   Duration: {basic_result['metadata']['duration_formatted']}")
        print(f"   Tempo: {basic_result['basic_features']['tempo_bpm']:.1f} BPM")
        print(f"   Processing time: {basic_result['metadata']['processing_time_seconds']:.2f}s")
        
    except Exception as e:
        print(f"   ❌ Basic analysis failed: {e}")
        return
    
    # Test 3: Complete analysis  
    print("\n3. Testing complete audio analysis...")
    try:
        complete_result = await analyzer.analyze_complete(test_file)
        
        print("   ✅ Complete analysis completed!")
        print(f"   Estimated key: {complete_result['analysis']['harmonic']['estimated_key']}")
        print(f"   Tempo stability: {complete_result['analysis']['rhythmic']['tempo_stability']:.2f}")
        print(f"   Processing time: {complete_result['metadata']['processing_time_seconds']:.2f}s")
        
        # Show some spectral features
        spectral = complete_result['analysis']['spectral']
        print(f"   Spectral centroid (mean): {spectral['spectral_centroid']['mean']:.0f} Hz")
        print(f"   RMS energy (mean): {spectral['rms_energy']['mean']:.4f}")
        
    except Exception as e:
        print(f"   ❌ Complete analysis failed: {e}")
        return
    
    print("\n✅ All tests passed! IaraMCP server should work correctly.")
    print("\nTo use with Claude Desktop, add this to your config:")
    print('''
{
  "mcpServers": {
    "advanced-music-analysis": {
      "command": "python",
      "args": ["-m", "iaramcp.server"],
      "env": {"PYTHONPATH": "/Users/vitor/Desktop/analisemusicalavancado/src"}
    }
  }
}
    ''')

if __name__ == "__main__":
    asyncio.run(test_audio_analysis())