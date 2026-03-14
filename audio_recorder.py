"""
Audio recording module for capturing microphone input.
"""
import numpy as np
import sounddevice as sd
from typing import Tuple
import time
from colorama import Fore, Style

from config import Config


class AudioRecorder:
    """Handles real-time audio recording from microphone."""

    def __init__(self):
        """Initialize the audio recorder."""
        self.sample_rate = Config.SAMPLE_RATE
        self.channels = Config.CHANNELS
        self.silence_threshold = Config.SILENCE_THRESHOLD
        self.silence_duration = Config.SILENCE_DURATION

    def calculate_rms(self, audio_data: np.ndarray) -> float:
        """
        Calculate Root Mean Square (RMS) of audio data.

        Args:
            audio_data: Audio samples as numpy array

        Returns:
            RMS value
        """
        return np.sqrt(np.mean(audio_data ** 2))

    def record_audio(self, duration: int = None) -> Tuple[np.ndarray, int]:
        """
        Record audio from microphone until silence is detected or duration expires.

        Args:
            duration: Maximum recording duration in seconds (None for unlimited)

        Returns:
            Tuple of (audio data as numpy array, sample rate)
        """
        print(f"{Fore.GREEN}🎤 Listening... (speak now){Style.RESET_ALL}")

        recording = []
        silence_start = None
        start_time = time.time()
        has_speech = False

        def callback(indata, frames, time_info, status):
            """Callback function for audio stream."""
            if status:
                print(f"{Fore.YELLOW}Audio status: {status}{Style.RESET_ALL}")
            recording.append(indata.copy())

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.float32,
                callback=callback
            ):
                while True:
                    sd.sleep(100)  # Check every 100ms

                    if len(recording) > 0:
                        # Get recent audio chunk
                        recent_audio = np.concatenate(recording[-5:])
                        rms = self.calculate_rms(recent_audio)

                        # Detect speech
                        if rms > self.silence_threshold:
                            has_speech = True
                            silence_start = None
                        elif has_speech:
                            # Speech detected before, now silence
                            if silence_start is None:
                                silence_start = time.time()
                            elif time.time() - silence_start > self.silence_duration:
                                print(f"{Fore.CYAN}✓ Silence detected, processing...{Style.RESET_ALL}")
                                break

                    # Check duration limit
                    if duration and (time.time() - start_time) > duration:
                        print(f"{Fore.YELLOW}⏱ Max duration reached{Style.RESET_ALL}")
                        break

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Recording interrupted{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error during recording: {e}{Style.RESET_ALL}")
            return np.array([]), self.sample_rate

        if not recording:
            return np.array([]), self.sample_rate

        # Concatenate all recorded chunks
        audio_data = np.concatenate(recording, axis=0)
        audio_data = audio_data.flatten()

        return audio_data, self.sample_rate

    def test_microphone(self) -> bool:
        """
        Test if microphone is working properly.

        Returns:
            True if microphone is accessible, False otherwise
        """
        try:
            devices = sd.query_devices()
            default_input = sd.query_devices(kind='input')
            print(f"{Fore.CYAN}Default input device: {default_input['name']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Sample rate: {self.sample_rate} Hz{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Microphone test failed: {e}{Style.RESET_ALL}")
            return False

    def save_audio(self, audio_data: np.ndarray, filepath: str):
        """
        Save audio data to a WAV file.

        Args:
            audio_data: Audio samples as numpy array
            filepath: Path to save the audio file
        """
        from scipy.io import wavfile
        wavfile.write(filepath, self.sample_rate, audio_data)
        print(f"{Fore.GREEN}Audio saved to {filepath}{Style.RESET_ALL}")
