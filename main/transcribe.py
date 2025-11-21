# transcribe.py

import whisper
from whisper.utils import get_writer
import time
import os
import shutil
from config import INPUT_DIR, OUTPUT_DIR, MODEL_NAME, TRANSCRIPTION_OPTIONS, OUTPUT_FORMAT, WRITER_OPTIONS
from logger import setup_logger, log_info, log_error
from gpuUsage import get_gpu_usage


def transcribe():
    # Setup logger
    setup_logger()
    
    # Create input and output directories if they don't exist
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load the Whisper model
    try:
        model = whisper.load_model(MODEL_NAME)
    except Exception as e:
        log_error(f"Error loading model: {e}")
        exit(1)

    # Loop through audio files in the input directory
    for audio_file in os.listdir(INPUT_DIR):
        log_info(f"Initializing transcription process for {audio_file} ... ")
        audio_file_path = os.path.join(INPUT_DIR, audio_file)

        # Check if the file is an audio file
        if not audio_file.lower().endswith(('.mp3', '.wav', '.m4a')):
            log_info(f"Skipping non-audio file: {audio_file}")
            continue

        # Create a unique output directory based on audio file name, model used and timestamp
        audio_file_name = os.path.splitext(audio_file)[0]
        timestamp = time.strftime("%Y%m%d_%H-%M-%S")
        output_dir = f"{OUTPUT_DIR}/{audio_file_name}_{MODEL_NAME}_{timestamp}"

        # Create output directory
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            log_error(f"Error creating output directory for {audio_file}: {e}")
            continue

        # Get initial GPU usage
        gpu_usage_before = get_gpu_usage()
        log_info(f"Initial GPU Usage for {audio_file}:\n{gpu_usage_before}")

        log_info(f"Starting transcription process for {audio_file} ... ")

        # Start tracking time
        start_time = time.time()

        # Transcribe audio file
        try:
            result = model.transcribe(audio_file_path, **TRANSCRIPTION_OPTIONS)
        except Exception as e:
            log_error(f"Error during transcription of {audio_file}: {e}")
            continue

        # Get GPU usage after transcription
        gpu_usage_after = get_gpu_usage()
        log_info(f"GPU Usage After Transcription for {audio_file}:\n{gpu_usage_after}")

        # Save the output to the specified directory
        output_file_path = f"{output_dir}/"
        try:
            writer = get_writer(OUTPUT_FORMAT, output_file_path)
            writer(result, audio_file, WRITER_OPTIONS)
        except Exception as e:
            log_error(f"Error saving transcription for {audio_file}: {e}")
            continue

        # Move the processed audio file to the output directory
        try:
            shutil.move(audio_file_path, os.path.join(output_dir, audio_file))
        except Exception as e:
            log_error(f"Error moving {audio_file} to output directory: {e}")
            continue

        # Calculate elapsed time and format it
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        formatted_time = f"{minutes} minutes and {seconds} seconds"
        log_info(f"Transcription completed for {audio_file} and saved to {output_file_path}")
        log_info(f"Elapsed Time: {formatted_time}")

        # Move the log file to the output directory
        try:
            shutil.move("./logs/transcription.log", output_dir)
        except Exception as e:
            log_error(f"Error moving transcription log to output directory: {e}")
            continue
