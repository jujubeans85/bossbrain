import streamlit as st
import json
import os
import random
from datetime import datetime, timedelta

PROGRESS_FILE = 'progress.json'

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'streak': 0, 'last_date': None, 'scores': {'memory': 0, 'math': 0}, 'total_games': 0}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

def update_streak(progress):
    today = datetime.now().strftime('%Y-%m-%d')
    if progress['last_date'] != today:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if progress['last_date'] == yesterday:
            progress['streak'] += 1
        else:
            progress['streak'] = 1
        progress['last_date'] = today
    return progress

def memory_game(progress):
    st.subheader("🧠 Memory Game")
    items = random.sample(['apple', 'river', 'shadow', 'violin', 'jasmine', 'cloud', 'zebra'], 5)
    st.write("Memorize: ", ', '.join(items))
    st.button("Start Recall", on_click=st.rerun)
    user_input = st.text_input("Recall items (comma-separated):")
    if user_input:
        recalled = [w.strip() for w in user_input.lower().split(',')]
        correct = len(set(recalled) & set([i.lower() for i in items]))
        score = (correct / 5) * 100
        st.metric("Score", f"{score:.0f}%")
        progress['scores']['memory'] += score
        progress['total_games'] += 1
        return score >= 70
    return False

def math_game(progress):
    st.subheader("➕ Math Game")
    score = 0
    for i in range(3):
        a, b = random.randint(1, 10), random.randint(1, 10)
        answer = a + b
        user = st.number_input(f"{a} + {b} = ", key=f"q{i}", step=1)
        if user == answer:
            score += 1
    pct = (score / 3) * 100
    st.metric("Math Score", f"{pct:.0f}%")
    progress['scores']['math'] += pct
    progress['total_games'] += 1
    return pct >= 70

st.set_page_config(page_title="Danielle's Brain Boost", layout="wide")

st.title("🧠 Danielle's Brain Boost")
st.subheader("🎨 Upload Your South Park Avatar")

uploaded_img = st.file_uploader("Drop an image (PNG/JPG)", type=["png", "jpg", "jpeg"])
if uploaded_img:
    st.image(uploaded_img, caption="Your uploaded character!", use_column_width=True)
    os.makedirs("images", exist_ok=True)
    with open(f"images/{uploaded_img.name}", "wb") as f:
        f.write(uploaded_img.getbuffer())

progress = load_progress()
progress = update_streak(progress)

st.sidebar.title("📊 Stats")
st.sidebar.metric("🔥 Streak", f"{progress['streak']} days")
st.sidebar.metric("🧠 Memory Score", f"{progress['scores']['memory']:.0f}")
st.sidebar.metric("➕ Math Score", f"{progress['scores']['math']:.0f}")
st.sidebar.metric("🎮 Games", progress['total_games'])

st.write("Choose your game mode:")
mode = st.selectbox("Game Mode", ["Memory", "Math"])

if mode == "Memory":
    if memory_game(progress):
        st.success("Great job! 🎉")
elif mode == "Math":
    if math_game(progress):
        st.success("You're crushing it! 💪")

save_progress(progress)
