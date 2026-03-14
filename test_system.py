#!/usr/bin/env python3
"""
Test script to verify system setup and components.
"""
from colorama import init, Fore, Style
import sys

init(autoreset=True)


def print_section(title):
    """Print section header."""
    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")


def test_imports():
    """Test if all required modules can be imported."""
    print_section("Testing Python Imports")

    modules = [
        ("numpy", "NumPy"),
        ("sounddevice", "SoundDevice"),
        ("scipy", "SciPy"),
        ("faster_whisper", "Faster-Whisper"),
        ("langdetect", "LangDetect"),
        ("colorama", "Colorama"),
        ("dotenv", "Python-dotenv"),
    ]

    optional_modules = [
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("TTS", "Coqui TTS"),
    ]

    success = True

    # Test required modules
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"{Fore.GREEN}✓ {display_name}{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}✗ {display_name} - NOT INSTALLED{Style.RESET_ALL}")
            success = False

    # Test optional modules
    print(f"\n{Fore.YELLOW}Optional modules:{Style.RESET_ALL}")
    for module_name, display_name in optional_modules:
        try:
            __import__(module_name)
            print(f"{Fore.GREEN}✓ {display_name}{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.YELLOW}⚠ {display_name} - Not installed (optional){Style.RESET_ALL}")

    return success


def test_audio_devices():
    """Test audio device availability."""
    print_section("Testing Audio Devices")

    try:
        import sounddevice as sd

        devices = sd.query_devices()
        default_input = sd.query_devices(kind='input')
        default_output = sd.query_devices(kind='output')

        print(f"{Fore.GREEN}✓ Audio devices available{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Default Input Device:{Style.RESET_ALL}")
        print(f"  Name: {default_input['name']}")
        print(f"  Channels: {default_input['max_input_channels']}")

        print(f"\n{Fore.CYAN}Default Output Device:{Style.RESET_ALL}")
        print(f"  Name: {default_output['name']}")
        print(f"  Channels: {default_output['max_output_channels']}")

        return True

    except Exception as e:
        print(f"{Fore.RED}✗ Audio device error: {e}{Style.RESET_ALL}")
        return False


def test_microphone():
    """Test microphone recording."""
    print_section("Testing Microphone")

    try:
        import sounddevice as sd
        import numpy as np

        print(f"{Fore.YELLOW}Recording 2 seconds of audio...{Style.RESET_ALL}")

        duration = 2
        sample_rate = 16000

        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()

        max_amplitude = np.max(np.abs(audio))
        rms = np.sqrt(np.mean(audio ** 2))

        print(f"\n{Fore.CYAN}Audio Stats:{Style.RESET_ALL}")
        print(f"  Max Amplitude: {max_amplitude:.4f}")
        print(f"  RMS: {rms:.4f}")

        if max_amplitude > 0.001:
            print(f"\n{Fore.GREEN}✓ Microphone is working{Style.RESET_ALL}")
            return True
        else:
            print(f"\n{Fore.YELLOW}⚠ Microphone signal is very weak. Check your settings.{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}✗ Microphone test failed: {e}{Style.RESET_ALL}")
        return False


def test_whisper():
    """Test Whisper model loading."""
    print_section("Testing Whisper Model")

    try:
        from faster_whisper import WhisperModel
        from config import Config

        print(f"{Fore.YELLOW}Loading Whisper model ({Config.WHISPER_MODEL_SIZE})...{Style.RESET_ALL}")

        model = WhisperModel(
            Config.WHISPER_MODEL_SIZE,
            device=Config.WHISPER_DEVICE,
            compute_type=Config.WHISPER_COMPUTE_TYPE
        )

        print(f"{Fore.GREEN}✓ Whisper model loaded successfully{Style.RESET_ALL}")
        return True

    except Exception as e:
        print(f"{Fore.RED}✗ Whisper model error: {e}{Style.RESET_ALL}")
        return False


def test_tts():
    """Test TTS model loading."""
    print_section("Testing TTS Model")

    try:
        from TTS.api import TTS
        from config import Config

        print(f"{Fore.YELLOW}Loading TTS model (this may take a while)...{Style.RESET_ALL}")

        tts = TTS(Config.TTS_MODEL_NAME)

        print(f"{Fore.GREEN}✓ TTS model loaded successfully{Style.RESET_ALL}")

        # Test synthesis
        print(f"\n{Fore.YELLOW}Testing speech synthesis...{Style.RESET_ALL}")
        from config import Config
        test_file = Config.TEMP_DIR / "test.wav"
        Config.TEMP_DIR.mkdir(exist_ok=True)

        tts.tts_to_file(
            text="This is a test.",
            language="en",
            file_path=str(test_file)
        )

        if test_file.exists():
            print(f"{Fore.GREEN}✓ TTS synthesis working{Style.RESET_ALL}")
            test_file.unlink()  # Clean up
            return True
        else:
            print(f"{Fore.RED}✗ TTS synthesis failed{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}✗ TTS error: {e}{Style.RESET_ALL}")
        return False


def test_env_config():
    """Test environment configuration."""
    print_section("Testing Environment Configuration")

    try:
        from config import Config
        import os

        print(f"{Fore.CYAN}LLM Provider: {Fore.WHITE}{Config.LLM_PROVIDER}{Style.RESET_ALL}")

        if Config.LLM_PROVIDER == "openai":
            if Config.OPENAI_API_KEY:
                key_preview = Config.OPENAI_API_KEY[:8] + "..." if len(Config.OPENAI_API_KEY) > 8 else "***"
                print(f"{Fore.GREEN}✓ OpenAI API key configured: {key_preview}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}  Model: {Config.OPENAI_MODEL}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ OpenAI API key not set{Style.RESET_ALL}")

        elif Config.LLM_PROVIDER == "anthropic":
            if Config.ANTHROPIC_API_KEY:
                key_preview = Config.ANTHROPIC_API_KEY[:8] + "..." if len(Config.ANTHROPIC_API_KEY) > 8 else "***"
                print(f"{Fore.GREEN}✓ Anthropic API key configured: {key_preview}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}  Model: {Config.ANTHROPIC_MODEL}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ Anthropic API key not set{Style.RESET_ALL}")

        elif Config.LLM_PROVIDER == "local":
            print(f"{Fore.YELLOW}ℹ Using local rule-based responses{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Supported Languages:{Style.RESET_ALL}")
        for code, info in Config.SUPPORTED_LANGUAGES.items():
            print(f"  • {info['name']} ({code})")

        return True

    except Exception as e:
        print(f"{Fore.RED}✗ Configuration error: {e}{Style.RESET_ALL}")
        return False


def main():
    """Run all tests."""
    print(f"\n{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Voice Assistant - System Test{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Environment", test_env_config()))
    results.append(("Audio Devices", test_audio_devices()))
    results.append(("Microphone", test_microphone()))
    results.append(("Whisper Model", test_whisper()))
    results.append(("TTS Model", test_tts()))

    # Summary
    print_section("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}" if result else f"{Fore.RED}✗ FAIL{Style.RESET_ALL}"
        print(f"{name}: {status}")

    print(f"\n{Fore.CYAN}Results: {passed}/{total} tests passed{Style.RESET_ALL}")

    if passed == total:
        print(f"\n{Fore.GREEN}✓ All tests passed! System is ready.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Run 'python main.py' to start the voice assistant.{Style.RESET_ALL}\n")
        return 0
    else:
        print(f"\n{Fore.YELLOW}⚠ Some tests failed. Please fix the issues above.{Style.RESET_ALL}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
