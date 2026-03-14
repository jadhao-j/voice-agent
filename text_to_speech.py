"""
Text-to-speech module with multiple TTS engine support.
Supports both Coqui TTS (Python 3.9-3.11) and pyttsx3 (all Python versions).
"""
import os
import tempfile
from pathlib import Path
from typing import Optional
from colorama import Fore, Style
import sounddevice as sd
import numpy as np

from config import Config


class TextToSpeech:
    """Handles text-to-speech conversion using available TTS engines."""

    def __init__(self):
        """Initialize the TTS engine."""
        print(f"{Fore.CYAN}Initializing TTS engine...{Style.RESET_ALL}")

        self.engine_type = None

        # Try to load Coqui TTS first (better quality)
        try:
            from TTS.api import TTS
            print(f"{Fore.YELLOW}Loading Coqui TTS model (this may take a moment)...{Style.RESET_ALL}")
            self.tts = TTS(Config.TTS_MODEL_NAME)
            self.engine_type = "coqui"
            self.available_languages = self._get_coqui_languages()
            print(f"{Fore.GREEN}✓ Coqui TTS loaded successfully{Style.RESET_ALL}")
            return
        except ImportError:
            print(f"{Fore.YELLOW}Coqui TTS not available (requires Python 3.9-3.11){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}Coqui TTS error: {e}{Style.RESET_ALL}")

        # Fallback to pyttsx3 (works with all Python versions)
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine_type = "pyttsx3"

            # Configure pyttsx3
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level

            # Get available voices
            self.voices = self.engine.getProperty('voices')
            self.available_languages = ["en", "hi", "mr"]  # pyttsx3 supports system voices

            print(f"{Fore.GREEN}✓ pyttsx3 TTS engine loaded{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Available voices: {len(self.voices)}{Style.RESET_ALL}")
            return
        except ImportError:
            print(f"{Fore.RED}pyttsx3 not installed!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}pyttsx3 error: {e}{Style.RESET_ALL}")

        # If both fail
        print(f"{Fore.RED}No TTS engine available! Install pyttsx3 or TTS.{Style.RESET_ALL}")
        self.engine_type = None

    def _get_coqui_languages(self) -> list:
        """Get list of available languages for Coqui TTS."""
        try:
            if hasattr(self.tts, 'languages'):
                return self.tts.languages
            return ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hi"]
        except:
            return ["en", "hi"]

    def synthesize(
        self,
        text: str,
        language: str = "en",
        speaker_wav: Optional[str] = None,
        play_audio: bool = True
    ) -> Optional[str]:
        """
        Convert text to speech and optionally play it.

        Args:
            text: Text to convert to speech
            language: Language code for TTS
            speaker_wav: Path to reference audio for voice cloning (Coqui only)
            play_audio: Whether to play the audio immediately

        Returns:
            Path to the generated audio file (Coqui) or None (pyttsx3)
        """
        if not text or not text.strip():
            print(f"{Fore.YELLOW}No text to synthesize{Style.RESET_ALL}")
            return None

        if self.engine_type is None:
            print(f"{Fore.RED}No TTS engine available{Style.RESET_ALL}")
            return None

        print(f"{Fore.CYAN}Synthesizing speech...{Style.RESET_ALL}")

        try:
            if self.engine_type == "coqui":
                return self._synthesize_coqui(text, language, speaker_wav, play_audio)
            elif self.engine_type == "pyttsx3":
                return self._synthesize_pyttsx3(text, language, play_audio)
        except Exception as e:
            print(f"{Fore.RED}Error during TTS synthesis: {e}{Style.RESET_ALL}")
            return None

    def _synthesize_coqui(
        self,
        text: str,
        language: str,
        speaker_wav: Optional[str],
        play_audio: bool
    ) -> Optional[str]:
        """Synthesize using Coqui TTS."""
        # Map language to TTS language code
        tts_language = Config.TTS_LANGUAGE_MAP.get(language, "en")

        # Check if language is available
        if tts_language not in self.available_languages:
            print(f"{Fore.YELLOW}Language {tts_language} not available, using English{Style.RESET_ALL}")
            tts_language = "en"

        # Create temp directory
        Config.TEMP_DIR.mkdir(exist_ok=True)
        output_path = Config.TEMP_DIR / f"response_{os.getpid()}.wav"

        # Generate audio
        if speaker_wav and os.path.exists(speaker_wav):
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=tts_language,
                file_path=str(output_path)
            )
        else:
            self.tts.tts_to_file(
                text=text,
                language=tts_language,
                file_path=str(output_path)
            )

        print(f"{Fore.GREEN}✓ Speech synthesized{Style.RESET_ALL}")

        if play_audio:
            self.play_audio(str(output_path))

        return str(output_path)

    def _synthesize_pyttsx3(
        self,
        text: str,
        language: str,
        play_audio: bool
    ) -> None:
        """Synthesize using pyttsx3."""
        # Try to select appropriate voice for language
        voice_selected = False

        # Voice mapping for common languages
        language_keywords = {
            "hi": ["hindi", "hi"],
            "mr": ["marathi", "mr"],
            "en": ["english", "en", "us", "uk"]
        }

        keywords = language_keywords.get(language, ["english"])

        # Try to find matching voice
        for voice in self.voices:
            voice_name_lower = voice.name.lower()
            voice_id_lower = voice.id.lower()

            for keyword in keywords:
                if keyword in voice_name_lower or keyword in voice_id_lower:
                    self.engine.setProperty('voice', voice.id)
                    voice_selected = True
                    break

            if voice_selected:
                break

        # If no specific voice found, use default
        if not voice_selected and len(self.voices) > 0:
            self.engine.setProperty('voice', self.voices[0].id)

        print(f"{Fore.GREEN}✓ Speech synthesized{Style.RESET_ALL}")

        if play_audio:
            print(f"{Fore.GREEN}🔊 Playing response...{Style.RESET_ALL}")
            self.engine.say(text)
            self.engine.runAndWait()
            print(f"{Fore.GREEN}✓ Audio playback complete{Style.RESET_ALL}")

        return None

    def play_audio(self, audio_path: str):
        """
        Play audio file through speakers.

        Args:
            audio_path: Path to the audio file
        """
        try:
            from scipy.io import wavfile

            print(f"{Fore.GREEN}🔊 Playing response...{Style.RESET_ALL}")

            # Read the audio file
            sample_rate, audio_data = wavfile.read(audio_path)

            # Ensure audio is in the correct format
            if audio_data.dtype == np.int16:
                audio_data = audio_data.astype(np.float32) / 32768.0
            elif audio_data.dtype == np.int32:
                audio_data = audio_data.astype(np.float32) / 2147483648.0

            # Play the audio
            sd.play(audio_data, sample_rate)
            sd.wait()

            print(f"{Fore.GREEN}✓ Audio playback complete{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error playing audio: {e}{Style.RESET_ALL}")

    def synthesize_and_play(self, text: str, language: str = "en") -> bool:
        """
        Synthesize text to speech and play it immediately.

        Args:
            text: Text to convert to speech
            language: Language code

        Returns:
            True if successful, False otherwise
        """
        result = self.synthesize(text, language, play_audio=True)
        return result is not None or self.engine_type == "pyttsx3"

    def cleanup_temp_files(self):
        """Remove temporary audio files."""
        if self.engine_type != "coqui":
            return

        try:
            if Config.TEMP_DIR.exists():
                for file in Config.TEMP_DIR.glob("response_*.wav"):
                    file.unlink()
                print(f"{Fore.CYAN}Temporary files cleaned{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}Error cleaning temp files: {e}{Style.RESET_ALL}")

    def test_tts(self, language: str = "en"):
        """
        Test TTS functionality.

        Args:
            language: Language code to test
        """
        test_messages = {
            "en": "Hello, this is a test of the text to speech system.",
            "hi": "नमस्ते, यह टेक्स्ट टू स्पीच सिस्टम का परीक्षण है।",
            "mr": "नमस्कार, ही मजकूर ते भाषण प्रणालीची चाचणी आहे."
        }

        test_text = test_messages.get(language, test_messages["en"])
        print(f"{Fore.CYAN}Testing TTS with: {test_text}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Using engine: {self.engine_type}{Style.RESET_ALL}")

        success = self.synthesize_and_play(test_text, language)

        if success:
            print(f"{Fore.GREEN}✓ TTS test successful{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ TTS test failed{Style.RESET_ALL}")

        return success
