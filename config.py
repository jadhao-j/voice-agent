"""
Configuration file for the multilingual voice assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for the voice assistant."""

    # Project directories
    BASE_DIR = Path(__file__).parent
    MODELS_DIR = BASE_DIR / "models"
    TEMP_DIR = BASE_DIR / "temp"

    # Audio settings
    SAMPLE_RATE = 16000
    CHANNELS = 1
    RECORDING_DURATION = 5  # seconds for each recording chunk
    SILENCE_THRESHOLD = 0.01  # RMS threshold for silence detection
    SILENCE_DURATION = 1.5  # seconds of silence to stop recording

    # Faster-Whisper settings
    WHISPER_MODEL_SIZE = "base"  # tiny, base, small, medium, large-v3
    WHISPER_DEVICE = "cpu"  # cpu or cuda
    WHISPER_COMPUTE_TYPE = "int8"  # int8, float16, float32

    # Supported languages
    SUPPORTED_LANGUAGES = {
        "en": {"name": "English", "code": "en"},
        "hi": {"name": "Hindi", "code": "hi"},
        "mr": {"name": "Marathi", "code": "mr"}
    }

    # Language detection confidence threshold
    LANG_DETECT_CONFIDENCE = 0.7

    # LLM settings
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "local")  # local, huggingface, openai, anthropic

    # Local LLM settings (no API key required)
    USE_HUGGINGFACE_LOCAL = os.getenv("USE_HUGGINGFACE_LOCAL", "false").lower() == "true"
    HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-small")  # Free local model

    # Optional: API-based LLMs (require API keys)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

    # TTS settings (Coqui XTTS)
    TTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
    TTS_LANGUAGE_MAP = {
        "en": "en",
        "hi": "hi",
        "mr": "hi"  # Marathi uses Hindi model in XTTS
    }

    # Voice settings
    SPEAKER_WAV = None  # Path to reference audio for voice cloning (optional)
    TTS_SPEED = 1.0

    # System messages for different languages
    SYSTEM_MESSAGES = {
        "en": "You are a helpful multilingual voice assistant. Keep responses concise and natural.",
        "hi": "आप एक सहायक बहुभाषी आवाज सहायक हैं। प्रतिक्रियाएं संक्षिप्त और स्वाभाविक रखें।",
        "mr": "तुम्ही एक उपयुक्त बहुभाषी आवाज सहाय्यक आहात. प्रतिसाद संक्षिप्त आणि नैसर्गिक ठेवा."
    }

    # Greeting messages
    GREETINGS = {
        "en": "Hello! I'm your multilingual voice assistant. How can I help you today?",
        "hi": "नमस्ते! मैं आपका बहुभाषी वॉयस असिस्टेंट हूं। आज मैं आपकी कैसे मदद कर सकता हूं?",
        "mr": "नमस्कार! मी तुमचा बहुभाषी व्हॉइस असिस्टंट आहे. आज मी तुम्हाला कशी मदत करू शकतो?"
    }

    # Exit commands
    EXIT_COMMANDS = {
        "en": ["exit", "quit", "goodbye", "bye", "stop"],
        "hi": ["बाहर निकलें", "बंद करो", "अलविदा", "रुको"],
        "mr": ["बाहेर पडा", "बंद करा", "निरोप", "थांबा"]
    }

    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.MODELS_DIR.mkdir(exist_ok=True)
        cls.TEMP_DIR.mkdir(exist_ok=True)
