import os
from pathlib import Path
from pydub import AudioSegment
from typing import List, Union
from logger import CustomLogger

log = CustomLogger("CombineAudio", log_file="combine_audio.log")

def combine_audio_files(input_files: List[Union[str, Path]], output_file: Union[str, Path]) -> str:
    """
    Combine multiple audio files into a single MP3 file.
    
    Args:
        input_files: List of paths to input audio files
        output_file: Path where the combined audio should be saved
    """
    log.log_debug("Starting audio combination process...")
    
    # Convert all paths to Path objects
    input_files = [Path(f) for f in input_files]
    output_file = Path(output_file)
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Initialize an empty AudioSegment
    log.log_debug("Initializing an empty AudioSegment...")
    combined = AudioSegment.empty()

    # Iterate through the input files
    for file_path in input_files:
        try:
            log.log_debug(f"Processing file: {file_path}")
            
            # Load the audio file (handle both wav and mp3)
            if file_path.suffix.lower() == '.wav':
                audio = AudioSegment.from_wav(str(file_path))
            elif file_path.suffix.lower() == '.mp3':
                audio = AudioSegment.from_mp3(str(file_path))
            else:
                log.log_warning(f"Unsupported file format: {file_path}")
                continue

            # Add it to the combined AudioSegment
            combined += audio
            log.log_debug(f"Added: {file_path}")
            
        except Exception as e:
            log.log_error(f"Error processing {file_path}: {str(e)}")
            continue

    if len(combined) == 0:
        raise ValueError("No audio files were successfully combined")

    # Export the combined audio to a file
    log.log_debug(f"Exporting combined audio to {output_file}...")
    combined.export(str(output_file), format="mp3")
    log.log_debug(f"Combined audio saved as: {output_file}")

    return str(output_file)