import os
import azure.cognitiveservices.speech as speechsdk
import time
from pathlib import Path
from dotenv import load_dotenv
from pydub import AudioSegment

from logger import CustomLogger

log = CustomLogger("SpeechGenerator", log_file="speech_generator.log")

load_dotenv()

# Azure Speech Service configuration
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")


speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)


def create_speech(text, voice, output_file):
    if not text.strip():
        log.log_warning(f"Warning: Empty text for {output_file}. Skipping this segment.")
        return

    try:
        speech_config.speech_synthesis_voice_name = voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=None)
        
        
        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
            with open(output_file, "wb") as audio_file:
                audio_file.write(audio_data)
            log.log_debug(f"Audio saved to {output_file}")
        else:
            log.log_error(f"Error synthesizing speech for {output_file}: {result.reason}")

    except Exception as e:
        log.log_error(f"Error creating speech for {output_file}: {str(e)}")
        log.log_error(f"Problematic text: '{text}'")


def create_speech_from_ssml(ssml, output_file):
    try:
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=None)
        
        log.log_debug(ssml)
        result = speech_synthesizer.speak_ssml_async(ssml).get()
        log.log_debug(result)

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
            with open(output_file, "wb") as audio_file:
                audio_file.write(audio_data)
            log.log_debug(f"Audio saved to {output_file}")
            return output_file
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            log.log_debug(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                log.log_debug(f"Error details: {cancellation_details.error_details}")
        else:
            log.log_error(f"Error synthesizing speech for {output_file}: {result.reason}")
            return None

    except Exception as e:
        log.log_error(f"Error creating speech for {output_file}: {str(e)}")
        log.log_error(f"Problematic SSML: '{ssml[:100]}...'")  # log.log_debug first 100 characters of SSML for debugging
        return None

def convert_wav_to_mp3(wav_file: Path, mp3_file: Path):
    try:
        audio = AudioSegment.from_wav(str(wav_file))
        audio.export(str(mp3_file), format="mp3")
        log.log_debug(f"Converted {wav_file} to {mp3_file}")
        return mp3_file
    except Exception as e:
        log.log_error(f"Error converting WAV to MP3: {str(e)}")
        return None

# async def text_to_speech(script: str, output_path: Path) -> tuple:
    # Convert the entire script to SSML
    # full_ssml = markdown_to_ssml(script)

    # # remove asterisks
    # full_ssml = full_ssml.replace('*', '')

    # wav_file = output_path / "full_script.wav"
    # mp3_file = output_path / "full_script.mp3"

    # wav_result = create_speech_from_ssml(full_ssml, wav_file)
    
    # if wav_result:
    #     mp3_result = convert_wav_to_mp3(wav_file, mp3_file)
    #     if mp3_result:
    #         log.log_debug(f"Processed full script and saved to {mp3_file}")
    #         os.remove(wav_file)  # Remove the temporary WAV file
    #         return full_ssml, mp3_file
    #     else:
    #         return full_ssml, wav_file  # Return WAV file if MP3 conversion fails
    # else:
    #     return full_ssml, None

async def text_to_speech(script: str, output_path: str):
    # Convert output_path to Path object
    output_path = Path(output_path)
    
    # Make sure the directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Split the script into lines
    lines = script.split('\n')

    # Initialize variables
    current_speaker = ""
    current_text = ""
    audio_segments = []
    line_number = 0

    for line in lines:
        line_number += 1
        line = line.strip()

        # Check for speaker lines in both formats
        if ':' in line and (line.startswith('**') or any(name in line.split(':')[0] for name in ['Alex', 'Jane'])):
            # New speaker
            if current_speaker and current_text.strip():
                audio_segments.append(
                    (current_speaker, current_text.strip(), line_number - 1))
            current_speaker = line.split(':')[0].strip('* ')
            current_text = line.split(':', 1)[1].strip() + " "
        elif line and not line.startswith('[') and not line.startswith('#'):
            current_text += line + " "

    # Add the last segment
    if current_speaker and current_text.strip():
        audio_segments.append(
            (current_speaker, current_text.strip(), line_number))

    # Create audio files for each segment
    temp_segments = []
    for i, (speaker, text, line_number) in enumerate(audio_segments):
        if 'Alex' in speaker:
            voice = "en-US-AndrewMultilingualNeural"
        elif 'Jane' in speaker:
            voice = "en-US-AvaMultilingualNeural"
        else:
            voice = "en-US-BrandonMultilingualNeural"  # Default voice

        clean_text = text.strip()

        if not clean_text:
            log.log_debug(f"Warning: Empty cleaned text for segment {i} (starting at line {line_number}). Original text: '{text}'")
            continue

        # Create segment filename using parent directory of output_path
        segment_file = output_path.parent / f"segment_{i:03d}.wav"
        create_speech(clean_text, voice, str(segment_file))
        temp_segments.append(segment_file)
        log.log_debug(f"Created {segment_file} for {speaker}: {clean_text[:50]}...")

        # Add a short pause between segments
        time.sleep(0.5)

    log.log_debug(f"Processed {len(audio_segments)} segments.")
    return output_path

# Example usage:
# output_path = Path("path/to/output/directory")
# await text_to_speech(your_script, output_path)