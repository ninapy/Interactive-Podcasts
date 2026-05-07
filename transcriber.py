# source: https://developers.openai.com/api/docs/guides/speech-to-text

import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found on .env file")

client = OpenAI()

def transcribe_audio(file_path="episode.mp3"):
    Path("./output/temp_files").mkdir(parents=True, exist_ok=True)
    audio_file = open(file_path, "rb") # read binary

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
        # TODO: prompt="might include prompting later for better results"
    )

    audio_file.close()

    output = {
        "text": transcription.text,
        "words": [
            {"word": w.word, "start": w.start, "end": w.end}
            for w in transcription.words
        ]
    }

    output_file = open("./output/temp_files/transcript.json", "w") # write
    json.dump(output, output_file, indent=2)
    output_file.close()

    print(json.dumps(output["words"], indent=2))

if __name__ == "__main__":
    transcribe_audio()
    