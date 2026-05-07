from transcriber import transcribe_audio
from question_generator import generate_questions
from text_to_speech import generate_audio_for_questions
from audio_editor import edit_podcast

if __name__ == "__main__":
    transcribe_audio()
    generate_questions()
    generate_audio_for_questions()
    edit_podcast()
    print("Pipeline completed successfully. Podcast episode saved to output/episode_interactive.mp3")
