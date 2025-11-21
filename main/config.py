# config.py

# Input and output directories
INPUT_DIR = "./input_audio"
OUTPUT_DIR = "./transcripts"

# Whisper model to use
MODEL_NAME = "large-v3"

# Transcription options
TRANSCRIPTION_OPTIONS = {
    # Core
    "language": "English", # Target language (auto-detected if None)
    "task": "transcribe", # "transcribe" for same-language output, "translate" for English output
    "initial_prompt": "This is a Court Proceeding.", # Custom vocabulary or context prompt ie Relevant context about the audio content.
    "carry_initial_prompt": True, # Persistent Prompting. Helps remind the AI as to what it is doing to avoid hallucinations.
    "verbose": True, # Controls progress display (True, False, or None). Verbose is not indicative of the transcription output.

    # Quality Control
    "word_timestamps": True, # Enabled for Hallucination Threshold and Writer Options.
    "temperature": 0.0, # Sampling randomness (0.0 = deterministic). (0.0, 0.2, 0.4, 0.6) For Fallback temperatures.
    "beam_size": 5, # Number of beams for beam search (when temperature = 0.0). Keeping lower helps with speed and to be more deterministic.
    "patience": 2.0, # Beam search parameter that controls how many candidate sequences are maintained during decoding.
    "condition_on_previous_text": False, # Prevents repetition loops/hallucinations.
    "compression_ratio_threshold": 2.0, # Detect repetitive output (default: 2.4). Lower value to be more strict. Below 1.8 is too aggressive.
    "logprob_threshold": -0.5, # Detect low-confidence output (default: -1.0) Higher value to reject low-confidence segments.
    "no_speech_threshold": 0.6, # Detect silent segments (default: 0.6).
    "hallucination_silence_threshold": 2.0 # Skip silent periods in word timestamps.
}

# Output format to use
OUTPUT_FORMAT = "all" # "txt", "vtt", "srt", "tsv", "json", "all"

# Output format parameters
# Set to compare accuracy between runs.
WRITER_OPTIONS = {
    "max_line_width": 100,
    "max_line_count": 1,
    "max_words_per_line": 19 # 0 inclusive
}