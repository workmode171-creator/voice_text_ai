
import speech_recognition as sr
import io


def transcribe_audio(audio_bytes, language="en-US"):
    recognizer = sr.Recognizer()

    try:
        audio_file = io.BytesIO(audio_bytes)
        results = []

        with sr.AudioFile(audio_file) as source:
            # Read long recordings in smaller sections
            while True:
                audio = source.record(
                    duration=25
                )

                if not audio.frame_data:
                    break

                try:
                    text = recognizer.recognize_google(
                        audio,
                        language=language
                    )

                    if text.strip():
                        results.append(text.strip())

                except sr.UnknownValueError:
                    # Skip sections that cannot be understood
                    continue

        if results:
            return " ".join(results)

        return "Sorry, no clear speech was detected. Please record again."

    except sr.RequestError:
        return (
            "Internet or Google Speech Recognition "
            "service error. Please try again."
        )

    except Exception as e:
        return f"Error: {str(e)}"

