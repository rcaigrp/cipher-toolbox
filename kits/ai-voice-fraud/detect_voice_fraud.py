#!/usr/bin/env python3

import os
import sys
import hashlib
import numpy as np
from scipy.io import wavfile
import librosa
import joblib

# Configuration
MODEL_PATH = "voice_model.pkl"
THRESHOLD = 0.7

def extract_features(file_path):
    """Extract audio features from a WAV file."""
    try:
        # Load audio file
        sample_rate, audio_data = wavfile.read(file_path)
        
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
            
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
        mfccs = np.mean(mfccs.T, axis=0)
        
        return mfccs
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def compare_voice_samples(sample1_path, sample2_path):
    """Compare two voice samples to detect similarity."""
    try:
        features1 = extract_features(sample1_path)
        features2 = extract_features(sample2_path)
        
        if features1 is None or features2 is None:
            return 0.0
            
        # Calculate cosine similarity
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    except Exception as e:
        print(f"Error in voice comparison: {e}")
        return 0.0

def detect_voice_fraud(audio_file_path, known_voice_samples):
    """Detect if an audio file contains fraudulent voice patterns."""
    try:
        # Compare against known good samples
        similarities = []
        for sample_path in known_voice_samples:
            similarity = compare_voice_samples(audio_file_path, sample_path)
            similarities.append(similarity)
            
        # Calculate average similarity score
        avg_similarity = np.mean(similarities) if similarities else 0.0
        
        # If similarity is below threshold, flag as suspicious
        return avg_similarity < (1 - THRESHOLD)
    except Exception as e:
        print(f"Error in fraud detection: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_voice_fraud.py <audio_file_path> [known_voice_sample1] [known_voice_sample2] ...")
        sys.exit(1)
        
    audio_file = sys.argv[1]
    known_samples = sys.argv[2:] if len(sys.argv) > 2 else []
    
    is_fraud = detect_voice_fraud(audio_file, known_samples)
    
    if is_fraud:
        print("ALERT: Potential voice fraud detected!")
        exit(1)
    else:
        print("No fraud detected.")
        exit(0)