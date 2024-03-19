from openai import OpenAI
import os
import csv

# Detect audio files
audio_folder = os.environ.get("AUDIO_FILES_PATH")
if not os.path.exists():
    raise Exception(f"The folder '{audio_folder}' does not exist.")

# Filter .wav files
audio_files = [
    file
    for file in os.listdir(audio_folder)
    if file.endswith(f'.{os.environ.get("AUDIO_FILE_FORMAT")}')
]

print(f"Found {len(audio_files)} audio files in the audio folder")

# Transcribe audio files
client = OpenAI()
transcriptions = []
for audio_file_name in audio_files:
    print(f"Transcribing {audio_file_name}")
    with open(os.path.join(audio_folder, audio_file_name) , "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
          model="whisper-1", 
          file=audio_file
        )
        transcriptions.append({
            "id": audio_file_name,
            "text": transcription.text
        })

# Save transcriptions as csv
print("Saving")
with open(os.environ.get("OUTPUT_FILE_PATH"), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "text"])
        writer.writeheader()
        writer.writerows(transcriptions)
print("Done!")