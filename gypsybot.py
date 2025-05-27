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

# ---------------------
# Lesson 1 – Practice Examples
# ---------------------

st.markdown("### Lesson 1 – Practice Examples")

st.markdown("**Comping Example**")
st.audio("lesson1_comping.wav")

st.markdown("**Melodic Line Example**")
st.audio("lesson1_melody.wav")

st.markdown("**Backing Track**")
st.audio("lesson1_backing.wav")

st.markdown("**View Tablature**")
st.text(open("lesson1_tab.txt", "r").read())
# ---------------------
# Lesson 1 – Practice Examples
# ---------------------

st.markdown("### Lesson 1 – Practice Examples")

st.markdown("**Comping Example**")
st.audio("https://raw.githubusercontent.com/Stereococos/GypsyBot/main/lesson1_comping.wav")

st.markdown("**Melodic Line Example**")
st.audio("https://raw.githubusercontent.com/Stereococos/GypsyBot/main/lesson1_melody.wav")

st.markdown("**Backing Track**")
st.audio("https://raw.githubusercontent.com/Stereococos/GypsyBot/main/lesson1_backing.wav")

st.markdown("**View Tablature**")
st.text("""
Lesson 1 – II–V–I in C major
Comping:
Dm7      G7       Cmaj7
e|---5----3--------0---|
B|---6----3--------0---|
G|---5----4--------0---|
D|---7----3--------2---|
A|---5----5--------3---|
E|---x----3--------x---|

Melodic line example:
e|--------------------|
B|---5--6--8--10------|
G|--------------------|
D|--------------------|
A|--------------------|
E|--------------------|
""")

st.markdown(lessons[current_lesson]['content'])


st.markdown("### Lección 1 – Ejemplos de práctica")

st.markdown("**Ejemplo de Comping**")
st.audio("https://raw.githubusercontent.com/Stereococos/GypsyBot/main/lesson1_comping.wav")

st.markdown("**Ejemplo de Línea Melódica**")
st.audio("https://raw.githubusercontent.com/Stereococos/GypsyBot/main/lesson1_melody.wav")

st.markdown("**Backing Track**")
st.audio("https://raw.githubusercontent.com/Stereococos/GypsyBot/main/lesson1_backing.wav")

st.markdown("**Ver Tablatura**")
st.text("""
Lección 1 - II–V–I en Do mayor
Comping:
Dm7      G7       Cmaj7
e|---5----3--------0---|
B|---6----3--------0---|
G|---5----4--------0---|
D|---7----3--------2---|
A|---5----5--------3---|
E|---x----3--------x---|

Ejemplo de línea melódica:
e|--------------------|
B|---5--6--8--10------|
G|--------------------|
D|--------------------|
A|--------------------|
E|--------------------|
""")
st.markdown("### Lesson 1 – Practice Examples")

st.markdown("**Comping Example**")
st.audio("https://example.com/audio/lesson1_comping.wav")

st.markdown("**Melodic Line Example**")
st.audio("https://example.com/audio/lesson1_melody.wav")

st.markdown("**Backing Track**")
st.audio("https://example.com/audio/lesson1_backing.wav")

st.markdown("**View Tablature**")
st.text("""
Lesson 1 - II–V–I in C major
Comping:
Dm7      G7       Cmaj7
e|---5----3--------0---|
B|---6----3--------0---|
G|---5----4--------0---|
D|---7----3--------2---|
A|---5----5--------3---|
E|---x----3--------x---|

Melodic line example:
e|--------------------|
B|---5--6--8--10------|
G|--------------------|
D|--------------------|
A|--------------------|
E|--------------------|
""")
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
# st.audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg")

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
