import requests
import json
import time
from typing import Dict, Any, List
import re
from collections import defaultdict

# Use your Groq API Key
API_KEY = "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"

# Correct Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Bilingual theme-based prompts
THEME_PROMPTS = {
    "English": {
        "Modern": {
            "style": "Create a contemporary poem with modern references and style",
            "elements": ["urban life", "technology", "social media", "current events"]
        },
        "Classical": {
            "style": "Write in a traditional, formal poetic style",
            "elements": ["nature", "love", "death", "beauty", "truth"]
        },
        "Romantic": {
            "style": "Compose a poem with emotional depth and romantic elements",
            "elements": ["passion", "nature", "imagination", "individualism"]
        },
        "Nature": {
            "style": "Create a poem rich with natural imagery and environmental themes",
            "elements": ["landscapes", "seasons", "wildlife", "environmental concerns"]
        }
    },
    "हिंदी": {
        "आधुनिक": {
            "style": "आधुनिक संदर्भों और शैली के साथ एक समकालीन कविता बनाएं",
            "elements": ["शहरी जीवन", "प्रौद्योगिकी", "सोशल मीडिया", "वर्तमान घटनाएं"]
        },
        "शास्त्रीय": {
            "style": "पारंपरिक, औपचारिक काव्य शैली में लिखें",
            "elements": ["प्रकृति", "प्रेम", "मृत्यु", "सौंदर्य", "सत्य"]
        },
        "श्रृंगारिक": {
            "style": "भावनात्मक गहराई और रोमांटिक तत्वों के साथ एक कविता बनाएं",
            "elements": ["जुनून", "प्रकृति", "कल्पना", "व्यक्तिवाद"]
        },
        "प्रकृति": {
            "style": "प्राकृतिक छवियों और पर्यावरण विषयों से भरपूर एक कविता बनाएं",
            "elements": ["प्राकृतिक दृश्य", "ऋतुएं", "वन्यजीवन", "पर्यावरण चिंताएं"]
        }
    }
}

# Poetry forms and their rules for both languages
POETRY_FORMS = {
    "Sonnet": {
        "english": {
            "structure": "14 lines, iambic pentameter",
            "rules": ["Rhyme scheme: abab cdcd efef gg", "Turn at line 9"]
        },
        "hindi": {
            "structure": "14 पंक्तियाँ",
            "rules": ["उचित तुकबंदी", "भावपूर्ण अभिव्यक्ति"]
        }
    },
    "Haiku": {
        "english": {
            "structure": "3 lines: 5-7-5 syllables",
            "rules": ["Nature theme", "Present tense", "Seasonal reference"]
        },
        "hindi": {
            "structure": "तीन पंक्तियाँ",
            "rules": ["प्रकृति थीम", "वर्तमान काल", "ऋतु संदर्भ"]
        }
    },
    "Free Verse": {
        "english": {
            "structure": "No fixed structure",
            "rules": ["Poetic devices", "Imagery", "Flow"]
        },
        "hindi": {
            "structure": "मुक्त छंद",
            "rules": ["काव्य सौंदर्य", "बिम्ब योजना", "प्रवाह"]
        }
    },
    "Ghazal": {
        "english": {"structure": "Couplet-based form", "rules": ["Emotional depth", "Rhyming couplets", "Max 5 lines"]},
        "hindi": {"structure": "युग्मक आधारित", "rules": ["भावनात्मक गहराई", "तुकांत युग्मक", "अधिकतम 5 पंक्तियाँ"]}
    },
    "Nazm": {
        "english": {"structure": "Free-flowing verse", "rules": ["Emotional expression", "Metaphorical", "Max 5 lines"]},
        "hindi": {"structure": "मुक्त काव्य", "rules": ["भावनात्मक अभिव्यक्ति", "रूपकात्मक", "अधिकतम 5 पंक्तियाँ"]}
    },
    "Rubai": {
        "english": {"structure": "Quatrain", "rules": ["Four lines", "Philosophical theme", "Rhyme scheme AABA"]},
        "hindi": {"structure": "चतुष्पदी", "rules": ["चार पंक्तियाँ", "दार्शनिक विषय", "तुकांत AABA"]}
    }
}

def generate_poem(
    description: str,
    poem_type: str,
    theme: str,
    creativity: float = 0.7,
    language: str = "English",
    max_retries: int = 3,
    retry_delay: int = 1,
    shayari_length: str = "short"  # New parameter for Shayari length
) -> str:
    """Generate poem or shayari based on type."""
    
    # Check if this is a Shayari request
    is_shayari = poem_type in ["Ghazal", "Nazm", "Rubai", "Qasida", "Free Flow", "ग़ज़ल", "नज़्म", "रुबाई", "क़सीदा", "आज़ाद"]
    
    if is_shayari:
        # Set line limits based on Shayari length
        max_lines = 4 if shayari_length == "short" else 10
        min_lines = 2 if shayari_length == "short" else 6
        
        # Special handling for Shayari based on output language
        if language == "हिंदी" or language == "Hindi":
            system_prompt = f"""आप एक अनुभवी शायर हैं। निम्नलिखित विषय पर एक भावपूर्ण {'लघु' if shayari_length == 'short' else 'विस्तृत'} शायरी लिखें:
विषय: {description}

निर्देश:
- {'2-4 पंक्तियाँ' if shayari_length == 'short' else '6-10 पंक्तियाँ'}
- गहरी भावनाओं की अभिव्यक्ति
- सरल लेकिन प्रभावशाली भाषा
- शुद्ध हिंदी में लिखें
- विषय: {theme}
- शैली: {poem_type}

महत्वपूर्ण: 
- केवल हिंदी भाषा का प्रयोग करें
- देवनागरी लिपि में लिखें
- कोई अंग्रेजी शब्द न प्रयोग करें
- भावनात्मक गहराई बनाए रखें"""

            user_prompt = f"इस विषय पर एक भावपूर्ण {'लघु' if shayari_length == 'short' else 'विस्तृत'} हिंदी शायरी लिखें: {description}"

        else:
            system_prompt = f"""You are a master of English poetry. Create a deeply emotional {shayari_length} verse on the following theme:
Theme: {description}

Guidelines:
- {'2-4 lines' if shayari_length == 'short' else '6-10 lines'}
- Express deep emotions
- Simple yet impactful language
- Use pure English vocabulary
- Theme: {theme}
- Style: {poem_type}

Important:
- Use ONLY English language
- Create a verse that captures the essence of Shayari in English
- Focus on emotional depth and impact
- No Hindi/Urdu words or transliterations"""

            user_prompt = f"Create a deeply emotional {shayari_length} English verse about: {description}"

        # Higher creativity for emotional depth
        creativity = 0.8
        
        # Prepare data for API call
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": creativity,
            "max_tokens": 1000
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                generated_text = result["choices"][0]["message"]["content"]
                
                # Filter and limit lines based on Shayari length
                lines = [line for line in generated_text.split('\n') if line.strip()]
                if len(lines) > max_lines:
                    lines = lines[:max_lines]
                elif len(lines) < min_lines:
                    # If too short, try again
                    if attempt < max_retries - 1:
                        continue
                return clean_poem('\n'.join(lines))

            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to generate: {str(e)}")
                time.sleep(retry_delay)
    else:
        # Regular poem generation (existing code)
        form_data = POETRY_FORMS.get(poem_type, {
            "english": {"structure": "Free form", "rules": []},
            "hindi": {"structure": "मुक्त रचना", "rules": []}
        })
        
        if language == "English":
            system_prompt = f"""You are a master poet specializing in {theme.lower()} poetry.
Create a {poem_type.lower()} based on the English description provided.
Guidelines:
- Structure: {form_data['english']['structure']}
- Rules: {', '.join(form_data['english']['rules'])}
- Theme: {theme}
- Use vivid imagery and metaphors
- Include emotional depth
- Maintain consistent style"""
        else:
            system_prompt = f"""You are a master Hindi poet (कवि).
Create a Hindi poem based on this English description: "{description}"
Guidelines:
- रचना प्रकार: {form_data['hindi']['structure']}
- नियम: {', '.join(form_data['hindi']['rules'])}
- विषय: {theme}
- सजीव बिम्बों का प्रयोग करें
- भावनात्मक गहराई समाहित करें
- भाषा शैली में एकरूपता बनाए रखें
Important: Generate the poem in Hindi (Devanagari script) only."""
        
        user_prompt = f"Create a {theme.lower()} {poem_type.lower()} about: {description}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": creativity,
        "max_tokens": 1000
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"]
            
            # For Shayari, ensure it doesn't exceed 5 lines
            if is_shayari:
                lines = [line for line in generated_text.split('\n') if line.strip()]
                if len(lines) > 5:
                    lines = lines[:5]
                generated_text = '\n'.join(lines)
            
            return clean_poem(generated_text)

        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed to generate: {str(e)}")
            time.sleep(retry_delay)

def clean_poem(poem: str) -> str:
    """Clean and format the generated poem."""
    poem = poem.strip()
    poem = re.sub(r'```\w*\n?', '', poem)  # Remove code blocks
    poem = poem.replace("poem", "")
    return poem

def analyze_poem(poem: str, language: str = "English") -> Dict[str, Any]:
    """Analyze poem with language support."""
    lines = poem.split('\n')
    
    analysis = {
        "metrics": calculate_metrics(poem),
        "rhyme_scheme": analyze_rhyme_scheme(lines) if language == "English" else analyze_hindi_rhyme(lines),
        "mood": analyze_mood(poem, language),
        "literary_devices": find_literary_devices(poem, language)
    }
    
    return analysis

def analyze_syllables(lines: List[str]) -> List[int]:
    """Analyze syllable pattern of each line."""
    def count_syllables(word: str) -> int:
        # Basic syllable counting - can be improved
        count = len(re.findall(r'[aeiou]+', word.lower()))
        return max(1, count)
    
    return [sum(count_syllables(word) for word in line.split()) for line in lines]

def analyze_rhyme_scheme(lines: List[str]) -> str:
    """Determine the rhyme scheme of the poem."""
    def get_last_word(line: str) -> str:
        words = re.findall(r'\w+', line)
        return words[-1].lower() if words else ''
    
    last_words = [get_last_word(line) for line in lines if line.strip()]
    rhyme_dict = {}
    current_rhyme = 'A'
    scheme = []
    
    for word in last_words:
        if word not in rhyme_dict:
            rhyme_dict[word] = current_rhyme
            current_rhyme = chr(ord(current_rhyme) + 1)
        scheme.append(rhyme_dict[word])
    
    return ''.join(scheme)

def analyze_matra_pattern(lines: List[str]) -> List[int]:
    """Analyze matra pattern for Hindi poems."""
    # Basic implementation - can be improved
    return [len(line) for line in lines]

def analyze_hindi_rhyme(lines: List[str]) -> str:
    """Analyze rhyme scheme for Hindi poems."""
    # Basic implementation - can be improved
    def get_last_word(line: str) -> str:
        words = line.split()
        return words[-1] if words else ''
    
    last_words = [get_last_word(line) for line in lines if line.strip()]
    rhyme_dict = {}
    current_rhyme = 'क'
    scheme = []
    
    for word in last_words:
        if word not in rhyme_dict:
            rhyme_dict[word] = current_rhyme
            # Use Devanagari characters for rhyme scheme
            current_rhyme = chr(ord(current_rhyme) + 1)
        scheme.append(rhyme_dict[word])
    
    return ''.join(scheme)

def analyze_mood(poem: str, language: str = "English") -> str:
    """Analyze mood with language support."""
    # Enhanced mood analysis with more options
    moods = {
        "English": [
            "Contemplative", "Joyful", "Melancholic", "Romantic",
            "Nostalgic", "Hopeful", "Peaceful", "Mysterious"
        ],
        "Hindi": [
            "चिंतनशील", "आनंदमय", "विषादपूर्ण", "श्रृंगारिक",
            "नॉस्टैल्जिक", "आशावादी", "शांतिपूर्ण", "रहस्यमय"
        ]
    }
    
    # Simple mood detection based on keywords (can be enhanced)
    mood_keywords = {
        "English": {
            "Joyful": ["happy", "joy", "laugh", "smile", "bright", "sun"],
            "Melancholic": ["sad", "tears", "dark", "pain", "grief"],
            "Romantic": ["love", "heart", "passion", "desire", "embrace"],
            "Contemplative": ["think", "wonder", "ponder", "question"],
            "Nostalgic": ["remember", "memory", "past", "childhood"],
            "Hopeful": ["hope", "future", "dream", "wish", "better"],
            "Peaceful": ["peace", "calm", "quiet", "serene", "gentle"],
            "Mysterious": ["mystery", "secret", "unknown", "shadow"]
        },
        "Hindi": {
            "आनंदमय": ["खुशी", "आनंद", "हंसी", "मुस्कान"],
            "विषादपूर्ण": ["दुख", "आंसू", "पीड़ा", "व्यथा"],
            "श्रृंगारिक": ["प्रेम", "प्यार", "दिल", "हृदय"],
            "चिंतनशील": ["सोच", "विचार", "चिंतन"],
            "नॉस्टैल्जिक": ["याद", "स्मृति", "बचपन"],
            "आशावादी": ["आशा", "सपना", "भविष्य"],
            "शांतिपूर्ण": ["शांति", "शांत", "निर्मल"],
            "रहस्यमय": ["रहस्य", "छाया", "अज्ञात"]
        }
    }
    
    # Count occurrences of mood keywords
    mood_counts = {mood: 0 for mood in moods[language]}
    poem_lower = poem.lower()
    
    for mood, keywords in mood_keywords[language].items():
        for keyword in keywords:
            if keyword.lower() in poem_lower:
                mood_counts[mood] += 1
    
    # Get the mood with highest keyword matches
    dominant_mood = max(mood_counts.items(), key=lambda x: x[1])[0]
    
    # If no mood is detected, return default
    if mood_counts[dominant_mood] == 0:
        return moods[language][0]
    
    return dominant_mood

def find_literary_devices(poem: str, language: str) -> Dict[str, List[str]]:
    """Find literary devices with language support."""
    if language == "English":
        return {
            "alliteration": find_alliteration(poem),
            "assonance": find_assonance(poem),
            "metaphors": [],
            "similes": find_similes(poem)
        }
    else:
        return {
            "अनुप्रास": find_hindi_alliteration(poem),
            "रूपक": [],
            "उपमा": find_hindi_similes(poem)
        }

def find_alliteration(text: str) -> List[str]:
    """Find instances of alliteration."""
    words = text.split()
    alliterations = []
    for i in range(len(words) - 1):
        if words[i][0].lower() == words[i + 1][0].lower():
            alliterations.append(f"{words[i]} {words[i + 1]}")
    return alliterations

def find_assonance(text: str) -> List[str]:
    """Find instances of assonance."""
    # Basic implementation - can be improved
    return []

def find_similes(text: str) -> List[str]:
    """Find similes in the text."""
    similes = re.findall(r'\w+\s+like\s+\w+', text)
    return similes

def find_hindi_alliteration(text: str) -> List[str]:
    """Find alliteration in Hindi text."""
    words = text.split()
    alliterations = []
    for i in range(len(words) - 1):
        if words[i] and words[i+1] and words[i][0] == words[i+1][0]:
            alliterations.append(f"{words[i]} {words[i+1]}")
    return alliterations

def find_hindi_similes(text: str) -> List[str]:
    """Find similes in Hindi text."""
    similes = re.findall(r'\w+\s+(जैसे|सा|सी|से)\s+\w+', text)
    return similes

def calculate_metrics(poem: str) -> Dict[str, Any]:
    """Calculate metrics for both languages."""
    return {
        "line_count": len(poem.split('\n')),
        "word_count": len(poem.split()),
        "char_count": len(poem),
        "average_line_length": len(poem) / max(1, len(poem.split('\n')))
    }

def get_rhyming_words(word: str) -> List[str]:
    """Get a list of words that rhyme with the input word."""
    # This would typically use a rhyming dictionary API
    # For now, returning placeholder data
    return ["Example rhyming words would appear here"]

def enhance_poem(poem: str, options: List[str], language: str = "English") -> str:
    """Enhance a poem based on selected options while maintaining the original language."""
    
    # Create language-specific enhancement prompt
    if language == "English":
        system_prompt = f"""Enhance this English poem by focusing on: {', '.join(options)}.
Guidelines:
- Maintain the original structure and meaning
- Improve the selected aspects
- Keep the same language (English)
- Preserve the poem's core essence
- Enhance poetic elements naturally"""
    else:
        system_prompt = f"""इस हिंदी कविता को निम्नलिखित पहलुओं पर ध्यान देते हुए बेहतर बनाएं: {', '.join(options)}
दिशानिर्देश:
- मूल संरचना और अर्थ बनाए रखें
- चुने गए पहलुओं को बेहतर बनाएं
- भाषा हिंदी में ही रखें
- कविता का मूल भाव बनाए रखें
- काव्य तत्वों को स्वाभाविक रूप से बढ़ाएं"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": poem}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return clean_poem(result["choices"][0]["message"]["content"])
    except Exception as e:
        raise Exception(f"Failed to enhance poem: {str(e)}")
