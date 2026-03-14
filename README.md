# Real-time Multilingual Voice Assistant

🎤 **A FREE, production-ready voice assistant that works WITHOUT any API keys!**

Built with Python 3.10, supports real-time multilingual conversations in English, Hindi, and Marathi - completely offline and free.

## ✨ Key Features

- **🆓 100% FREE - No API Keys Required**: Works out of the box with intelligent local AI
- **🎙️ Real-time Voice Recognition**: Instant speech-to-text using Faster-Whisper
- **🌍 Multilingual Support**: English, Hindi, Marathi (easily extensible)
- **🤖 Smart Local AI**: Enhanced pattern-matching responses without any cloud services
- **🗣️ Natural Text-to-Speech**: Human-like voices using Coqui XTTS
- **🔌 Integration Ready**: Optional support for HuggingFace, OpenAI, or Anthropic
- **💬 Context-Aware**: Maintains conversation history for natural dialogue
- **⚡ Silence Detection**: Automatically stops recording when you finish speaking

## 🚀 Quick Start (No API Keys!)

### Windows:
```bash
# Run the automated setup
setup.bat

# Start immediately (no configuration needed!)
python main.py
```

### Linux/Mac:
```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh

# Start immediately (no configuration needed!)
python main.py
```

That's it! The assistant works immediately without any API keys or configuration.

## 📦 What Gets Installed

**Core Components** (All FREE):
- Faster-Whisper: Speech recognition with automatic language detection
- Coqui TTS: Natural multilingual text-to-speech
- SoundDevice: Microphone and speaker access
- LangDetect: Language validation
- Enhanced Local AI: Smart pattern-matching response system

**No paid services required!**

## 🎯 How It Works

```
1. You speak into microphone
   ↓
2. Whisper detects language & transcribes
   ↓
3. Enhanced Local AI generates intelligent response
   ↓
4. Coqui TTS speaks response in your language
```

All processing happens on your computer - completely private and offline!

## 💡 Usage Examples

**English:**
```
You: "Hello, how are you?"
Assistant: "Hello! It's great to hear from you. How can I assist you today?"

You: "What is 25 plus 17?"
Assistant: "The answer is 42"

You: "What time is it?"
Assistant: "The current time is 3:45 PM"
```

**Hindi:**
```
You: "नमस्ते, आप कैसे हैं?"
Assistant: "मैं बिल्कुल ठीक हूं! पूछने के लिए धन्यवाद। आप कैसे हैं?"

You: "15 और 27 जोड़ो"
Assistant: "उत्तर: 42"
```

**Marathi:**
```
You: "नमस्कार, तुम्ही कसे आहात?"
Assistant: "मी पूर्णपणे बरे आहे! विचारल्याबद्दल धन्यवाद। तुम्ही कसे आहात?"
```

## 🎨 What Can It Do?

The Enhanced Local AI can handle:

✅ Greetings in multiple languages
✅ Time and date queries
✅ Basic math calculations
✅ Jokes and casual conversation
✅ Help and capability questions
✅ Thank you / acknowledgment responses
✅ Contextual follow-up questions
✅ Natural dialogue flow

## ⚙️ Optional: Advanced AI Integration

Want even smarter responses? The system supports three optional modes:

### 1. HuggingFace (FREE, No API Key)
Use free local models from HuggingFace:

```bash
# Install optional dependencies
pip install transformers torch

# Edit .env file
LLM_PROVIDER=huggingface
USE_HUGGINGFACE_LOCAL=true
```

### 2. OpenAI (Requires API Key & Payment)
```bash
# Edit .env file
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
```

### 3. Anthropic Claude (Requires API Key & Payment)
```bash
# Edit .env file
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
```

**Note**: The default local mode works great without any of these!

## 🛠️ Configuration

Edit `config.py` to customize:

### Adjust Microphone Sensitivity
```python
SILENCE_THRESHOLD = 0.01  # Lower = more sensitive
SILENCE_DURATION = 1.5    # Seconds of silence before stopping
```

### Change Whisper Model Size
```python
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large-v3
# tiny = fastest, large-v3 = most accurate
```

### Enable GPU (if available)
```python
WHISPER_DEVICE = "cuda"  # Use "cpu" if no GPU
```

## 🌍 Adding New Languages

1. Edit `config.py`:
```python
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "code": "en"},
    "hi": {"name": "Hindi", "code": "hi"},
    "mr": {"name": "Marathi", "code": "mr"},
    "es": {"name": "Spanish", "code": "es"},  # Add your language
}
```

2. Add TTS language mapping:
```python
TTS_LANGUAGE_MAP = {
    "en": "en",
    "hi": "hi",
    "mr": "hi",
    "es": "es",  # Add mapping
}
```

3. Add responses in `llm_agent.py`

## 🔧 Troubleshooting

### "No audio captured"
- Check microphone permissions
- Adjust `SILENCE_THRESHOLD` in config.py (try 0.005 for sensitive mics)
- Test with: `python -c "import sounddevice as sd; print(sd.query_devices())"`

### "No speech detected"
- Speak closer to the microphone
- Reduce background noise
- Use a better quality microphone

### Slow performance
- Use smaller Whisper model: `WHISPER_MODEL_SIZE = "tiny"`
- Enable GPU if available: `WHISPER_DEVICE = "cuda"`

### Want to test the system?
```bash
python test_system.py
```

## 📱 Project Structure

```
jarvis agent/
├── main.py              # Start here!
├── config.py            # All settings
├── llm_agent.py         # Enhanced AI brain (600+ lines of smart responses)
├── audio_recorder.py    # Microphone capture
├── speech_to_text.py    # Whisper STT
├── language_detector.py # Language validation
├── text_to_speech.py    # Coqui TTS
├── requirements.txt     # Dependencies
├── test_system.py       # System verification
├── examples.py          # Usage examples
└── README.md           # You are here
```

## 🎯 Exit Commands

**English**: exit, quit, goodbye, bye, stop
**Hindi**: बाहर निकलें, बंद करो, अलविदा, रुको
**Marathi**: बाहेर पडा, बंद करा, निरोप, थांबा

Or press `Ctrl+C` anytime.

## 🔒 Privacy

- **100% Local**: All processing happens on your machine
- **No Data Sent**: Nothing is transmitted to external servers
- **No Tracking**: Your conversations are completely private
- **No API Calls**: Unless you explicitly enable optional cloud features

## 💰 Cost Breakdown

**Default Configuration (Local Mode):**
- Speech Recognition: **FREE** (Faster-Whisper)
- AI Responses: **FREE** (Enhanced Local AI)
- Text-to-Speech: **FREE** (Coqui TTS)
- **Total: $0.00**

**Optional API-based LLMs** (if you choose to enable them):
- OpenAI GPT-4: ~$0.01-0.02 per conversation turn
- Anthropic Claude: ~$0.001-0.005 per conversation turn
- HuggingFace Local: **FREE** (runs on your computer)

## 🚦 System Requirements

- **Python**: 3.10 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: ~2GB for models
- **Microphone & Speakers**: Any standard audio devices
- **Internet**: Only for initial setup (downloading models)
- **GPU**: Optional, speeds up processing significantly

## 🤝 Contributing

Want to add more languages or improve responses?

1. Fork the repository
2. Add your enhancements
3. Submit a pull request

## 📄 License

MIT License - Free for personal and commercial use.

## 🎓 Learn More

**Test individual components:**
```bash
python examples.py
```

**Verify system:**
```bash
python test_system.py
```

**Get detailed help:**
Check the code comments - every module is well-documented!

## ⭐ Why This Project?

- **No Vendor Lock-in**: Works without any paid APIs
- **Privacy First**: Your conversations stay on your machine
- **Production Ready**: Clean, modular, well-documented code
- **Easily Extensible**: Add languages, features, or integrate your own models
- **Educational**: Learn how voice assistants work under the hood

## 🎉 Get Started Now!

```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh && ./setup.sh

# Then just run
python main.py
```

**No API keys. No payments. No complicated setup. Just works!**

---

**Built with ❤️ for the open-source community**

*Questions? Issues? Check the troubleshooting section above or review the code - it's heavily commented!*
