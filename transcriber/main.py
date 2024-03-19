import whisper
# from dotenv import load_dotenv
import os
import csv

# Load .env
# load_dotenv()

# Detect audio files
audio_folder = os.getenv("AUDIO_FILES_PATH")
if not os.path.exists(audio_folder):
    raise Exception(f"The folder '{audio_folder}' does not exist.")

# Filter .wav files
audio_files = [
    file
    for file in os.listdir(audio_folder)
    if file.endswith(f'.{os.getenv("AUDIO_FILE_FORMAT")}')
]

print(f"Found {len(audio_files)} audio files in the audio folder")

# Transcribe audio files
transcriptions = []
model = whisper.load_model("medium", download_root=".cache/whisper")
for audio_file_name in audio_files:
    print("Transcribing", audio_file_name)
    result = model.transcribe(os.path.join(audio_folder, audio_file_name), fp16=False)
    transcriptions.append({
        "id": audio_file_name,
        "text": result["text"]
    })

# Save transcriptions as csv
print("Saving")
with open(os.getenv("OUTPUT_FILE_PATH"), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "text"])
        writer.writeheader()
        writer.writerows(transcriptions)
print("Done!")