import re
import pyttsx3
import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Setup TTS engine for sympathetic text-to-speech
def setup_tts_engine():
    """Configure the TTS engine for a sympathetic voice."""
    # Set the speaking rate (default is ~200 words per minute)
    tts_engine.setProperty('rate', 150)  # Slower rate for a calmer tone

    # Set the volume (default is 1.0)
    tts_engine.setProperty('volume', 0.9)  # Slightly softer volume

    # Choose a voice
    voices = tts_engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower():  # Prefer a female voice for a warmer tone
            tts_engine.setProperty('voice', voice.id)
            break
    else:
        # If no female voice is found, default to the first voice
        tts_engine.setProperty('voice', voices[0].id)

setup_tts_engine()

def speak_text(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

# SQLite database setup
# conn = sqlite3.connect('user_data.db')
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS user_locations
#                   (id INTEGER PRIMARY KEY, username TEXT, location TEXT)''')

# def save_user_location(username, location):
#     """Save user location to the database."""
#     cursor.execute("INSERT INTO user_locations (username, location) VALUES (?, ?)", (username, location))
    # conn.commit()

def extract_name(user_input):
    """Extract a name from the user's input."""
    match = re.search(r"my name is (\w+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# Predefined questions and answers
questions = [
    "How can I reduce anxiety?",
    "What are some relaxation techniques?",
    "How do I deal with stress at work?",
    "Can you help me feel better?"
]

answers = [
    "Try deep breathing or meditation to reduce anxiety.",
    "Relaxation techniques include yoga, meditation, and progressive muscle relaxation.",
    "Take short breaks, manage your time effectively, and talk to someone about your stress.",
    "Of course! Talking about your feelings is the first step to feeling better."
]

# Emotional keywords and responses
emotions = {
    "stressed": "It sounds like you're feeling stressed. Try taking deep breaths or stepping away for a few minutes.",
    "anxious": "Feeling anxious can be tough. Consider practicing mindfulness or talking to someone you trust.",
    "low": "If you're feeling low, try to focus on something you enjoy or reach out to a friend or loved one.",
    "overwhelmed": "When feeling overwhelmed, breaking tasks into smaller steps can help.",
    "sad": "I'm sorry you're feeling sad. Talking to a loved one or journaling your thoughts can sometimes help.",
    "tired": "It seems like you're feeling tired. Make sure you're getting enough rest and taking care of yourself.",
    "thanks": "No need to thank me I am just a bot. Keep pushing and keep living your life!",
    "thank you": "No need to thank me I am just a bot. Keep pushing and keep living your life!",
    "anxiety": "Try deep breathing or meditation to reduce anxiety."
    # ,
    # "how can i reduce anxiety?": "Try deep breathing or meditation to reduce anxiety.",
    # "what are some relaxation techniques?": "Relaxation techniques include yoga, meditation, and progressive muscle relaxation.",
    # "how do I deal with stress at work?": "Take short breaks, manage your time effectively, and talk to someone about your stress.",
    # "can you help me feel better?": "Of course! Talking about your feelings is the first step to feeling better."
}

# Stop words for text preprocessing
stop_words = set(stopwords.words('english'))

def preprocess(text):
    """Preprocess text by tokenizing and removing stop words."""
    tokens = word_tokenize(text.lower())
    return [word for word in tokens if word.isalnum() and word not in stop_words]

def detect_emotion(user_input):
    """Detect emotion based on keywords."""
    for emotion, response in emotions.items():
        if emotion in user_input.lower():
            return response
    return None

def get_bot_response(user_input):
    """Get the most relevant response based on user input."""
    # Handle greetings and dynamic name recognition
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if any(greeting in user_input.lower() for greeting in greetings):
        name = extract_name(user_input)
        if name:
            return f"Hi {name}, how may I help you today?"
        return "Hello! How are you feeling today?"
    elif "quit" in user_input.lower():
        return "Goodbye, take care! I'm here whenever you need me."

    # Check for emotional states
    emotion_response = detect_emotion(user_input)
    if emotion_response:
        return emotion_response

    # Process input for similarity matching
    vectorizer = TfidfVectorizer(tokenizer=preprocess, token_pattern=None)
    tfidf = vectorizer.fit_transform(questions + [user_input])
    similarities = cosine_similarity(tfidf[-1], tfidf[:-1])
    max_sim_score = similarities[0].max()

    # Respond with rephrase message if input is too similar to predefined questions
    if max_sim_score > 0.3:
        return "I'm not sure how to help with that. Can you rephrase?"

    # Fallback response if no match or emotion is detected
    return "I'm here to help, but I didn't quite understand. Could you tell me more?"


#def ask_user_location():
#    """Ask for and save user's name and location."""
#    username = input("What's your name? ")
#    location = input("Where are you located? ")
#    save_user_location(username, location)
#    print(f"Thanks, {username}! Your location #({location}) has been saved.")

def chatbot():
    """Main chatbot loop."""
    print("Chatbot has started.")  # Debugging print statement to ensure the function is being entered
    setup_tts_engine()
    
    # Greet the user immediately before starting the conversation loop
    greeting_message = "Hi! How can I help you today? Type 'quit' to exit."
    print(greeting_message)
    speak_text(greeting_message)  # Speak the greeting before entering the loop

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "quit":
            farewell_message = "Goodbye, take care! I'm here whenever you need me."
            print(farewell_message)
            speak_text(farewell_message)  # Speak the farewell message
            break
        
        response = get_bot_response(user_input)
        print(f"Bot: {response}")
        speak_text(response)  # Speak the response

if __name__ == "__main__":
    chatbot()