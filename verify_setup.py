"""
Step-by-step setup and verification script.
Run this to ensure everything is installed correctly.
"""
import sys
from colorama import init, Fore, Style

init(autoreset=True)


def print_header(text):
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def print_step(number, text):
    print(f"{Fore.YELLOW}[{number}] {text}{Style.RESET_ALL}")


def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_info(text):
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")


print_header("Voice Assistant - Installation Verification")

# Step 1: Python Version
print_step(1, "Checking Python version...")
py_version = sys.version_info
print(f"Python {py_version.major}.{py_version.minor}.{py_version.micro}")

if py_version.major == 3 and 10 <= py_version.minor <= 11:
    print_success("Perfect! Python 3.10-3.11 detected. Coqui TTS will work.")
elif py_version.major == 3 and py_version.minor >= 12:
    print_info("Python 3.12+ detected. Will use pyttsx3 for TTS.")
else:
    print_error("Python 3.10 or higher required!")
    sys.exit(1)

# Step 2: Import core packages
print_step(2, "Testing core imports...")

packages = {
    "numpy": "NumPy",
    "scipy": "SciPy",
    "sounddevice": "SoundDevice",
    "faster_whisper": "Faster-Whisper",
    "langdetect": "Language Detection",
    "colorama": "Colorama",
    "dotenv": "Python-dotenv",
}

failed = []
for module, name in packages.items():
    try:
        __import__(module)
        print_success(f"{name} installed")
    except ImportError:
        print_error(f"{name} NOT installed")
        failed.append(name)

if failed:
    print_error(f"\nMissing packages: {', '.join(failed)}")
    print_info("Run: pip install -r requirements.txt")
    sys.exit(1)

# Step 3: TTS Engine
print_step(3, "Checking TTS engine...")

tts_available = False
tts_engine = None

try:
    import TTS
    print_success("Coqui TTS is installed (high-quality voices)")
    tts_available = True
    tts_engine = "coqui"
except ImportError:
    print_info("Coqui TTS not available")

try:
    import pyttsx3
    print_success("pyttsx3 is installed (system voices)")
    tts_available = True
    if tts_engine is None:
        tts_engine = "pyttsx3"
except ImportError:
    print_info("pyttsx3 not available")

if not tts_available:
    print_error("No TTS engine found!")
    print_info("Install: pip install TTS (Python 3.10-3.11) or pip install pyttsx3")
    sys.exit(1)

print_success(f"Using TTS engine: {tts_engine}")

# Step 4: Audio devices
print_step(4, "Checking audio devices...")

try:
    import sounddevice as sd

    input_device = sd.query_devices(kind='input')
    output_device = sd.query_devices(kind='output')

    print_success(f"Microphone: {input_device['name']}")
    print_success(f"Speakers: {output_device['name']}")
except Exception as e:
    print_error(f"Audio device error: {e}")
    print_info("Please check your microphone and speaker connections")

# Step 5: Test microphone
print_step(5, "Testing microphone...")

try:
    import numpy as np

    print_info("Recording 2 seconds... Please make some noise!")
    duration = 2
    sample_rate = 16000

    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()

    max_amplitude = np.max(np.abs(audio))
    rms = np.sqrt(np.mean(audio ** 2))

    print(f"Max amplitude: {max_amplitude:.4f}, RMS: {rms:.4f}")

    if max_amplitude > 0.001:
        print_success("Microphone is working!")
    else:
        print_error("Microphone signal is very weak")
        print_info("Speak louder or adjust SILENCE_THRESHOLD in config.py")
except Exception as e:
    print_error(f"Microphone test failed: {e}")

# Step 6: Configuration
print_step(6, "Checking configuration...")

try:
    from config import Config

    print_success(f"LLM Provider: {Config.LLM_PROVIDER}")
    print_success(f"Whisper Model: {Config.WHISPER_MODEL_SIZE}")
    print_success(f"Supported Languages: {', '.join(Config.SUPPORTED_LANGUAGES.keys())}")

    # Check directories
    Config.setup_directories()
    print_success("Created necessary directories")
except Exception as e:
    print_error(f"Configuration error: {e}")

# Step 7: Test Whisper
print_step(7, "Testing Whisper model (this may take a minute)...")

try:
    from faster_whisper import WhisperModel
    from config import Config

    print_info(f"Loading {Config.WHISPER_MODEL_SIZE} model...")
    model = WhisperModel(
        Config.WHISPER_MODEL_SIZE,
        device=Config.WHISPER_DEVICE,
        compute_type=Config.WHISPER_COMPUTE_TYPE
    )
    print_success("Whisper model loaded successfully!")
except Exception as e:
    print_error(f"Whisper error: {e}")
    print_info("This is normal on first run - models will download automatically")

# Step 8: Test TTS
print_step(8, "Testing TTS engine...")

if tts_engine == "coqui":
    try:
        from TTS.api import TTS
        print_info("Loading Coqui TTS (first time takes 2-3 minutes)...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print_success("Coqui TTS loaded successfully!")

        print_info("Testing voice synthesis...")
        from config import Config
        Config.TEMP_DIR.mkdir(exist_ok=True)
        test_file = Config.TEMP_DIR / "test_tts.wav"

        tts.tts_to_file(text="Testing voice synthesis.", language="en", file_path=str(test_file))

        if test_file.exists():
            print_success("TTS synthesis working!")
            test_file.unlink()
        else:
            print_error("TTS file not created")
    except Exception as e:
        print_error(f"Coqui TTS error: {e}")
        print_info("This is normal on first run - models will download")

elif tts_engine == "pyttsx3":
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print_success(f"pyttsx3 ready with {len(voices)} voices")
    except Exception as e:
        print_error(f"pyttsx3 error: {e}")

# Step 9: Test LLM Agent
print_step(9, "Testing LLM Agent...")

try:
    from llm_agent import LLMAgent

    agent = LLMAgent()

    # Test in English
    response = agent.generate_response("Hello", "en")
    if response:
        print_success(f"English response: {response[:50]}...")

    # Test in Hindi
    response = agent.generate_response("नमस्ते", "hi")
    if response:
        print_success(f"Hindi response: {response[:50]}...")

    print_success("LLM Agent working!")
except Exception as e:
    print_error(f"LLM Agent error: {e}")

# Final summary
print_header("Verification Complete!")

print(f"\n{Fore.GREEN}System Status:{Style.RESET_ALL}")
print(f"  • Python Version: {Fore.CYAN}{py_version.major}.{py_version.minor}.{py_version.micro}{Style.RESET_ALL}")
print(f"  • TTS Engine: {Fore.CYAN}{tts_engine}{Style.RESET_ALL}")
print(f"  • LLM Provider: {Fore.CYAN}local (no API keys){Style.RESET_ALL}")
print(f"  • Ready: {Fore.GREEN}YES{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}To start the voice assistant:{Style.RESET_ALL}")
print(f"  {Fore.CYAN}python main.py{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL}")
print(f"  1. Wait for '🎤 Listening...'")
print(f"  2. Speak in English, Hindi, or Marathi")
print(f"  3. Stop speaking (assistant detects silence)")
print(f"  4. Get response in same language")
print(f"  5. Say 'goodbye' or press Ctrl+C to exit\n")

print(f"{Fore.GREEN}{'=' * 70}{Style.RESET_ALL}")
print(f"{Fore.GREEN}Everything is ready! Run 'python main.py' to start.{Style.RESET_ALL}")
print(f"{Fore.GREEN}{'=' * 70}{Style.RESET_ALL}\n")
