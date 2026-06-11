# local_ai_voice_trainer.py
import os
from pydub import AudioSegment
from tracker_web import log_app_usage

def slice_audio_source(file_path: str, output_dir: str, chunk_length_ms: int = 5000):
    """
    Split a long audio file into small chunks (e.g., 5 seconds) for RVC training.
    """
    print(f"[INFO] Accessing source file: {file_path}")
    
    # Track button click or function execution with JSON details
    log_app_usage(
        "local_ai_voice_trainer", 
        "audio_slicing_started", 
        {"source_file": file_path, "chunk_size_ms": chunk_length_ms}
    )

    if not os.path.exists(file_path):
        print("[ERROR] Source audio file not found.")
        return False

    os.makedirs(output_dir, exist_ok=True)
    
    # Load and slice the audio using pydub
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    for idx, chunk in enumerate(chunks):
        chunk_output_path = os.path.join(output_dir, f"slice_{idx:03d}.wav")
        # Export as WAV format which is preferred by Applio/RVC
        chunk.export(chunk_output_path, format="wav")

    print(f"[SUCCESS] Generated {len(chunks)} audio slices in: {output_dir}")
    
    # Track successful completion
    log_app_usage(
        "local_ai_voice_trainer", 
        "audio_slicing_completed", 
        {"total_slices": len(chunks)}
    )
    return True

if __name__ == "__main__":
    # Define default path settings matching the project structure
    SRC_FILE = "dataset/raw_source/The_Residence.m4a"
    OUT_DIR = "dataset/clipchamp_slices"
    
    slice_audio_source(SRC_FILE, OUT_DIR)