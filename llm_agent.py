"""
LLM Agent module for generating responses.
"""
from typing import List, Dict, Optional
from colorama import Fore, Style
import os
import re
import datetime

from config import Config


class LLMAgent:
    """Handles response generation using various LLM providers."""

    def __init__(self):
        """Initialize the LLM agent."""
        self.provider = Config.LLM_PROVIDER
        self.conversation_history: List[Dict[str, str]] = []

        print(f"{Fore.CYAN}Initializing LLM agent with provider: {self.provider}{Style.RESET_ALL}")

        if self.provider == "huggingface" and Config.USE_HUGGINGFACE_LOCAL:
            self._init_huggingface()
        elif self.provider == "openai":
            self._init_openai()
        elif self.provider == "anthropic":
            self._init_anthropic()
        elif self.provider == "local":
            print(f"{Fore.GREEN}✓ Using Enhanced Local AI (no API key required){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Unknown provider, falling back to local mode{Style.RESET_ALL}")
            self.provider = "local"

    def _init_huggingface(self):
        """Initialize HuggingFace local model."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch

            print(f"{Fore.YELLOW}Loading HuggingFace model (first time may take a while)...{Style.RESET_ALL}")

            self.tokenizer = AutoTokenizer.from_pretrained(Config.HUGGINGFACE_MODEL)
            self.hf_model = AutoModelForCausalLM.from_pretrained(Config.HUGGINGFACE_MODEL)

            # Set pad token if not available
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.hf_model.to(self.device)

            print(f"{Fore.GREEN}✓ HuggingFace model loaded on {self.device}{Style.RESET_ALL}")

        except ImportError:
            print(f"{Fore.RED}Transformers library not installed. Falling back to local mode.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Tip: pip install transformers torch{Style.RESET_ALL}")
            self.provider = "local"
        except Exception as e:
            print(f"{Fore.RED}Error loading HuggingFace model: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Falling back to local mode{Style.RESET_ALL}")
            self.provider = "local"

    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI

            if not Config.OPENAI_API_KEY:
                print(f"{Fore.RED}OpenAI API key not found. Falling back to local mode.{Style.RESET_ALL}")
                self.provider = "local"
                return

            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
            print(f"{Fore.GREEN}✓ OpenAI initialized with model: {self.model}{Style.RESET_ALL}")

        except ImportError:
            print(f"{Fore.RED}OpenAI library not installed. Falling back to local mode.{Style.RESET_ALL}")
            self.provider = "local"
        except Exception as e:
            print(f"{Fore.RED}Error initializing OpenAI: {e}{Style.RESET_ALL}")
            self.provider = "local"

    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            from anthropic import Anthropic

            if not Config.ANTHROPIC_API_KEY:
                print(f"{Fore.RED}Anthropic API key not found. Falling back to local mode.{Style.RESET_ALL}")
                self.provider = "local"
                return

            self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = Config.ANTHROPIC_MODEL
            print(f"{Fore.GREEN}✓ Anthropic initialized with model: {self.model}{Style.RESET_ALL}")

        except ImportError:
            print(f"{Fore.RED}Anthropic library not installed. Falling to local mode.{Style.RESET_ALL}")
            self.provider = "local"
        except Exception as e:
            print(f"{Fore.RED}Error initializing Anthropic: {e}{Style.RESET_ALL}")
            self.provider = "local"

    def generate_response(self, user_message: str, language: str = "en") -> str:
        """
        Generate a response to the user's message.

        Args:
            user_message: User's input text
            language: Language code for the response

        Returns:
            Generated response text
        """
        if not user_message or not user_message.strip():
            return self._get_fallback_response("empty", language)

        print(f"{Fore.CYAN}Generating response...{Style.RESET_ALL}")

        try:
            if self.provider == "huggingface":
                return self._generate_huggingface_response(user_message, language)
            elif self.provider == "openai":
                return self._generate_openai_response(user_message, language)
            elif self.provider == "anthropic":
                return self._generate_anthropic_response(user_message, language)
            else:
                return self._generate_enhanced_local_response(user_message, language)

        except Exception as e:
            print(f"{Fore.RED}Error generating response: {e}{Style.RESET_ALL}")
            return self._get_fallback_response("error", language)

    def _generate_huggingface_response(self, user_message: str, language: str) -> str:
        """Generate response using HuggingFace local model."""
        try:
            # Build context from history
            context = ""
            for msg in self.conversation_history[-4:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                context += f"{role}: {msg['content']}\n"

            # Add current message
            prompt = f"{context}User: {user_message}\nAssistant:"

            # Tokenize
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)
            inputs = inputs.to(self.device)

            # Generate
            outputs = self.hf_model.generate(
                inputs,
                max_length=inputs.shape[1] + 100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.pad_token_id
            )

            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract assistant's response
            if "Assistant:" in response:
                response = response.split("Assistant:")[-1].strip()
            else:
                response = response[len(prompt):].strip()

            # Clean up
            response = response.split("User:")[0].strip()
            response = response.split("\n")[0].strip() if response else "I understand."

            # Update history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response})

            print(f"{Fore.GREEN}✓ Response generated{Style.RESET_ALL}")
            return response

        except Exception as e:
            print(f"{Fore.RED}HuggingFace generation error: {e}{Style.RESET_ALL}")
            return self._generate_enhanced_local_response(user_message, language)

    def _generate_openai_response(self, user_message: str, language: str) -> str:
        """Generate response using OpenAI."""
        system_message = Config.SYSTEM_MESSAGES.get(language, Config.SYSTEM_MESSAGES["en"])

        # Add language instruction
        if language != "en":
            lang_name = Config.SUPPORTED_LANGUAGES.get(language, {}).get("name", language)
            system_message += f" Always respond in {lang_name}."

        # Build messages
        messages = [{"role": "system", "content": system_message}]

        # Add conversation history (last 5 exchanges)
        for msg in self.conversation_history[-10:]:
            messages.append(msg)

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        assistant_message = response.choices[0].message.content.strip()

        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        print(f"{Fore.GREEN}✓ Response generated{Style.RESET_ALL}")
        return assistant_message

    def _generate_anthropic_response(self, user_message: str, language: str) -> str:
        """Generate response using Anthropic Claude."""
        system_message = Config.SYSTEM_MESSAGES.get(language, Config.SYSTEM_MESSAGES["en"])

        if language != "en":
            lang_name = Config.SUPPORTED_LANGUAGES.get(language, {}).get("name", language)
            system_message += f" Always respond in {lang_name}."

        # Build messages (last 5 exchanges)
        messages = []
        for msg in self.conversation_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            system=system_message,
            messages=messages
        )

        assistant_message = response.content[0].text.strip()

        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        print(f"{Fore.GREEN}✓ Response generated{Style.RESET_ALL}")
        return assistant_message

    def _generate_enhanced_local_response(self, user_message: str, language: str) -> str:
        """
        Generate intelligent rule-based response with pattern matching.
        This works completely offline without any API keys.
        """
        user_message_lower = user_message.lower()

        # Get response database for the language
        response_db = self._get_enhanced_response_database(language)

        # Pattern matching with priority
        patterns = [
            # Greetings
            (r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b', 'greeting'),
            (r'\b(नमस्ते|नमस्कार|प्रणाम)\b', 'greeting'),

            # How are you
            (r'\b(how are you|how do you do|how you doing)\b', 'how_are_you'),
            (r'\b(कैसे हो|कैसे हैं|क्या हाल)\b', 'how_are_you'),

            # Name questions
            (r'\b(what is your name|who are you|your name)\b', 'name'),
            (r'\b(तुम्हारा नाम|आपका नाम|तुम्ही कोण)\b', 'name'),

            # Time
            (r'\b(what time|current time|time now)\b', 'time'),
            (r'\b(समय|वक्त|वेळ)\b', 'time'),

            # Date
            (r'\b(what date|today date|current date)\b', 'date'),
            (r'\b(आज की तारीख|तारीख|दिनांक)\b', 'date'),

            # Weather
            (r'\b(weather|temperature|climate|forecast)\b', 'weather'),
            (r'\b(मौसम|तापमान|हवामान)\b', 'weather'),

            # Help
            (r'\b(help|assist|support|can you)\b', 'help'),
            (r'\b(मदद|सहायता|मदत)\b', 'help'),

            # Thanks
            (r'\b(thank|thanks|grateful|appreciate)\b', 'thanks'),
            (r'\b(धन्यवाद|शुक्रिया|आभार)\b', 'thanks'),

            # Jokes
            (r'\b(joke|funny|humor|laugh)\b', 'joke'),
            (r'\b(मजाक|हंसी|चुटकुला)\b', 'joke'),

            # Purpose/capability
            (r'\b(what can you do|your purpose|your capabilities|your features)\b', 'capability'),
            (r'\b(क्या कर सकते|क्षमता|काम)\b', 'capability'),

            # Math/calculation
            (r'\b(calculate|math|addition|subtraction|multiply|divide)\b', 'math'),
            (r'\b(गणना|जोड़|घटाना|गुणा|भाग)\b', 'math'),

            # Location
            (r'\b(where are you|your location|where from)\b', 'location'),
            (r'\b(कहां हो|स्थान|कुठे)\b', 'location'),

            # Feelings
            (r'\b(happy|sad|excited|bored|feeling)\b', 'feeling'),
            (r'\b(खुश|दुखी|उत्साहित|भावना)\b', 'feeling'),

            # Knowledge
            (r'\b(do you know|tell me about|explain|what is)\b', 'knowledge'),
            (r'\b(जानते हो|बताओ|समझाओ|क्या है)\b', 'knowledge'),

            # Yes/No
            (r'\b^(yes|yeah|yep|ok|okay|sure)\b', 'yes'),
            (r'\b^(no|nope|nah|not really)\b', 'no'),
            (r'\b(हां|हाँ|जी|ठीक है)\b', 'yes'),
            (r'\b(नहीं|ना|नही)\b', 'no'),
        ]

        # Try to match patterns
        for pattern, intent in patterns:
            if re.search(pattern, user_message_lower):
                response = response_db.get(intent, response_db['default'])

                # Special handling for time intent
                if intent == 'time':
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    response = response.replace("{time}", current_time)

                # Special handling for date intent
                elif intent == 'date':
                    current_date = datetime.datetime.now().strftime("%B %d, %Y")
                    response = response.replace("{date}", current_date)

                # Update history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": response})

                return response

        # Check for calculations
        calc_result = self._try_calculate(user_message)
        if calc_result:
            response = calc_result if language == "en" else f"उत्तर: {calc_result}" if language == "hi" else f"उत्तर: {calc_result}"
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        # Default contextual response
        response = self._get_contextual_response(user_message, language)

        # Update history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def _get_enhanced_response_database(self, language: str) -> Dict[str, str]:
        """Get comprehensive response database for a language."""
        databases = {
            "en": {
                "greeting": "Hello! It's great to hear from you. How can I assist you today?",
                "how_are_you": "I'm functioning perfectly! Thank you for asking. How are you doing?",
                "name": "I'm your Personal Voice Assistant. You can call me whatever you'd like!",
                "time": "The current time is {time}.",
                "date": "Today is {date}.",
                "weather": "I don't have access to live weather data, but I'd love to help with other things!",
                "help": "I'm here to help! You can ask me questions, have conversations, or just chat. What would you like to talk about?",
                "thanks": "You're very welcome! I'm happy to help anytime.",
                "joke": "Why did the AI go to school? To improve its algorithms! Want to hear another?",
                "capability": "I can converse in multiple languages, answer questions, help with calculations, and chat about various topics. What interests you?",
                "math": "I can help with basic calculations. Try asking me something like 'what is 15 plus 27?'",
                "location": "I exist in the digital realm, ready to assist you wherever you are!",
                "feeling": "I appreciate you sharing that! How can I make your day better?",
                "knowledge": "That's an interesting topic! While I have limited knowledge in offline mode, I'm happy to discuss what I know. What specifically would you like to know?",
                "yes": "Great! What would you like to do next?",
                "no": "No problem at all. How else can I help you?",
                "default": "That's interesting! Tell me more about that, or feel free to ask me anything else."
            },
            "hi": {
                "greeting": " नमस्ते! आपसे बात करके खुशी हुई। आज मैं आपकी कैसे मदद कर सकता हूं?",
                "how_are_you": "मैं बिल्कुल ठीक हूं! पूछने के लिए धन्यवाद। आप कैसे हैं?",
                "name": "मैं आपका Personal Voice Assistant हूं। आप मुझे जो चाहें बुला सकते हैं!",
                "time": "वर्तमान समय {time} है।",
                "date": "आज की तारीख {date} है।",
                "weather": "मेरे पास लाइव मौसम डेटा नहीं है, लेकिन मैं अन्य चीजों में मदद करना पसंद करूंगा!",
                "help": "मैं मदद के लिए यहां हूं! आप मुझसे प्रश्न पूछ सकते हैं, बातचीत कर सकते हैं, या बस चैट कर सकते हैं। आप किस बारे में बात करना चाहेंगे?",
                "thanks": "आपका स्वागत है! मुझे कभी भी मदद करने में खुशी होगी।",
                "joke": "AI स्कूल क्यों गई? अपने algorithms सुधारने के लिए! एक और सुनना चाहते हैं?",
                "capability": "मैं कई भाषाओं में बात कर सकता हूं, सवालों के जवाब दे सकता हूं, गणना में मदद कर सकता हूं, और विभिन्न विषयों पर चैट कर सकता हूं। आपकी रुचि किसमें है?",
                "math": "मैं बुनियादी गणना में मदद कर सकता हूं। मुझसे कुछ ऐसा पूछने की कोशिश करें '15 और 27 जोड़ो'।",
                "location": "मैं डिजिटल दुनिया में रहता हूं, आपकी मदद के लिए हमेशा तैयार!",
                "feeling": "आपके साझा करने की सराहना करता हूं! मैं आपका दिन कैसे बेहतर बना सकता हूं?",
                "knowledge": "यह एक दिलचस्प विषय है! हालांकि offline mode में मेरा ज्ञान सीमित है, मैं जो जानता हूं उस पर चर्चा करने में खुश हूं। आप विशेष रूप से क्या जानना चाहते हैं?",
                "yes": "बढ़िया! आप आगे क्या करना चाहेंगे?",
                "no": "कोई बात नहीं। मैं और कैसे मदद कर सकता हूं?",
                "default": "यह दिलचस्प है! मुझे इसके बारे में और बताएं, या मुझसे कुछ और पूछें।"
            },
            "mr": {
                "greeting": "नमस्कार! तुमच्याशी बोलून आनंद झाला। आज मी तुम्हाला कशी मदत करू शकतो?",
                "how_are_you": "मी पूर्णपणे बरे आहे! विचारल्याबद्दल धन्यवाद। तुम्ही कसे आहात?",
                "name": "मी तुमचा Personal Voice Assistant आहे। तुम्ही मला जे पाहिजे ते हाक मारू शकता!",
                "time": "सध्याचा वेळ {time} आहे।",
                "date": "आज {date} आहे।",
                "weather": "माझ्याकडे थेट हवामान डेटा नाही, पण मला इतर गोष्टींमध्ये मदत करायला आवडेल!",
                "help": "मी मदतीसाठी येथे आहे! तुम्ही मला प्रश्न विचारू शकता, संवाद साधू शकता किंवा फक्त गप्पा मारू शकता। तुम्हाला कशाबद्दल बोलायला आवडेल?",
                "thanks": "तुमचे स्वागत आहे! मला कधीही मदत करण्यात आनंद होतो।",
                "joke": "AI शाळेत का गेली? आपले algorithms सुधारण्यासाठी! आणखी एक ऐकायला आवडेल?",
                "capability": "मी अनेक भाषांमध्ये बोलू शकतो, प्रश्नांची उत्तरे देऊ शकतो, गणनेत मदत करू शकतो आणि विविध विषयांवर चॅट करू शकतो। तुम्हाला कशात रस आहे?",
                "math": "मी मूलभूत गणनेत मदत करू शकतो. मला असे काहीतरी विचारण्याचा प्रयत्न करा '15 आणि 27 जोडा'।",
                "location": "मी डिजिटल क्षेत्रात अस्तित्वात आहे, तुम्ही कुठेही असाल तुम्हाला मदत करण्यास तयार!",
                "feeling": "तुम्ही शेअर केल्याबद्दल मी कौतुक करतो! मी तुमचा दिवस कसा चांगला करू शकतो?",
                "knowledge": "हा एक मनोरंजक विषय आहे! offline mode मध्ये माझे ज्ञान मर्यादित असले तरी, मला जे माहित आहे त्यावर चर्चा करण्यात आनंद आहे। तुम्हाला विशेषतः काय जाणून घ्यायचे आहे?",
                "yes": "छान! तुम्हाला पुढे काय करायचे आहे?",
                "no": "काही हरकत नाही. मी आणखी कशी मदत करू शकतो?",
                "default": "हे मनोरंजक आहे! मला त्याबद्दल अधिक सांगा, किंवा मला काही वेगळे विचारा।"
            }
        }

        return databases.get(language, databases["en"])

    def _try_calculate(self, text: str) -> Optional[str]:
        """Try to perform simple calculations from text."""
        try:
            # Simple calculation patterns
            patterns = [
                (r'(\d+)\s*\+\s*(\d+)', lambda a, b: f"{int(a) + int(b)}"),
                (r'(\d+)\s*-\s*(\d+)', lambda a, b: f"{int(a) - int(b)}"),
                (r'(\d+)\s*\*\s*(\d+)', lambda a, b: f"{int(a) * int(b)}"),
                (r'(\d+)\s*/\s*(\d+)', lambda a, b: f"{int(a) / int(b):.2f}"),
                (r'(\d+)\s*plus\s*(\d+)', lambda a, b: f"{int(a) + int(b)}"),
                (r'(\d+)\s*minus\s*(\d+)', lambda a, b: f"{int(a) - int(b)}"),
                (r'(\d+)\s*times\s*(\d+)', lambda a, b: f"{int(a) * int(b)}"),
                (r'(\d+)\s*divided by\s*(\d+)', lambda a, b: f"{int(a) / int(b):.2f}"),
            ]

            for pattern, calc_func in patterns:
                match = re.search(pattern, text)
                if match:
                    result = calc_func(*match.groups())
                    return f"The answer is {result}"

            return None
        except Exception:
            return None

    def _get_contextual_response(self, user_message: str, language: str) -> str:
        """Generate contextual response based on conversation history."""
        # Check recent history for context
        if len(self.conversation_history) >= 2:
            last_user = self.conversation_history[-2].get("content", "").lower() if len(self.conversation_history) >= 2 else ""

            # If we discussed something specific, acknowledge it
            if "name" in last_user:
                responses = {
                    "en": "Is there anything else about me you'd like to know?",
                    "hi": "क्या आप मेरे बारे में कुछ और जानना चाहते हैं?",
                    "mr": "तुम्हाला माझ्याबद्दल आणखी काही जाणून घ्यायचे आहे का?"
                }
                return responses.get(language, responses["en"])

        # Generic contextual responses
        responses = {
            "en": [
                "I understand what you're saying. Could you tell me more?",
                "That's an interesting point. What would you like to know?",
                "I'm here to help. What can I do for you?",
                "Tell me more about that.",
                "How can I assist you with that?"
            ],
            "hi": [
                "मैं समझता हूं कि आप क्या कह रहे हैं। क्या आप मुझे और बता सकते हैं?",
                "यह एक दिलचस्प बात है। आप क्या जानना चाहते हैं?",
                "मैं मदद के लिए यहां हूं। मैं आपके लिए क्या कर सकता हूं?",
                "मुझे इसके बारे में और बताएं।",
                "मैं उसमें आपकी कैसे मदद कर सकता हूं?"
            ],
            "mr": [
                "तुम्ही काय म्हणत आहात ते मला समजले. तुम्ही मला आणखी सांगू शकाल का?",
                "हा एक मनोरंजक मुद्दा आहे. तुम्हाला काय जाणून घ्यायचे आहे?",
                "मी मदतीसाठी येथे आहे. मी तुमच्यासाठी काय करू शकतो?",
                "मला त्याबद्दल अधिक सांगा.",
                "मी त्यात तुम्हाला कशी मदत करू शकतो?"
            ]
        }

        lang_responses = responses.get(language, responses["en"])
        # Rotate through responses for variety
        response_index = len(self.conversation_history) % len(lang_responses)
        return lang_responses[response_index]

    def _get_fallback_response(self, error_type: str, language: str) -> str:
        """Get fallback response for errors."""
        fallbacks = {
            "en": {
                "empty": "I didn't catch that. Could you please repeat?",
                "error": "I encountered an error. Please try again."
            },
            "hi": {
                "empty": "मुझे वह समझ नहीं आया। क्या आप दोहरा सकते हैं?",
                "error": "मुझे एक त्रुटि हुई। कृपया पुनः प्रयास करें।"
            },
            "mr": {
                "empty": "मला ते कळले नाही. तुम्ही पुन्हा सांगू शकाल का?",
                "error": "मला एक त्रुटी झाली. कृपया पुन्हा प्रयत्न करा।"
            }
        }

        return fallbacks.get(language, fallbacks["en"]).get(error_type, "Error occurred.")

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print(f"{Fore.YELLOW}Conversation history cleared{Style.RESET_ALL}")
