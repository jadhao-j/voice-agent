#!/usr/bin/env python3
"""
Usage examples for individual modules.
Demonstrates how to use each component programmatically.
"""
from colorama import init, Fore, Style

init(autoreset=True)


def example_audio_recording():
    """Example: Record audio from microphone."""
    print(f"\n{Fore.CYAN}Example: Audio Recording{Style.RESET_ALL}")
    print("-" * 60)

    from audio_recorder import AudioRecorder

    recorder = AudioRecorder()

    # Test microphone
    if not recorder.test_microphone():
        print("Microphone not available")
        return

    # Record audio
    print("\nSpeak for a few seconds...")
    audio_data, sample_rate = recorder.record_audio(duration=10)

    print(f"Recorded {len(audio_data)} samples at {sample_rate} Hz")

    # Optionally save
    # recorder.save_audio(audio_data, "test_recording.wav")


def example_speech_to_text():
    """Example: Transcribe audio file."""
    print(f"\n{Fore.CYAN}Example: Speech-to-Text{Style.RESET_ALL}")
    print("-" * 60)

    from speech_to_text import SpeechToText
    import numpy as np

    stt = SpeechToText()

    # Example with dummy audio (in real use, pass actual audio data)
    audio_data = np.random.randn(16000 * 3).astype(np.float32)  # 3 seconds

    text, language, confidence = stt.transcribe(audio_data)

    print(f"Transcription: {text}")
    print(f"Language: {language}")
    print(f"Confidence: {confidence:.2f}")


def example_language_detection():
    """Example: Detect language from text."""
    print(f"\n{Fore.CYAN}Example: Language Detection{Style.RESET_ALL}")
    print("-" * 60)

    from language_detector import LanguageDetector

    detector = LanguageDetector()

    # Test with different languages
    test_texts = {
        "en": "Hello, how are you today?",
        "hi": "नमस्ते, आप कैसे हैं?",
        "mr": "नमस्कार, तुम्ही कसे आहात?"
    }

    for expected_lang, text in test_texts.items():
        detected_lang, confidence = detector.detect_language(text)
        lang_name = detector.get_language_name(detected_lang)
        print(f"\nText: {text}")
        print(f"Detected: {lang_name} ({detected_lang}) - Confidence: {confidence:.2f}")


def example_llm_agent():
    """Example: Generate responses with LLM agent."""
    print(f"\n{Fore.CYAN}Example: LLM Agent{Style.RESET_ALL}")
    print("-" * 60)

    from llm_agent import LLMAgent

    agent = LLMAgent()

    # Test conversation in different languages
    conversations = [
        ("en", "What is artificial intelligence?"),
        ("hi", "कृत्रिम बुद्धिमत्ता क्या है?"),
        ("mr", "कृत्रिम बुद्धिमत्ता म्हणजे काय?")
    ]

    for language, user_message in conversations:
        print(f"\nUser ({language}): {user_message}")
        response = agent.generate_response(user_message, language)
        print(f"Assistant: {response}")


def example_text_to_speech():
    """Example: Convert text to speech."""
    print(f"\n{Fore.CYAN}Example: Text-to-Speech{Style.RESET_ALL}")
    print("-" * 60)

    from text_to_speech import TextToSpeech

    tts = TextToSpeech()

    # Test TTS in different languages
    test_messages = {
        "en": "This is a test of the text to speech system.",
        "hi": "यह टेक्स्ट टू स्पीच सिस्टम का परीक्षण है।",
        "mr": "ही मजकूर ते भाषण प्रणालीची चाचणी आहे."
    }

    print("\nTesting TTS in multiple languages...")
    print("Audio will play for each language.\n")

    for language, text in test_messages.items():
        print(f"Language: {language}")
        print(f"Text: {text}")

        # Synthesize and play
        success = tts.synthesize_and_play(text, language)

        if success:
            print(f"{Fore.GREEN}✓ Success{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}✗ Failed{Style.RESET_ALL}\n")

    # Cleanup
    tts.cleanup_temp_files()


def example_full_pipeline():
    """Example: Complete pipeline from recording to response."""
    print(f"\n{Fore.CYAN}Example: Full Pipeline{Style.RESET_ALL}")
    print("-" * 60)

    from audio_recorder import AudioRecorder
    from speech_to_text import SpeechToText
    from language_detector import LanguageDetector
    from llm_agent import LLMAgent
    from text_to_speech import TextToSpeech

    # Initialize components
    recorder = AudioRecorder()
    stt = SpeechToText()
    detector = LanguageDetector()
    agent = LLMAgent()
    tts = TextToSpeech()

    print("\n1. Recording audio...")
    audio_data, sample_rate = recorder.record_audio(duration=10)

    if len(audio_data) == 0:
        print("No audio recorded")
        return

    print("\n2. Transcribing speech...")
    text, whisper_lang, whisper_conf = stt.transcribe(audio_data, sample_rate)

    if not text:
        print("No speech detected")
        return

    print(f"Transcription: {text}")

    print("\n3. Detecting language...")
    language, confidence = detector.validate_and_correct(whisper_lang, whisper_conf, text)
    print(f"Language: {language} (confidence: {confidence:.2f})")

    print("\n4. Generating response...")
    response = agent.generate_response(text, language)
    print(f"Response: {response}")

    print("\n5. Converting to speech...")
    tts.synthesize_and_play(response, language)

    print(f"\n{Fore.GREEN}✓ Pipeline complete{Style.RESET_ALL}")


def main():
    """Run example demonstrations."""
    print(f"\n{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Voice Assistant - Usage Examples{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")

    examples = [
        ("1", "Audio Recording", example_audio_recording),
        ("2", "Speech-to-Text", example_speech_to_text),
        ("3", "Language Detection", example_language_detection),
        ("4", "LLM Agent", example_llm_agent),
        ("5", "Text-to-Speech", example_text_to_speech),
        ("6", "Full Pipeline", example_full_pipeline),
    ]

    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")

    print(f"\n  0. Run all examples")
    print(f"  q. Quit")

    while True:
        choice = input(f"\n{Fore.YELLOW}Select an example (0-6, q): {Style.RESET_ALL}").strip()

        if choice.lower() == 'q':
            break
        elif choice == '0':
            for num, name, func in examples:
                try:
                    func()
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Skipped{Style.RESET_ALL}")
                except Exception as e:
                    print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
            break
        else:
            for num, name, func in examples:
                if choice == num:
                    try:
                        func()
                    except KeyboardInterrupt:
                        print(f"\n{Fore.YELLOW}Interrupted{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
                    break
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
