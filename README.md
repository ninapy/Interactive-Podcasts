# Interactive-Podcasts
Enhanced Listening: Interactive Podcasts. This tool uses AI to transform standard audio files into active learning experiences. It automatically generates and inserts comprehension questions, utilizing active recall to improve retention.

## Files
- `transcriber.py`: transcribes the input podcast using OpenAI's Whisper API. Outputs transcript.json containing the full text and a word-level list with start and end timestamps.

- `question_generator.py`: reads transcript.json and prompts GPT-4o-mini to generate comprehension questions placed coherent points in the podcast. Outputs questions.json with each question, its answer, and the word index after which it should be inserted.

- `text_to_speech.py`: reads questions.json and generates an MP3 audio file for each question using OpenAI's TTS API (tts-1, voice: alloy). Updates questions.json with the path to each generated audio file and the timestamp after which it should be inserted based on the word index provided by question_generator.py.

- `audio_editor.py`: assembles the final podcast by splitting the original audio at each insertion timestamp and adding the question audios. Adds a bell sound before each question, a 6-second silence for the listener to think, and another bell when the pause ends. Outputs the final file to output/episode_interactive.mp3.

- `run_pipeline.py`: runs all four steps in sequence. See usage instructions below.

- `analysis.py` and `visualizations.ipynb`: contains the statistical analysis for the experiment testing the tool's effectiveness on information retention, including ANOVA, t-tests, and performance breakdowns by group and question format and their corresponding visualizations.

## Install Dependencies

run: `pip install -r requirements.txt`

## Configure environment

Create a `.env` file in the root of the project and add you OpenAI API key:

`OPENAI_API_KEY=your_openai_api_key_here`

## Usage

Place your podcast file in the project root and rename it episode.mp3 (or update the filename in the scripts).

Run the full pipeline: `run_pipeline.py`

This will run all four steps in order and output the final file to `output/episode_interactive.mp3`.

Run steps individually:
- `python transcriber.py`
- `python question_generator.py`
- `python text_to_speech.py`
- `python audio_editor.py`



#### Sounds:

Twinkling Stars Sound Effect
https://www.youtube.com/watch?v=okMJSAxfOzc

Ding - Sound Effect
https://www.youtube.com/watch?v=Fu82s5DnhBc
