import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found on .env file")

client = OpenAI()

questions_file = open("questions.json", "r")
questions = json.load(questions_file)
questions_file.close()

output_dir = Path("question_audio")
output_dir.mkdir(exist_ok=True) # create folder if it doesn't exist

for i, q in enumerate(questions):
    # text to speak: question + answer
    question_text = f"Take a second to think about this question: {q['question']}"
    # answer_text = f"Great work! The answer is: {q['answer']}"

    # source: https://developeres.openai.com/api/docs/guides/text-to-speech
    # TODO: we might want to change the voice. check: https://www.openai.fm/
    question_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=question_text
        # TODO: instructions="may add instructions later for better results"
    )
    question_path = output_dir / f"question_{i + 1}.mp3"
    question_response.stream_to_file(question_path)

    # generate answer audio
    # answer_response = client.audio.speech.create(
    #     model="tts-1",
    #     voice="alloy",
    #     input=answer_text
    # )
    # answer_path = output_dir / f"answer_{i + 1}.mp3"
    # answer_response.stream_to_file(answer_path)

    q["question_audio_path"] = str(question_path)
    # q["answer_audio_path"] = str(answer_path)
    print(f"Audio generated for question {i + 1}. ")

output_file = open("questions.json", "w")
json.dump(questions, output_file, indent=2)
output_file.close()

print("\nAudio files generated. questions.json updated with audio paths.")
