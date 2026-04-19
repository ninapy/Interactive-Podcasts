import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found on .env file")

client = OpenAI()

transcript_file = open("transcript.json", "r")
transcript = json.load(transcript_file)
transcript_file.close()

full_text = transcript["text"]
words = transcript["words"]

# prompt for the llm
NUMBER_OF_QUESTIONS = 2

prompt = f"""
You are helping create an interactive podcast experience.
Given the transcript below, generate exactly {NUMBER_OF_QUESTIONS} comprehension questions.

Each question should:
- Test knowledge of one specific fact, term, or number from the podcast
- Be short answer or multiple choice
- Be inserted AFTER the content it tests has been explained
- Have a clear, concise answer (one word or short phrase)

For placement: pick a word index (from the transcript word list) after which the question should be inserted.
Choose a natural pause point, ideally the end of a sentence or topic, and after the relevant content has been covered.
Split the podcast roughly in thirds: place one question around the 1/3 mark and one around the 2/3 mark.

Respond ONLY with valid JSON in this format:
[
  {{
    "question": "...",
    "answer": "...",
    "insert_after_word_index": <int>
  }},
  {{
    "question": "...",
    "answer": "...",
    "insert_after_word_index": <int>
  }}
]

Transcript:
{full_text}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
)

raw = response.choices[0].message.content # get text from llm response
questions = json.loads(raw)

# source: https://stackoverflow.com/questions/49490696/finding-key-using-next-and-iter
if isinstance(questions, dict): # unwrap if questions list is wrapped in a dict e.g. {"questions": [...]}
    questions = next(iter(questions.values()))

# convert word index into timestamp
for q in questions:
    idx = q["insert_after_word_index"] # get word index to insert question after
    q["insert_after_timestamp"] = words[idx]["end"] # add timestamp for when to insert question, from original transcript

output_file = open("questions.json", "w")
json.dump(questions, output_file, indent=2)
output_file.close()

print(json.dumps(questions, indent=2))
