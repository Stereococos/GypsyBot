import streamlit as st
import librosa
import soundfile as sf
import os
import json

# ---------------------
# GYPSYBOT - YOUR GUITAR MENTOR
# ---------------------

st.set_page_config(page_title="GypsyBot - Jazz Guitar Tutor", layout="centered")

st.title("GypsyBot")
st.subheader("Your mentor for swing, gypsy jazz, and blues guitar")

# ---------------------
# USER SESSION & PROGRESS
# ---------------------

user = st.text_input("Enter your name to save your progress:")

data_file = f"{user.lower().strip()}_progress.json" if user else None
progress = {}

if user:
    try:
        with open(data_file, "r") as f:
            progress = json.load(f)
    except FileNotFoundError:
        progress = {"level": "Beginner", "lesson": 1}

# ---------------------
# LESSON MODULE
# ---------------------

st.markdown("### Current Lesson")

lessons = {
    1: {
        "title": "II–V–I Chord Progression in C",
        "content": """
        **Goal:** Learn the common II–V–I progression in jazz.

        **Chords:**
        - Dm7
        - G7
        - Cmaj7

        **Instruction:** 
        Play the chords using a swing rhythm, emphasizing beats 2 and 4. Use basic comping with palm muting if possible.
        """
    },
    2: {
        "title": "Swing Rhythm with Metronome",
        "content": """
        **Goal:** Feel the swing groove in 4/4 time.

        **Instruction:**
        Practice with a metronome at 85 BPM, emphasizing beats 2 and 4. Use palm muting for control.
        """
    }
}

current_lesson = progress.get("lesson", 1)
st.markdown(f"**{lessons[current_lesson]['title']}**")
st.markdown(lessons[current_lesson]['content'])

# ---------------------
# UPLOAD PRACTICE AUDIO (OPTIONAL)
# ---------------------

st.markdown("### Upload Practice Recording (Optional)")

audio_file = st.file_uploader("Upload your recording (.wav or .mp3)", type=["wav", "mp3"])

def evaluate_audio(file, target_bpm=85):
    y, sr = librosa.load(file, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    feedback = f"- Duration: {duration:.2f} seconds\n- Detected tempo: {tempo:.1f} BPM\n"
    if abs(tempo - target_bpm) > 5:
        feedback += f"You're off tempo. Try practicing at {tempo - 5:.1f} BPM for better control."
    else:
        feedback += "Great timing! Keep it up."
    return feedback

if audio_file is not None:
    st.audio(audio_file)
    with open("temp.wav", "wb") as f:
        f.write(audio_file.getbuffer())
    st.markdown("### Performance Feedback")
    feedback = evaluate_audio("temp.wav")
    st.text(feedback)
    os.remove("temp.wav")

# ---------------------
# ADVANCE TO NEXT LESSON
# ---------------------

if user and st.button("Complete Lesson and Continue"):
    progress["lesson"] = min(progress["lesson"] + 1, len(lessons))
    with open(data_file, "w") as f:
        json.dump(progress, f)
    st.success("Lesson completed! Refresh to view the next one.")

# ---------------------
# METRONOME
# ---------------------

st.markdown("### Practice Metronome")
bpm = st.slider("Select tempo (BPM)", min_value=60, max_value=160, value=85)
if st.button("Play metronome"):
    st.audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg")

# ---------------------
# COMPOSITION MODULE
# ---------------------

st.markdown("### Start a New Composition")

style = st.selectbox("Choose a style:", ["Jazz", "Blues", "Gypsy Jazz"])
key = st.selectbox("Choose a key:", ["C", "D", "E", "F", "G", "A", "B"])

if st.button("Generate Composition Idea"):
    if style == "Jazz":
        chords = f"{key}maj7 - A7 - Dm7 - G7"
        melody = f"Try a phrase using the {key} major scale with a chromatic passing tone."
        bpm_suggested = 95
    elif style == "Blues":
        chords = f"{key}7 - {key}7 - {key}7 - {key}7\n{key[0]}7 - {key[0]}7 - {key}7 - {key}7"
        melody = f"Try using the {key} minor pentatonic scale with a bluesy bend on the flat 5."
        bpm_suggested = 80
    else:  # Gypsy Jazz
        chords = f"{key}m6 - D9 - Gmaj7 - E7"
        melody = f"Use harmonic minor and arpeggios for that gypsy sound."
        bpm_suggested = 120

    st.markdown(f"**Suggested Chord Progression:** `{chords}`")
    st.markdown(f"**Melodic Idea:** {melody}")
    st.markdown(f"**Suggested BPM:** {bpm_suggested} BPM")

st.info("GypsyBot is evolving. Stay tuned for backing tracks, tablature, and full composition exports!")