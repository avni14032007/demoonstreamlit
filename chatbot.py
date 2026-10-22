import streamlit as st
import numpy as np
import time
import random
from datetime import datetime  # ADDED

# =====================================================
# ADDED: page setup
# =====================================================
st.set_page_config(page_title="ChatBot", page_icon="🤖")
st.title("🤖 My ChatBot")
st.caption("Type 'help' to see what I can do")

# =====================================================
# ADDED: bot data
# =====================================================
GREETINGS = ["hi", "hii", "hiii", "hello", "hey", "heyy", "namaste", "hola", "yo",
             "good morning", "good afternoon", "good evening"]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "Why did the computer go to the doctor? It had a virus! 🤒",
    "Why was the math book sad? It had too many problems. 📘",
    "What do you call a fake noodle? An impasta! 🍝",
    "Why don't skeletons fight each other? They don't have the guts. 💀",
]

FACTS = [
    "Honey never spoils — edible honey has been found in ancient Egyptian tombs. 🍯",
    "Octopuses have three hearts. 🐙",
    "A day on Venus is longer than a year on Venus. 🪐",
    "Bananas are berries, but strawberries are not. 🍌",
    "The Eiffel Tower grows a few cm taller in summer due to heat expansion. 🗼",
]

QUOTES = [
    "Small steps every day add up to big results. 💪",
    "Every expert was once a beginner. Keep going! 🚀",
    "Progress, not perfection. ✨",
    "Your only competition is who you were yesterday.",
    "Don't wait for the perfect moment — start now and make it perfect.",
]

FALLBACK = [
    "Hmm, I didn't get that 🤔 Type 'help' to see what I can do.",
    "Sorry, I don't understand that yet. Try 'help'.",
    "Interesting! But I'm still learning 😅 Type 'help' for options.",
]

HELP_TEXT = """**Things I can do:**
- 👋 Greet: hi, hello, hey, namaste
- 🙋 how are you / who are you
- 📛 my name is ___ / what is my name
- 🕒 time / 📅 date
- 😂 joke | 🧠 fact | 💡 quote
- 🎲 random number | 🪙 toss coin | 🎯 roll dice
- ➗ Math: 2+3*4, (10-2)/4
- 🙏 thanks | 👋 bye"""


# =====================================================
# ADDED: helper functions
# =====================================================
def calculate(expr):
    allowed = "0123456789+-*/(). "
    if not expr or "**" in expr or not any(c.isdigit() for c in expr):
        return None
    if not all(c in allowed for c in expr):
        return None
    if not any(op in expr for op in "+-*/"):
        return None
    try:
        result = eval(expr)
        return round(result, 4) if isinstance(result, float) else result
    except Exception:
        return None


def get_reply(text):
    msg = text.lower().strip()
    clean = "".join(c for c in msg if c.isalnum() or c.isspace())
    words = clean.split()
    name = st.session_state.user_name

    # math
    result = calculate(msg)
    if result is not None:
        return f"🧮 {msg} = **{result}**"

    # greetings
    if clean in GREETINGS:
        return random.choice([
            f"Hello {name}! 😊" if name else "Hello! 😊",
            "Hey there! 👋",
            "Namaste 🙏 How can I help?",
        ])

    if "how are you" in clean:
        return random.choice(["I'm doing great, thanks for asking! 😄 How about you?",
                              "All good here! What about you?"])

    if any(w in words for w in ["fine", "good", "great", "awesome"]) and len(words) <= 4:
        return "Glad to hear that! 😊"

    if "who are you" in clean or "your name" in clean:
        return "I'm a simple Streamlit chatbot 🤖 built with Python."

    # name memory
    if "my name is" in clean:
        new_name = clean.split("my name is", 1)[1].strip().title()
        if new_name:
            st.session_state.user_name = new_name
            return f"Nice to meet you, {new_name}! 🤝"

    if "what is my name" in clean or "whats my name" in clean:
        return f"Your name is {name} 😊" if name else "You haven't told me yet! Say 'my name is ___'."

    # time / date
    if "time" in words:
        return f"🕒 Current time: **{datetime.now().strftime('%I:%M %p')}**"
    if "date" in words or "day" in words:
        return f"📅 Today is **{datetime.now().strftime('%A, %d %B %Y')}**"

    # fun
    if any(w.startswith("joke") for w in words):
        return random.choice(JOKES)
    if any(w.startswith("fact") for w in words):
        return random.choice(FACTS)
    if any(w.startswith("quote") or w.startswith("motivat") for w in words):
        return random.choice(QUOTES)
    if "random" in words and "number" in words:
        return f"🎲 Your random number: **{np.random.randint(1, 101)}**"
    if "coin" in words or "toss" in words:
        return f"🪙 It's **{random.choice(['Heads', 'Tails'])}**!"
    if "dice" in words or "roll" in words:
        return f"🎯 You rolled a **{np.random.randint(1, 7)}**!"

    # help / thanks / bye
    if "help" in words:
        return HELP_TEXT
    if any(w in words for w in ["thanks", "thank", "thx", "shukriya", "dhanyavad"]):
        return random.choice(["You're welcome! 😊", "Anytime! 🙌", "Happy to help!"])
    if any(w in words for w in ["bye", "goodbye", "tata", "cya"]):
        return random.choice(["Bye! Have a great day 👋", "See you soon! 😊"])

    return random.choice(FALLBACK)


# =====================================================
# YOUR ORIGINAL CODE (unchanged)
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ADDED: remember user's name
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

user = st.chat_input("type something....")

if user:
    st.session_state.messages.append({"role": "user", "content": user})

    if user == "hi":
        st.session_state.messages.append({"role": "ai", "content": "hello"})

    elif user == "hello":
        st.session_state.messages.append({"role": "ai", "content": "hi"})

    # ADDED: handles every other message
    else:
        with st.spinner("🤖 typing..."):
            time.sleep(random.uniform(0.4, 1.0))
        st.session_state.messages.append({"role": "ai", "content": get_reply(user)})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# =====================================================
# ADDED: welcome message + sidebar
# =====================================================
if not st.session_state.messages:
    with st.chat_message("ai"):
        st.write("👋 Hi! I'm your chatbot. Type **help** to see what I can do.")

with st.sidebar:
    st.header("⚙️ Options")
    st.write(f"💬 Messages: {len(st.session_state.messages)}")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.session_state.user_name = ""
        st.rerun()
    st.markdown(HELP_TEXT)
