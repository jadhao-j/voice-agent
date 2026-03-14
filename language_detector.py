"""
Language detection module with fallback support.
"""
from langdetect import detect, detect_langs, LangDetectException
from typing import Tuple, Optional
from colorama import Fore, Style

from config import Config


class LanguageDetector:
    """Handles language detection and validation."""

    def __init__(self):
        """Initialize the language detector."""
        self.supported_languages = Config.SUPPORTED_LANGUAGES
        self.confidence_threshold = Config.LANG_DETECT_CONFIDENCE

    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language from text with confidence score.

        Args:
            text: Input text

        Returns:
            Tuple of (language code, confidence score)
        """
        if not text or len(text.strip()) < 3:
            return "en", 0.0

        try:
            # Get all possible languages with probabilities
            languages = detect_langs(text)

            if not languages:
                return "en", 0.0

            # Get the most probable language
            best_match = languages[0]
            detected_lang = best_match.lang
            confidence = best_match.prob

            # Map detected language to supported languages
            mapped_lang = self._map_language(detected_lang)

            print(f"{Fore.CYAN}Language detection: {mapped_lang} (confidence: {confidence:.2f}){Style.RESET_ALL}")

            return mapped_lang, confidence

        except LangDetectException as e:
            print(f"{Fore.YELLOW}Language detection error: {e}. Defaulting to English.{Style.RESET_ALL}")
            return "en", 0.0
        except Exception as e:
            print(f"{Fore.RED}Unexpected error in language detection: {e}{Style.RESET_ALL}")
            return "en", 0.0

    def _map_language(self, detected_lang: str) -> str:
        """
        Map detected language code to supported language.

        Args:
            detected_lang: Detected language code

        Returns:
            Supported language code
        """
        # Direct match
        if detected_lang in self.supported_languages:
            return detected_lang

        # Language code mapping (langdetect format to our format)
        language_map = {
            "hi": "hi",  # Hindi
            "mr": "mr",  # Marathi
            "en": "en",  # English
        }

        return language_map.get(detected_lang, "en")

    def validate_and_correct(
        self,
        whisper_lang: str,
        whisper_confidence: float,
        text: str
    ) -> Tuple[str, float]:
        """
        Validate Whisper's language detection with langdetect as fallback.

        Args:
            whisper_lang: Language detected by Whisper
            whisper_confidence: Confidence from Whisper
            text: Transcribed text

        Returns:
            Tuple of (final language code, confidence)
        """
        # If Whisper is confident and language is supported, trust it
        if whisper_confidence > 0.8 and whisper_lang in self.supported_languages:
            return whisper_lang, whisper_confidence

        # If Whisper confidence is low, use langdetect as backup
        if whisper_confidence < self.confidence_threshold:
            print(f"{Fore.YELLOW}Low Whisper confidence, using langdetect...{Style.RESET_ALL}")
            detected_lang, lang_confidence = self.detect_language(text)

            # Use langdetect if it's more confident
            if lang_confidence > whisper_confidence:
                return detected_lang, lang_confidence

        # Default to Whisper's detection
        mapped_lang = self._map_language(whisper_lang)
        return mapped_lang, whisper_confidence

    def get_language_name(self, lang_code: str) -> str:
        """
        Get full language name from code.

        Args:
            lang_code: Two-letter language code

        Returns:
            Full language name
        """
        return self.supported_languages.get(lang_code, {}).get("name", "Unknown")

    def is_supported(self, lang_code: str) -> bool:
        """
        Check if language is supported.

        Args:
            lang_code: Language code to check

        Returns:
            True if supported, False otherwise
        """
        return lang_code in self.supported_languages

    def get_supported_languages(self) -> dict:
        """
        Get all supported languages.

        Returns:
            Dictionary of supported languages
        """
        return self.supported_languages
