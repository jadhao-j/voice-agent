# QUICK START - No API Keys Needed!

This voice assistant works **immediately** without any API keys or configuration.

## Installation (3 steps)

### Windows:
```bash
1. Double-click `setup.bat`
2. Wait for installation to complete
3. Run: python main.py
```

### Linux/Mac:
```bash
1. chmod +x setup.sh && ./setup.sh
2. Wait for installation to complete
3. Run: python main.py
```

## That's It!

The assistant is now running. Just speak and it will respond in your language!

## Supported Languages

- 🇺🇸 **English** - Full support
- 🇮🇳 **Hindi** (हिंदी) - Full support
- 🇮🇳 **Marathi** (मराठी) - Full support

## Usage

1. **Start the assistant**: `python main.py`
2. **Wait for "🎤 Listening..."**: This means it's ready
3. **Speak naturally**: In any supported language
4. **Stop speaking**: The assistant detects silence automatically
5. **Get response**: It responds in the same language
6. **Exit**: Say "goodbye" or press Ctrl+C

## Examples

### English
```
You: "Hello!"
Assistant: "Hello! It's great to hear from you. How can I assist you today?"

You: "What is 10 plus 5?"
Assistant: "The answer is 15"
```

### Hindi
```
You: "नमस्ते!"
Assistant: "नमस्ते! आपसे बात करके खुशी हुई। आज मैं आपकी कैसे मदद कर सकता हूं?"
```

### Marathi
```
You: "नमस्कार!"
Assistant: "नमस्कार! तुमच्याशी बोलून आनंद झाला। आज मी तुम्हाला कशी मदत करू शकतो?"
```

## Common Issues

### Problem: "No audio captured"
**Solution**: Adjust microphone sensitivity in `config.py`:
```python
SILENCE_THRESHOLD = 0.005  # Make more sensitive
```

### Problem: Too slow
**Solution**: Use faster Whisper model in `config.py`:
```python
WHISPER_MODEL_SIZE = "tiny"  # Fastest option
```

### Problem: Language not detected correctly
**Solution**: Speak longer sentences (more than 5 words)

## Test Your Setup

```bash
python test_system.py
```

This will verify:
- All dependencies are installed
- Microphone is working
- Models load correctly
- System is ready

## Need More Intelligence?

The default local AI is smart and works great. But if you want even more advanced responses:

### Option 1: Free HuggingFace (No API Key)
```bash
pip install transformers torch
```

Edit `.env`:
```
LLM_PROVIDER=huggingface
USE_HUGGINGFACE_LOCAL=true
```

### Option 2: OpenAI (Requires API Key & Payment)
Edit `.env`:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

## Cost: $0

✅ Speech Recognition: FREE
✅ AI Responses: FREE
✅ Text-to-Speech: FREE
✅ No hidden costs
✅ No API keys needed
✅ Works completely offline (after initial setup)

## System Requirements

- Python 3.10+
- 4GB RAM
- Microphone & Speakers
- 2GB storage for models

## Help

- Full documentation: `README.md`
- Test components: `python examples.py`
- Code is well-commented - read it!

---

**Ready in 3 commands. No API keys. No payments. Just works!**

```bash
# 1. Setup
setup.bat  # Windows
# or
./setup.sh  # Linux/Mac

# 2. Run
python main.py

# 3. Speak!
```
