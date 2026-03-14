"""
Speech-to-text module using Faster-Whisper.
"""
import numpy as np
from faster_whisper import WhisperModel
from typing import Tuple, Optional
from colorama import Fore, Style

from config import Config


class SpeechToText:
    """Handles speech-to-text conversion using Faster-Whisper."""

    def __init__(self):
        """Initialize the Faster-Whisper model."""
        print(f"{Fore.CYAN}Loading Whisper model ({Config.WHISPER_MODEL_SIZE})...{Style.RESET_ALL}")

        try:
            self.model = WhisperModel(
                Config.WHISPER_MODEL_SIZE,
                device=Config.WHISPER_DEVICE,
                compute_type=Config.WHISPER_COMPUTE_TYPE,
                download_root=str(Config.MODELS_DIR)
            )
            print(f"{Fore.GREEN}✓ Whisper model loaded successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error loading Whisper model: {e}{Style.RESET_ALL}")
            raise

    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Tuple[str, str, float]:
        """
        Transcribe audio to text with automatic language detection.

        Args:
            audio_data: Audio samples as numpy array
            sample_rate: Audio sample rate

        Returns:
            Tuple of (transcribed text, detected language code, confidence)
        """
        if len(audio_data) == 0:
            return "", "en", 0.0

        try:
            # Ensure audio is in the correct format
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)

            # Normalize audio
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))

            print(f"{Fore.CYAN}Transcribing audio...{Style.RESET_ALL}")

            # Transcribe with language detection
            segments, info = self.model.transcribe(
                audio_data,
                beam_size=5,
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    threshold=0.5
                )
            )

            # Extract text from segments
            transcription = " ".join([segment.text for segment in segments]).strip()

            detected_language = info.language
            language_probability = info.language_probability

            if transcription:
                print(f"{Fore.GREEN}✓ Transcription: {transcription}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Language: {detected_language} (confidence: {language_probability:.2f}){Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No speech detected{Style.RESET_ALL}")

            return transcription, detected_language, language_probability

        except Exception as e:
            print(f"{Fore.RED}Error during transcription: {e}{Style.RESET_ALL}")
            return "", "en", 0.0

    def transcribe_file(self, audio_path: str) -> Tuple[str, str, float]:
        """
        Transcribe audio from a file.

        Args:
            audio_path: Path to the audio file

        Returns:
            Tuple of (transcribed text, detected language code, confidence)
        """
        try:
            segments, info = self.model.transcribe(
                audio_path,
                beam_size=5,
                vad_filter=True
            )

            transcription = " ".join([segment.text for segment in segments]).strip()
            return transcription, info.language, info.language_probability

        except Exception as e:
            print(f"{Fore.RED}Error transcribing file: {e}{Style.RESET_ALL}")
            return "", "en", 0.0

    def get_supported_languages(self) -> list:
        """
        Get list of supported languages.

        Returns:
            List of language codes
        """
        return list(Config.SUPPORTED_LANGUAGES.keys())

    def validate_language(self, language_code: str) -> bool:
        """
        Check if a language is supported.

        Args:
            language_code: Two-letter language code

        Returns:
            True if language is supported, False otherwise
        """
        return language_code in Config.SUPPORTED_LANGUAGES
