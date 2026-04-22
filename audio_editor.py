import json
from pathlib import Path
from pydub import AudioSegment

PAUSE_DURATION_MS = 6000  # 6 seconds, in ms
SILENCE = 1000
# TODO: duration pause should be backed up by litterature, if possible

# source: https://github.com/jiaaro/pydub
podcast = AudioSegment.from_mp3("episode.mp3")

questions_file = open("questions.json", "r")
questions = json.load(questions_file)
questions_file.close()

# sort questions by timestamp
questions = sorted(questions, key=lambda q: q["insert_after_timestamp"])

Path("output").mkdir(exist_ok=True)

result = AudioSegment.empty()
curr = 0  # keep track of location on original podcast, in ms

for q in questions:
    end_segment = int(q["insert_after_timestamp"] * 1000)  # convert s to ms

    # add podcast segment up to insertion point
    result += podcast[curr:end_segment]

    # add sound effect before question
    ding = AudioSegment.from_mp3("ding.mp3")
    result += ding

    # add question audio
    question_audio = AudioSegment.from_mp3(q["question_audio_path"])
    result += question_audio

    # add pause for listener to think
    result += AudioSegment.silent(duration=PAUSE_DURATION_MS)

    # add answer audio
    # answer_audio = AudioSegment.from_mp3(q["answer_audio_path"])
    # result += answer_audio

    # add silence after answer
    result += AudioSegment.silent(duration=SILENCE)

    # add sound effect after question
    result += ding

    # move pointer
    curr = end_segment
    print(f"Inserted question at {q['insert_after_timestamp']:.1f}s: {q['question']}")

# add remaining podcast after last question
result += podcast[curr:]

result.export("output/episode_interactive.mp3", format="mp3")
print(f"\nDone. Saved to output/episode_interactive.mp3")
