import whisper
from dotenv import load_dotenv
import os
import csv

# Load .env
load_dotenv()

# Consts
OUTPUT_FILE_PATH = os.getenv("OUTPUT_FILE_PATH")
AUDIO_FILE_FORMAT = os.getenv("AUDIO_FILE_FORMAT")
AUDIO_FILES_PATH = os.getenv("AUDIO_FILES_PATH")
WHISPER_MODEL = os.getenv("WHISPER_MODEL")

# Read existing transcriptions
transcriptions = []
if os.path.exists(OUTPUT_FILE_PATH):
    with open(OUTPUT_FILE_PATH, 'r') as file:
        csv_reader = csv.DictReader(file)
        transcriptions = [row for row in csv_reader]

existing_transcriptions_ids = [transcription["id"] for transcription in transcriptions]

# Detect audio files
if not os.path.exists(AUDIO_FILES_PATH):
    raise Exception(f"The folder '{AUDIO_FILES_PATH}' does not exist.")

# Filter audio files
audio_files = [
    file
    for file in os.listdir(AUDIO_FILES_PATH)
    if file.endswith(f'.{AUDIO_FILE_FORMAT}')
    and file not in existing_transcriptions_ids
]
print(f"Found {len(audio_files)} new audio files in the audio folder")

# Transcribe audio files
def transcribe():
    print(f"Loading model: whisper {WHISPER_MODEL}")
    model = whisper.load_model(WHISPER_MODEL, download_root=".cache/whisper")
    for audio_file_name in audio_files:
        print("Transcribing", audio_file_name)
        result = model.transcribe(os.path.join(AUDIO_FILES_PATH, audio_file_name), fp16=False)
        transcriptions.append({
            "id": audio_file_name,
            "text": result["text"]
        })

    # Save transcriptions as csv
    print("Saving")
    with open(OUTPUT_FILE_PATH, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "text"])
        writer.writeheader()
        writer.writerows(transcriptions)
    print("Done")

if (len(audio_files) > 0):
    transcribe()
else:
    print("No new audio files to transcribe.")

