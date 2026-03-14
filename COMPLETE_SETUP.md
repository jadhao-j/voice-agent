# COMPLETE SETUP GUIDE - Python 3.10.11

This guide will get your voice assistant working in **3 simple steps**.

## Prerequisites
- ✅ Python 3.10.11 installed
- ✅ Microphone connected
- ✅ Speakers/headphones connected
- ✅ Windows 10/11

## Installation (Choose ONE method)

### Method 1: Automated (Recommended)

```powershell
# Just run the automated installer
.\install_py310.bat
```

This will:
1. Check Python 3.10
2. Create virtual environment
3. Install all dependencies
4. Run verification tests
5. Tell you if everything is ready

---

### Method 2: Manual (Step by Step)

```powershell
# 1. Create venv with Python 3.10
py -3.10 -m venv venv

# 2. Activate venv
.\venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 4. Install dependencies (takes 5-10 minutes)
pip install -r requirements.txt

# 5. Verify installation
python verify_setup.py
```

---

## First Run

```powershell
# Start the assistant
python main.py
```

**What happens:**
1. Models download (first time only, ~2GB)
2. Whisper loads (~30 seconds)
3. TTS loads (~1 minute)
4. "🎤 Listening..." appears - NOW SPEAK!

---

## Usage

### Basic Conversation

1. **Wait for**: `🎤 Listening...`
2. **Speak**: "Hello, how are you?"
3. **Stop speaking**: Assistant detects silence
4. **Get response**: In the same language
5. **Continue**: Keep talking as long as you want

### Example Conversations

**English:**
```
You: "Hello!"
Assistant: "Hello! It's great to hear from you. How can I assist you today?"

You: "What is 25 plus 17?"
Assistant: "The answer is 42"

You: "What time is it?"
Assistant: "The current time is 3:45 PM"
```

**Hindi:**
```
You: "नमस्ते!"
Assistant: "नमस्ते! आपसे बात करके खुशी हुई।"

You: "15 और 27 जोड़ो"
Assistant: "उत्तर: 42"
```

**Marathi:**
```
You: "नमस्कार!"
Assistant: "नमस्कार! तुमच्याशी बोलून आनंद झाला।"
```

### Exit Commands

**English**: "goodbye", "exit", "quit", "bye"
**Hindi**: "अलविदा", "बंद करो"
**Marathi**: "निरोप", "बंद करा"

Or press: **Ctrl+C**

---

## What It Can Do (No API Keys!)

✅ **Natural Conversations**
- Greetings and small talk
- Questions and answers
- Context-aware responses

✅ **Calculations**
- Basic math: "what is 15 plus 27?"
- Division: "48 divided by 6"
- Any arithmetic operation

✅ **Information**
- Current time
- Today's date
- General knowledge (limited in offline mode)

✅ **Multilingual**
- Auto-detects English, Hindi, Marathi
- Responds in same language
- Natural voice in each language

---

## Configuration

### Adjust Microphone Sensitivity

Edit `config.py`:
```python
SILENCE_THRESHOLD = 0.01  # Lower = more sensitive (try 0.005)
SILENCE_DURATION = 1.5    # Seconds to wait (try 1.0)
```

### Change Whisper Model Speed

Edit `config.py`:
```python
WHISPER_MODEL_SIZE = "tiny"  # Options:
# - tiny: Fastest, less accurate
# - base: Good balance (default)
# - small: Better accuracy
# - medium: High accuracy, slower
# - large-v3: Best accuracy, slowest
```

### Enable GPU (if you have NVIDIA GPU)

Edit `config.py`:
```python
WHISPER_DEVICE = "cuda"
WHISPER_COMPUTE_TYPE = "float16"
```

---

## Troubleshooting

### Problem: "No audio captured"
**Solution:**
```powershell
# Test microphone
python -c "import sounddevice as sd; print(sd.query_devices())"

# Or adjust sensitivity in config.py
SILENCE_THRESHOLD = 0.005
```

### Problem: "Language not detected correctly"
**Solution:**
- Speak longer sentences (5+ words)
- Speak clearly and at normal pace
- Reduce background noise

### Problem: "Slow performance"
**Solution:**
```python
# In config.py, use smaller model
WHISPER_MODEL_SIZE = "tiny"
```

### Problem: "TTS voice quality"
**Solution:**
- You're using Coqui TTS (best quality)
- First synthesis takes time (model loading)
- Subsequent ones are faster

### Problem: "ImportError"
**Solution:**
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## Integration Examples

### Use in Your Python Code

```python
from audio_recorder import AudioRecorder
from speech_to_text import SpeechToText
from llm_agent import LLMAgent
from text_to_speech import TextToSpeech

# Initialize components
recorder = AudioRecorder()
stt = SpeechToText()
agent = LLMAgent()
tts = TextToSpeech()

# Record audio
audio_data, sr = recorder.record_audio()

# Transcribe
text, lang, conf = stt.transcribe(audio_data, sr)

# Get response
response = agent.generate_response(text, lang)

# Speak response
tts.synthesize_and_play(response, lang)
```

### Call Individual Functions

```python
# Just speech-to-text
from speech_to_text import SpeechToText
stt = SpeechToText()
text, lang, conf = stt.transcribe_file("audio.wav")

# Just text-to-speech
from text_to_speech import TextToSpeech
tts = TextToSpeech()
tts.synthesize_and_play("Hello world", "en")

# Just AI responses
from llm_agent import LLMAgent
agent = LLMAgent()
response = agent.generate_response("What is AI?", "en")
```

---

## Optional: Add More Intelligence

### Option 1: HuggingFace (Free, Local)

```powershell
# Install transformers
pip install transformers torch

# Edit .env
LLM_PROVIDER=huggingface
USE_HUGGINGFACE_LOCAL=true
```

### Option 2: OpenAI (Requires API Key)

```powershell
# Edit .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
```

---

## Files Overview

```
jarvis agent/
├── main.py                    # Main entry point - START HERE
├── config.py                  # All configuration settings
├── llm_agent.py              # AI brain (600+ lines, no API needed!)
├── audio_recorder.py          # Microphone capture
├── speech_to_text.py          # Whisper integration
├── language_detector.py       # Language validation
├── text_to_speech.py          # TTS engine
├── requirements.txt           # Dependencies
├── verify_setup.py            # Test all components
├── install_py310.bat          # Automated installer
├── test_system.py             # System verification
├── examples.py                # Usage examples
└── README.md                  # Full documentation
```

---

## Performance Benchmarks (Python 3.10)

| Component | First Run | Subsequent |
|-----------|-----------|------------|
| Whisper Load | ~30 sec | Instant |
| TTS Load | ~1 min | Instant |
| Speech Recognition | 2-3 sec | 2-3 sec |
| AI Response | Instant | Instant |
| TTS Synthesis | 3-4 sec | 3-4 sec |

**Total response time**: ~5-7 seconds

---

## Cost

- **Everything**: $0.00
- **Forever**: $0.00
- **No trial periods**: Works indefinitely
- **No API calls**: Everything runs on your computer

---

## Next Steps

1. **Run installer**: `.\install_py310.bat`
2. **Verify setup**: `python verify_setup.py`
3. **Start assistant**: `python main.py`
4. **Say "Hello"**: Test it out!
5. **Read full docs**: Check `README.md` for advanced features

---

## Getting Help

### Quick Tests

```powershell
# Test all components
python verify_setup.py

# Test individual modules
python examples.py

# Check system
python test_system.py
```

### Still Having Issues?

1. Check Python version: `py -3.10 --version`
2. Check venv activated: Look for `(venv)` in prompt
3. Reinstall: Delete `venv` folder and run installer again
4. Read error messages carefully - they usually tell you what's wrong

---

## Success Indicators

You'll know it's working when you see:

```
✓ Whisper model loaded successfully
✓ Coqui TTS loaded successfully
✓ Enhanced Local AI (no API key required)

🎤 Listening... (speak now)
```

**Then just speak and watch it respond!**

---

**Ready? Run: `.\install_py310.bat`**
