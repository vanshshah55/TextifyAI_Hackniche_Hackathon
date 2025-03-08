import streamlit as st
from generate_poem import generate_poem, analyze_poem, get_rhyming_words, enhance_poem
import json
from datetime import datetime
import random
from gtts import gTTS
import os
import base64
import tempfile

# Function to convert English terms to Hindi
def convert_to_hindi_terms(text):
    # Dictionary for English to Hindi term conversion
    english_to_hindi = {
        # Shayari specific terms and analysis
        "Shayari": "शायरी",
        "Ghazal": "ग़ज़ल",
        "Nazm": "नज़्म",
        "Rubai": "रुबाई",
        "Qasida": "क़सीदा",
        "Free Flow": "आज़ाद",
        "Matla": "मतला",
        "Maqta": "मक़्ता",
        "Radif": "रदीफ़",
        "Qaafiya": "क़ाफ़िया",
        "Bahr": "बहर",
        "Misra": "मिसरा",
        "Sher": "शेर",
        "Beher": "बहर",
        "Tarannum": "तरन्नुम",
        "Radeef": "रदीफ़",
        "Kaafiya": "काफ़िया",
        
        # Shayari themes and emotions
        "Love": "इश्क़",
        "Life": "ज़िंदगी",
        "Philosophy": "फ़लसफ़ा",
        "Social": "समाजिक",
        "Spiritual": "रूहानी",
        "Romance": "इश्क़िया",
        "Longing": "इंतज़ार",
        "Separation": "जुदाई",
        "Union": "विसाल",
        "Pain": "दर्द",
        "Joy": "ख़ुशी",
        "Hope": "उम्मीद",
        "Despair": "मायूसी",
        "Faith": "यक़ीन",
        "Beauty": "हुस्न",
        "Truth": "हक़ीक़त",
        
        # Technical analysis terms
        "Rhyme Pattern": "तुक योजना",
        "Meter": "बहर",
        "Rhythm": "लय",
        "Flow": "रवानी",
        "Structure": "बनावट",
        "Form": "शैली",
        "Style": "अंदाज़",
        "Theme": "मौज़ू",
        "Meaning": "मायने",
        "Depth": "गहराई",
        "Quality": "मेयार",
        "Language": "ज़बान",
        "Expression": "इज़हार",
        "Imagery": "तस्वीरकशी",
        "Metaphor": "इस्तेआरा",
        "Symbolism": "अलामत",
        
        # Analysis results and descriptions
        "Excellent": "बेहतरीन",
        "Very Good": "बहुत अच्छा",
        "Good": "अच्छा",
        "Average": "औसत",
        "Needs Improvement": "सुधार की ज़रूरत",
        "Perfect": "कामिल",
        "Beautiful": "ख़ूबसूरत",
        "Elegant": "नफ़ीस",
        "Powerful": "मज़बूत",
        "Deep": "गहरा",
        "Meaningful": "मायनेख़ेज़",
        "Simple": "सादा",
        "Complex": "मुरक्कब",
        
        # Enhancement related terms
        "Enhanced": "बेहतर",
        "Version": "नुस्ख़ा",
        "Original": "असल",
        "Analysis": "तजज़िया",
        "Features": "ख़ूबियाँ",
        "Process": "अमल",
        "Result": "नतीजा",
        "Improvement": "बेहतरी",
        "Translation": "तर्जुमा",
        "Lines": "मिसरे",
        "Words": "अल्फ़ाज़",
        "Pattern": "तर्तीब",
        
        # Common phrases in analysis
        "shows": "दिखाता है",
        "contains": "रखता है",
        "demonstrates": "पेश करता है",
        "expresses": "बयान करता है",
        "reveals": "ज़ाहिर करता है",
        "indicates": "ज़ाहिर करता है",
        "suggests": "बताता है",
        "represents": "पेश करता है",
        "has": "रखता है",
        "with": "के साथ",
        "and": "और",
        "in": "में",
        "of": "का",
        "the": "",
        
        # Additional poetic terms
        "Verse": "शेर",
        "Couplet": "दोहा",
        "Stanza": "बंद",
        "Poetry": "शायरी",
        "Poet": "शायर",
        "Composition": "तख़लीक़",
        "Creation": "तख़लीक़",
        "Writing": "तहरीर",
        "Literature": "अदब",
        
        # Mood and emotion descriptions
        "Romantic": "रोमानी",
        "Philosophical": "फ़िलसफ़ाना",
        "Emotional": "जज़्बाती",
        "Passionate": "पुरजोश",
        "Intense": "गहरा",
        "Subtle": "नाज़ुक",
        "Delicate": "नाज़ुक",
        "Strong": "मज़बूत",
        "Soft": "नर्म",
        "Gentle": "मुलायम",
        "Harsh": "सख़्त",
        "Sweet": "मीठा",
        "Bitter": "कड़वा",
        "Happy": "ख़ुश",
        "Sad": "ग़मगीन"
    }
    
    # Replace English terms with Hindi equivalents
    for eng, hin in english_to_hindi.items():
        # Case-insensitive replacement
        text = text.replace(eng.lower(), hin)
        text = text.replace(eng.upper(), hin)
        text = text.replace(eng.capitalize(), hin)
        # Handle plural forms
        text = text.replace(eng.lower() + 's', hin)
        text = text.replace(eng.upper() + 'S', hin)
        text = text.replace(eng.capitalize() + 's', hin)
    
    return text

# Function to analyze poem emotion and context
def analyze_poem_emotion(text, is_shayari=False):
    """
    Analyze the emotional context of the poem to determine recitation style.
    Returns emotion type and intensity.
    """
    # Keywords for emotion detection
    emotion_keywords = {
        'romantic': ['love', 'heart', 'प्रेम', 'दिल', 'इश्क़', 'महोब्बत', 'romantic', 'passion'],
        'melancholic': ['sadness', 'pain', 'दर्द', 'ग़म', 'अकेला', 'विरह', 'grief', 'sorrow'],
        'philosophical': ['life', 'truth', 'जीवन', 'सत्य', 'फ़लसफ़ा', 'meaning', 'wisdom'],
        'nature': ['flowers', 'sky', 'फूल', 'आसमान', 'प्रकृति', 'seasons', 'river'],
        'spiritual': ['divine', 'soul', 'आत्मा', 'ईश्वर', 'रूह', 'spirit', 'prayer'],
        'patriotic': ['nation', 'freedom', 'देश', 'वतन', 'आज़ादी', 'country', 'pride']
    }
    
    # Analyze text for emotions
    text_lower = text.lower()
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        emotion_scores[emotion] = score
    
    # Get primary emotion
    primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    # Determine intensity
    intensity = 'moderate'
    if '!' in text or '?' in text:
        intensity = 'high'
    elif '...' in text or '।' in text:
        intensity = 'contemplative'
    
    return primary_emotion, intensity

# Function to create audio with specific tone/style
def create_styled_audio(text, language, is_shayari=False):
    """
    Create audio with specific style for poem or shayari.
    Uses emotion analysis and contextual pausing for more poetic recitation.
    """
    # Convert language code for gTTS
    lang_code = "hi" if language == "हिंदी" else "en"
    
    # Analyze emotion and context
    emotion, intensity = analyze_poem_emotion(text, is_shayari)
    
    # Process text to add pauses and emphasis
    lines = text.split('\n')
    processed_text = ""
    
    # Emotion-specific pause patterns
    pause_patterns = {
        'romantic': {'line': '... ', 'stanza': '...... ', 'emphasis': '... '},
        'melancholic': {'line': '.... ', 'stanza': '........ ', 'emphasis': '... '},
        'philosophical': {'line': '... ', 'stanza': '....... ', 'emphasis': '.... '},
        'nature': {'line': '.. ', 'stanza': '..... ', 'emphasis': '... '},
        'spiritual': {'line': '.... ', 'stanza': '........ ', 'emphasis': '.... '},
        'patriotic': {'line': '... ', 'stanza': '...... ', 'emphasis': '! '}
    }
    
    current_pauses = pause_patterns.get(emotion, pause_patterns['romantic'])
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        # Process line based on content type and emotion
        if is_shayari:
            # For Shayari, add dramatic pauses and emphasis
            processed_line = line.strip()
            
            # Add emphasis for key phrases
            for emphasis_word in ['इश्क़', 'दिल', 'जान', 'love', 'heart', 'soul']:
                if emphasis_word in processed_line.lower():
                    processed_line = processed_line.replace(emphasis_word, f"{current_pauses['emphasis']}{emphasis_word}")
            
            # Add pause after each misra (line)
            processed_text += processed_line + current_pauses['line']
            
            # Add longer pause at end of complete sher (couplet)
            if i % 2 == 1:
                processed_text += current_pauses['stanza']
        else:
            # For regular poetry, add natural pauses and rhythm
            processed_line = line.strip()
            
            # Add emphasis for important words based on emotion
            if intensity == 'high':
                processed_line = processed_line.replace('!', '! ... ')
                processed_line = processed_line.replace('?', '? ... ')
            
            # Add pauses for punctuation
            processed_line = processed_line.replace(',', ', ... ')
            processed_line = processed_line.replace(';', '; .... ')
            
            # Add pause after each line
            processed_text += processed_line + current_pauses['line']
            
            # Add longer pause between stanzas
            if i < len(lines) - 1 and not lines[i + 1].strip():
                processed_text += current_pauses['stanza']
    
    # Create temporary file for audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        # Adjust speed based on emotion and intensity
        speed = True if (is_shayari or intensity == 'contemplative' or emotion in ['melancholic', 'spiritual']) else False
        
        # Create TTS with processed text and appropriate speed
        tts = gTTS(
            text=processed_text,
            lang=lang_code,
            slow=speed
        )
        
        # Save with high quality settings
        tts.save(fp.name)
        return fp.name

# Function to get audio player HTML with enhanced controls
def get_audio_player_html(audio_path):
    """Generate HTML for audio player with custom styling and enhanced controls."""
    audio_placeholder = st.empty()
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_player = f"""
        <div style='display: flex; justify-content: center; margin: 20px 0;'>
            <audio controls style='width: 100%; max-width: 500px; height: 50px;'>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
        <div style='text-align: center; margin-top: 10px;'>
            <p style='font-size: 0.9em; color: #666;'>
                💫 Adjust playback speed for optimal poetic experience
            </p>
        </div>
    """
    audio_placeholder.markdown(audio_player, unsafe_allow_html=True)

# Page config and styling
st.set_page_config(
    page_title="AI Studio",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with Hindi font support
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
    
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Custom poem text styling */
    .poem-text {
        font-size: 18px;
        line-height: 1.8;
        padding: 25px;
        border-left: 4px solid #6c5ce7;
        background-color: #fff;
        margin: 20px 0;
        white-space: pre-line;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    
    .poem-text.english {
        font-family: 'Georgia', serif;
    }
    
    .poem-text.hindi {
        font-family: 'Noto Sans Devanagari', sans-serif;
        font-size: 20px;
    }
    
    /* Title and headers styling */
    .title-text {
        background: linear-gradient(120deg, #6c5ce7, #a367dc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
    }
    
    .language-selector {
        text-align: center;
        padding: 15px;
        margin-bottom: 20px;
        background: #f8f9fa;
        border-radius: 15px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(120deg, #6c5ce7, #a367dc);
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #6c5ce7;
        padding: 10px 15px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #fff;
        border-radius: 10px;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 20px 0;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-top: 4px solid #6c5ce7;
    }
    
    /* Animation for generated content */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .generated-content {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize language selector first
st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
selected_language = st.radio(
    "Select Language",
    ["English", "हिंदी"],
    horizontal=True
)
st.markdown("</div>", unsafe_allow_html=True)

# Title with custom styling
st.markdown(
    "<h1 class='title-text'>" + 
    ("✨ AI Studio" if selected_language == "English" else "✨ काव्य स्टूडियो") + 
    "</h1>", 
    unsafe_allow_html=True
)

# Generation type selector
st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
generation_type = st.radio(
    "Select Generation Type" if selected_language == "English" else "रचना प्रकार चुनें",
    ["Poetry", "Shayari"] if selected_language == "English" else ["कविता", "शायरी"],
    horizontal=True
)
st.markdown("</div>", unsafe_allow_html=True)

# Define enhancement prompts
enhancement_prompt = {
    "English": ["Improve Imagery", "Strengthen Metaphors", "Refine Rhythm", "Add Symbolism"],
    "Hindi": ["बिम्ब सुधार", "रूपक सशक्तिकरण", "लय परिष्करण", "प्रतीक योजना"]
}

# Define poetry and shayari specific forms
poem_types = {
    "Poetry": {
        "English": ["Sonnet", "Haiku", "Free Verse", "Limerick", "Narrative", "Ode"],
        "हिंदी": ["दोहा", "गज़ल", "मुक्त छंद", "कविता", "गीत", "छंद"]
    },
    "Shayari": {
        "English": ["Ghazal", "Nazm", "Rubai", "Qasida", "Free Flow"],
        "हिंदी": ["ग़ज़ल", "नज़्म", "रुबाई", "क़सीदा", "आज़ाद"]
    }
}

# Define themes for both poetry and shayari
themes = {
    "Poetry": {
        "English": ["Modern", "Classical", "Romantic", "Nature"],
        "हिंदी": ["आधुनिक", "शास्त्रीय", "श्रृंगारिक", "प्रकृति"]
    },
    "Shayari": {
        "English": ["Love", "Life", "Philosophy", "Social", "Spiritual"],
        "हिंदी": ["इश्क़", "ज़िंदगी", "फ़लसफ़ा", "समाज", "रूहानी"]
    }
}

# Main tabs with bilingual labels
tab1, tab2 = st.tabs([
    "✍️ Write & Generate" if selected_language == "English" else "✍️ लिखें और बनाएं",
    "🔍 Analyze & Edit" if selected_language == "English" else "🔍 विश्लेषण और संपादन"
])

with tab1:
    # Bilingual header based on generation type
    header_text = (
        "Create Your Masterpiece" if generation_type == "Poetry" else "Craft Your Shayari"
    ) if selected_language == "English" else (
        "अपनी काव्य रचना करें" if generation_type == "कविता" else "अपनी शायरी रचें"
    )
    
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h3 style='color: #6c5ce7;'>{header_text}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Description input with language-specific placeholder
        placeholder_text = (
            "Let your imagination flow... What would you like your poem to be about?"
            if generation_type == "Poetry" else
            "Express your feelings... What would you like your shayari to convey?"
        ) if selected_language == "English" else (
            "अपनी कल्पना को बहने दें... आप किस विषय पर कविता लिखना चाहेंगे?"
            if generation_type == "कविता" else
            "अपनी भावनाओं को व्यक्त करें... आप क्या कहना चाहते हैं?"
        )
        
        poem_description = st.text_area(
            "Describe your idea:" if selected_language == "English" else "अपना विचार बताएं:",
            height=150,
            placeholder=placeholder_text,
            help="Be as descriptive as possible for better results" if selected_language == "English" else "बेहतर परिणामों के लिए यथासंभव विस्तृत वर्णन करें"
        )
        
        # Interactive elements in columns with language-dependent labels
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            generation_key = "Poetry" if generation_type in ["Poetry", "कविता"] else "Shayari"
            current_types = poem_types[generation_key]
            
            form_type = st.selectbox(
                "Form" if selected_language == "English" else "रचना प्रकार",
                current_types["English"] if selected_language == "English" else current_types["हिंदी"]
            )
        
        with col_b:
            current_themes = themes[generation_key]
            
            theme = st.selectbox(
                "Theme" if selected_language == "English" else "विषय",
                current_themes["English"] if selected_language == "English" else current_themes["हिंदी"]
            )
        
        with col_c:
            output_language = st.selectbox(
                "Output Language" if selected_language == "English" else "आउटपुट भाषा",
                ["English", "हिंदी"]
            )
            
            # Add Shayari length selector when Shayari is selected
            if generation_type in ["Shayari", "शायरी"]:
                shayari_length = st.selectbox(
                    "Shayari Length" if selected_language == "English" else "शायरी की लंबाई",
                    ["Short (2-4 lines)", "Long (6-10 lines)"] if selected_language == "English" else 
                    ["छोटी (2-4 पंक्तियाँ)", "लंबी (6-10 पंक्तियाँ)"]
                )
        
        creativity = st.slider(
            "Creativity Level" if selected_language == "English" else "रचनात्मकता स्तर",
            0.1, 1.0, 0.7,
            help="Higher values mean more creative but less predictable results" if selected_language == "English" else "उच्च मान का अर्थ है अधिक रचनात्मक लेकिन कम अनुमानित परिणाम"
        )
        
        # Generate button with loading animation
        button_text = (
            "✨ Generate Poem" if generation_type == "Poetry" else "✨ Generate Shayari"
        ) if selected_language == "English" else (
            "✨ कविता बनाएं" if generation_type == "कविता" else "✨ शायरी बनाएं"
        )
        
        if st.button(button_text, use_container_width=True):
            if poem_description.strip() == "":
                st.warning(
                    "🎭 Please enter a description first!"
                    if selected_language == "English"
                    else "🎭 कृपया पहले विवरण दर्ज करें!"
                )
            else:
                with st.spinner(
                    "🌟 Crafting your masterpiece..."
                    if selected_language == "English"
                    else "🌟 आपकी रचना बनाई जा रही है..."
                ):
                    try:
                        # Determine shayari_length parameter
                        if generation_type == "Shayari":
                            length_param = "short" if ("Short" in str(shayari_length) or "छोटी" in str(shayari_length)) else "long"
                        else:
                            length_param = "short"  # Default for poetry
                        
                        poem = generate_poem(
                            description=poem_description,
                            poem_type=form_type,
                            theme=theme,
                            creativity=creativity,
                            language=output_language,
                            shayari_length=length_param
                        )
                        
                        # Convert any remaining English terms to Hindi if output language is Hindi
                        if output_language == "हिंदी":
                            poem = convert_to_hindi_terms(poem)
                        
                        st.markdown(
                            f"""<div class='generated-content'>
                                <div class='poem-text {"english" if output_language == "English" else "hindi"}'>{poem}</div>
                            </div>""",
                            unsafe_allow_html=True
                        )
                        
                        # Add audio generation
                        with st.spinner(
                            "🎵 Creating audio rendition..."
                            if selected_language == "English"
                            else "🎵 ऑडियो बना रहा है..."
                        ):
                            is_shayari = generation_type in ["Shayari", "शायरी"]
                            audio_path = create_styled_audio(poem, output_language, is_shayari)
                            get_audio_player_html(audio_path)
                            
                            # Add playback controls
                            st.markdown(
                                """<div style='text-align: center; margin: 10px 0;'>
                                    <p style='font-size: 0.9em; color: #666;'>
                                        {}
                                    </p>
                                </div>""".format(
                                    "🎭 Listen to the recitation with poetic expression"
                                    if selected_language == "English"
                                    else "🎭 काव्यात्मक अभिव्यक्ति के साथ सुनें"
                                ),
                                unsafe_allow_html=True
                            )
                        
                        # Quick actions with bilingual labels
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button(
                                "📋 Copy to Clipboard"
                                if selected_language == "English"
                                else "📋 कॉपी करें"
                            )
                        with col2:
                            st.download_button(
                                "💾 Save Text"
                                if selected_language == "English"
                                else "💾 टेक्स्ट सेव करें",
                                poem,
                                file_name=f"poem.{'txt' if output_language == 'English' else 'txt'}",
                                mime="text/plain"
                            )
                        with col3:
                            # Add download button for audio
                            with open(audio_path, "rb") as f:
                                st.download_button(
                                    "🎵 Save Audio"
                                    if selected_language == "English"
                                    else "🎵 ऑडियो सेव करें",
                                    f,
                                    file_name=f"recitation.mp3",
                                    mime="audio/mp3"
                                )
                        
                        # Clean up temporary audio file
                        os.unlink(audio_path)
                    
                    except Exception as e:
                        st.error(
                            f"😔 Oops! Something went wrong: {str(e)}"
                            if selected_language == "English"
                            else f"😔 माफ़ कीजिये! कुछ गड़बड़ हो गई: {str(e)}"
                        )
    
    with col2:
        # Writing tips in selected language
        tips_text = {
            "English": """
                <div class='metric-card'>
                    <h4>✨ Writing Tips</h4>
                    <ul>
                        <li>Be specific in your description</li>
                        <li>Consider your chosen form's rules</li>
                        <li>Experiment with different themes</li>
                        <li>Try various creativity levels</li>
                    </ul>
                </div>
            """,
            "हिंदी": """
                <div class='metric-card'>
                    <h4>✨ लेखन टिप्स</h4>
                    <ul>
                        <li>विवरण में विशिष्ट रहें</li>
                        <li>चुने गए काव्य रूप के नियमों पर ध्यान दें</li>
                        <li>विभिन्न विषयों का प्रयोग करें</li>
                        <li>विभिन्न रचनात्मकता स्तरों का प्रयोग करें</li>
                    </ul>
                </div>
            """
        }
        st.markdown(tips_text[selected_language], unsafe_allow_html=True)
        
        # Example prompts in selected language
        example_prompts = {
            "English": [
                "A sunset over the ocean waves",
                "The first snowfall of winter",
                "A busy city street at midnight",
                "A garden blooming in spring"
            ],
            "हिंदी": [
                "सूर्यास्त के समय समुद्र की लहरें",
                "सर्दियों की पहली बर्फबारी",
                "आधी रात की व्यस्त सड़क",
                "बसंत में खिलता हुआ बगीचा"
            ]
        }
        
        with st.expander(
            "🎲 Need Inspiration?"
            if selected_language == "English"
            else "🎲 प्रेरणा चाहिए?"
        ):
            if st.button(
                "Get Random Prompt"
                if selected_language == "English"
                else "रैंडम प्रॉम्प्ट पाएं"
            ):
                st.info(random.choice(example_prompts[selected_language]))

with tab2:
    # Analysis section header with language-dependent text
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h3 style='color: #6c5ce7;'>
                {
                    "Analyze & Perfect Your Poem" 
                    if selected_language == "English" 
                    else "अपनी रचना का विश्लेषण और सुधार करें"
                }
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        poem_to_analyze = st.text_area(
            "Enter your poem for analysis:" if selected_language == "English" else "विश्लेषण के लिए अपनी रचना दर्ज करें:",
            height=200,
            placeholder="Paste your poem here..." if selected_language == "English" else "अपनी रचना यहाँ पेस्ट करें..."
        )
        
        # Language selection for analysis
        analysis_language = st.radio(
            "Select original poem language:" if selected_language == "English" else "मूल रचना की भाषा चुनें:",
            ["English", "Hindi"] if selected_language == "English" else ["अंग्रे़ी", "हिंदी"],
            horizontal=True
        )
        
        # Convert analysis_language for internal use
        internal_analysis_language = "English" if analysis_language in ["English", "अंग्रे़ी"] else "Hindi"
        
        analyze_button_text = "🔍 Analyze & Enhance Poem" if selected_language == "English" else "🔍 रचना का विश्लेषण और सुधार करें"
        
        if st.button(analyze_button_text, use_container_width=True):
            if poem_to_analyze.strip():
                with st.spinner(
                    "Analyzing and enhancing your poem..." 
                    if selected_language == "English" 
                    else "आपकी रचना का विश्लेषण और सुधार किया जा रहा है..."
                ):
                    try:
                        # Analyze the original poem
                        analysis = analyze_poem(poem_to_analyze, language=internal_analysis_language)
                        
                        # Convert analysis results to Hindi if needed
                        if selected_language == "हिंदी" or output_language == "हिंदी":
                            # Deep conversion of all analysis results
                            analysis['rhyme_scheme'] = convert_to_hindi_terms(analysis['rhyme_scheme'])
                            analysis['mood'] = convert_to_hindi_terms(analysis['mood'])
                            
                            # Convert metrics and any nested dictionaries
                            for key in analysis.get('metrics', {}):
                                if isinstance(analysis['metrics'][key], str):
                                    analysis['metrics'][key] = convert_to_hindi_terms(analysis['metrics'][key])
                                elif isinstance(analysis['metrics'][key], dict):
                                    for subkey in analysis['metrics'][key]:
                                        if isinstance(analysis['metrics'][key][subkey], str):
                                            analysis['metrics'][key][subkey] = convert_to_hindi_terms(analysis['metrics'][key][subkey])
                        
                            # Convert any additional analysis fields
                            if 'additional_info' in analysis:
                                analysis['additional_info'] = convert_to_hindi_terms(analysis['additional_info'])
                        
                        # Display analysis metrics with language-dependent labels
                        st.markdown("<div class='generated-content'>", unsafe_allow_html=True)
                        
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        with metrics_col1:
                            structure_text = {
                                "English": {
                                    "title": "📏 Structure",
                                    "lines": "Lines",
                                    "words": "Words"
                                },
                                "Hindi": {
                                    "title": "📏 संरचना",
                                    "lines": "पंक्तियाँ",
                                    "words": "शब्द"
                                }
                            }[selected_language]
                            
                            st.markdown(
                                f"""<div class='metric-card'>
                                    <h4>{structure_text["title"]}</h4>
                                    <p>{structure_text["lines"]}: {analysis['metrics']['line_count']}</p>
                                    <p>{structure_text["words"]}: {analysis['metrics']['word_count']}</p>
                                </div>""",
                                unsafe_allow_html=True
                            )
                        
                        with metrics_col2:
                            rhyme_text = "🎵 Rhyme Scheme" if selected_language == "English" else "🎵 तुक योजना"
                            st.markdown(
                                f"""<div class='metric-card'>
                                    <h4>{rhyme_text}</h4>
                                    <p>{analysis['rhyme_scheme']}</p>
                                </div>""",
                                unsafe_allow_html=True
                            )
                        
                        with metrics_col3:
                            mood_text = "💭 Mood" if selected_language == "English" else "💭 भाव"
                            st.markdown(
                                f"""<div class='metric-card'>
                                    <h4>{mood_text}</h4>
                                    <p>{analysis['mood']}</p>
                                </div>""",
                                unsafe_allow_html=True
                            )
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Enhanced versions section
                        enhanced_original = enhance_poem(
                            poem_to_analyze,
                            enhancement_prompt[internal_analysis_language],
                            language=internal_analysis_language
                        )
                        
                        # Ensure complete Hindi conversion for enhanced version
                        if selected_language == "हिंदी" or output_language == "हिंदी":
                            enhanced_original = convert_to_hindi_terms(enhanced_original)
                            # Additional pass for any remaining English terms
                            enhanced_original = convert_to_hindi_terms(enhanced_original)
                        
                        # Display enhanced version
                        enhanced_label = (
                            f"**Enhanced {analysis_language} Version:**"
                            if selected_language == "English"
                            else f"**सुधारित {analysis_language} संस्करण:**"
                        )
                        st.markdown(enhanced_label)
                        st.markdown(
                            f"""<div class='poem-text {internal_analysis_language.lower()}'>
                                {enhanced_original}
                            </div>""",
                            unsafe_allow_html=True
                        )
                        
                        # Add audio generation
                        with st.spinner(
                            "🎵 Creating audio rendition..."
                            if selected_language == "English"
                            else "🎵 ऑडियो बना रहा है..."
                        ):
                            is_shayari = generation_type in ["Shayari", "शायरी"]
                            audio_path = create_styled_audio(enhanced_original, output_language, is_shayari)
                            get_audio_player_html(audio_path)
                            
                            # Add playback controls
                            st.markdown(
                                """<div style='text-align: center; margin: 10px 0;'>
                                    <p style='font-size: 0.9em; color: #666;'>
                                        {}
                                    </p>
                                </div>""".format(
                                    "🎭 Listen to the enhanced version with poetic expression"
                                    if selected_language == "English"
                                    else "🎭 बेहतर संस्करण को काव्यात्मक अभिव्यक्ति के साथ सुनें"
                                ),
                                unsafe_allow_html=True
                            )
                        
                        # Quick actions for enhanced version with language-dependent labels
                        col_a, col_b = st.columns(2)
                        with col_a:
                            copy_button_text = (
                                "📋 Copy Enhanced Version"
                                if selected_language == "English"
                                else "📋 सुधारित संस्करण कॉपी करें"
                            )
                            if st.button(copy_button_text, key="copy_enhanced"):
                                st.write(
                                    "Enhanced version copied!"
                                    if selected_language == "English"
                                    else "सुधारित संस्करण कॉपी किया गया!"
                                )
                        
                        with col_b:
                            save_button_text = (
                                "💾 Save Enhanced Version"
                                if selected_language == "English"
                                else "💾 सुधारित संस्करण सेव करें"
                            )
                            st.download_button(
                                save_button_text,
                                enhanced_original,
                                file_name=f"enhanced_poem_{internal_analysis_language.lower()}.txt",
                                mime="text/plain",
                                key="save_enhanced"
                            )
                        
                        # Add download button for audio
                        with open(audio_path, "rb") as f:
                            st.download_button(
                                "🎵 Save Audio"
                                if selected_language == "English"
                                else "🎵 ऑडियो सेव करें",
                                f,
                                file_name=f"enhanced_recitation.mp3",
                                mime="audio/mp3",
                                key="download_enhanced_audio"
                            )
                        
                        # Clean up temporary audio file
                        os.unlink(audio_path)
                    
                    except Exception as e:
                        error_msg = str(e)
                        if selected_language == "हिंदी":
                            error_msg = convert_to_hindi_terms(error_msg)
                        st.error(
                            f"😔 Oops! Something went wrong: {error_msg}"
                            if selected_language == "English"
                            else f"😔 माफ़ कीजिये! कुछ गड़बड़ हो गई: {error_msg}"
                        )
    
    with col2:
        # Analysis features card with language-dependent text
        features_text = {
            "English": """
                <div class='metric-card'>
                    <h4>✨ Analysis Features</h4>
                    <ul>
                        <li>Structural Analysis</li>
                        <li>Rhyme Pattern Detection</li>
                        <li>Mood Analysis</li>
                        <li>Automatic Enhancement</li>
                        <li>Bilingual Translation</li>
                        <li>Literary Device Detection</li>
                    </ul>
                </div>
            """,
            "Hindi": """
                <div class='metric-card'>
                    <h4>✨ विश्लेषण सुविधाएं</h4>
                    <ul>
                        <li>संरचनात्मक विश्लेषण</li>
                        <li>तुक पैटर्न की पहचान</li>
                        <li>भाव विश्लेषण</li>
                        <li>स्वचालित सुधार</li>
                        <li>द्विभाषी अनुवाद</li>
                        <li>काव्य उपकरणों की पहचान</li>
                    </ul>
                </div>
            """
        }
        st.markdown(features_text[selected_language], unsafe_allow_html=True)
        
        # Enhancement process expander with language-dependent text
        enhancement_process = {
            "English": {
                "title": "📝 Enhancement Process",
                "content": """
                    The enhancement process includes:
                    - Improving imagery and metaphors
                    - Refining rhythm and flow
                    - Adding symbolic elements
                    - Maintaining original meaning
                    - Preserving poetic structure
                    - Translating to other language
                """
            },
            "Hindi": {
                "title": "📝 सुधार प्रक्रिया",
                "content": """
                    सुधार प्रक्रिया में शामिल हैं:
                    - बिम्बों और रूपकों में सुधार
                    - लय और प्रवाह में परिष्कार
                    - प्रतीकात्मक तत्वों का समावेश
                    - मूल अर्थ की रक्षा
                    - काव्य संरचना का संरक्षण
                    - अन्य भाषा में अनुवाद
                """
            }
        }
        
        with st.expander(enhancement_process[selected_language]["title"]):
            st.markdown(enhancement_process[selected_language]["content"])

# Footer remains unchanged
st.markdown("---")
st.markdown(
    """<div style='text-align: center'>
        <p>Made with ❤️ for Poets</p>
    </div>""",
    unsafe_allow_html=True
)
