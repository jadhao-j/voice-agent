#!/usr/bin/env python3
"""
Real-time Multilingual Voice Assistant
Main application entry point.
"""
import sys
import signal
from colorama import init, Fore, Style

from config import Config
from audio_recorder import AudioRecorder
from speech_to_text import SpeechToText
from language_detector import LanguageDetector
from llm_agent import LLMAgent
from text_to_speech import TextToSpeech


class VoiceAssistant:
    """Main voice assistant orchestrator."""

    def __init__(self):
        """Initialize all components of the voice assistant."""
        init(autoreset=True)  # Initialize colorama

        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🤖 Multilingual Voice Assistant{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

        # Setup directories
        Config.setup_directories()

        # Initialize components
        print(f"{Fore.YELLOW}Initializing components...{Style.RESET_ALL}\n")

        try:
            self.audio_recorder = AudioRecorder()
            self.speech_to_text = SpeechToText()
            self.language_detector = LanguageDetector()
            self.llm_agent = LLMAgent()
            self.tts = TextToSpeech()

            print(f"\n{Fore.GREEN}✓ All components initialized successfully{Style.RESET_ALL}\n")

        except Exception as e:
            print(f"\n{Fore.RED}✗ Failed to initialize components: {e}{Style.RESET_ALL}")
            sys.exit(1)

        # State
        self.running = False
        self.current_language = "en"

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print(f"\n\n{Fore.YELLOW}Shutting down...{Style.RESET_ALL}")
        self.stop()
        sys.exit(0)

    def start(self):
        """Start the voice assistant."""
        self.running = True

        # Test microphone
        if not self.audio_recorder.test_microphone():
            print(f"{Fore.RED}Microphone test failed. Please check your audio settings.{Style.RESET_ALL}")
            return

        # Display greeting
        self._display_welcome()

        # Speak greeting
        greeting = Config.GREETINGS.get(self.current_language, Config.GREETINGS["en"])
        self.tts.synthesize_and_play(greeting, self.current_language)

        # Main conversation loop
        self._conversation_loop()

    def _display_welcome(self):
        """Display welcome message and instructions."""
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Supported Languages:{Style.RESET_ALL}")
        for code, info in Config.SUPPORTED_LANGUAGES.items():
            print(f"  • {info['name']} ({code})")

        print(f"\n{Fore.YELLOW}Instructions:{Style.RESET_ALL}")
        print(f"  • Speak naturally in any supported language")
        print(f"  • The assistant will detect your language automatically")
        print(f"  • Say 'exit', 'quit', or 'goodbye' to stop")
        print(f"  • Press Ctrl+C to force quit\n")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    def _conversation_loop(self):
        """Main conversation loop."""
        turn_count = 0

        while self.running:
            try:
                turn_count += 1
                print(f"\n{Fore.MAGENTA}{'─' * 60}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Turn {turn_count}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{'─' * 60}{Style.RESET_ALL}\n")

                # Step 1: Record audio
                audio_data, sample_rate = self.audio_recorder.record_audio()

                if len(audio_data) == 0:
                    print(f"{Fore.YELLOW}No audio captured. Please try again.{Style.RESET_ALL}")
                    continue

                # Step 2: Speech to text
                transcription, whisper_lang, whisper_confidence = self.speech_to_text.transcribe(
                    audio_data,
                    sample_rate
                )

                if not transcription:
                    print(f"{Fore.YELLOW}No speech detected. Please try again.{Style.RESET_ALL}")
                    continue

                # Step 3: Language detection (validation)
                detected_language, final_confidence = self.language_detector.validate_and_correct(
                    whisper_lang,
                    whisper_confidence,
                    transcription
                )

                self.current_language = detected_language
                lang_name = self.language_detector.get_language_name(detected_language)

                print(f"\n{Fore.CYAN}📢 You ({lang_name}): {Fore.WHITE}{transcription}{Style.RESET_ALL}")

                # Check for exit commands
                if self._is_exit_command(transcription, detected_language):
                    self._say_goodbye()
                    break

                # Step 4: Generate response
                response = self.llm_agent.generate_response(transcription, detected_language)

                if not response:
                    response = "I'm sorry, I couldn't generate a response."

                print(f"{Fore.GREEN}🤖 Assistant ({lang_name}): {Fore.WHITE}{response}{Style.RESET_ALL}\n")

                # Step 5: Text to speech
                self.tts.synthesize_and_play(response, detected_language)

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error in conversation loop: {e}{Style.RESET_ALL}")
                continue

    def _is_exit_command(self, text: str, language: str) -> bool:
        """
        Check if the text contains an exit command.

        Args:
            text: Input text to check
            language: Language of the text

        Returns:
            True if exit command detected, False otherwise
        """
        text_lower = text.lower().strip()

        # Check exit commands for the detected language
        exit_commands = Config.EXIT_COMMANDS.get(language, Config.EXIT_COMMANDS["en"])

        for command in exit_commands:
            if command in text_lower:
                return True

        # Also check English exit commands as fallback
        if language != "en":
            for command in Config.EXIT_COMMANDS["en"]:
                if command in text_lower:
                    return True

        return False

    def _say_goodbye(self):
        """Say goodbye in the current language."""
        goodbyes = {
            "en": "Goodbye! Have a great day!",
            "hi": "अलविदा! आपका दिन शुभ हो!",
            "mr": "निरोप! तुमचा दिवस चांगला जावो!"
        }

        goodbye_message = goodbyes.get(self.current_language, goodbyes["en"])
        print(f"\n{Fore.GREEN}{goodbye_message}{Style.RESET_ALL}\n")

        self.tts.synthesize_and_play(goodbye_message, self.current_language)

    def stop(self):
        """Stop the voice assistant and cleanup."""
        self.running = False

        # Cleanup
        if hasattr(self, 'tts'):
            self.tts.cleanup_temp_files()

        print(f"{Fore.CYAN}Voice assistant stopped.{Style.RESET_ALL}")


def main():
    """Main entry point."""
    try:
        assistant = VoiceAssistant()
        assistant.start()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
