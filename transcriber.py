# source: https://developers.openai.com/api/docs/guides/speech-to-text

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found on .env file")

client = OpenAI()
audio_file = open("episode.mp3", "rb") # read binary

transcription = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["word"]
    # TODO: prompt="might include prompting later for better results"
)

output = {
    "text": transcription.text,
    "words": [
        {"word": w.word, "start": w.start, "end": w.end}
        for w in transcription.words
    ]
}

output_file = open("transcript.json", "w") # write
json.dump(output, output_file, indent=2)
output_file.close()

print(json.dumps(transcription.words, indent=2))
