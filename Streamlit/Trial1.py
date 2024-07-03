import streamlit as st
import speech_recognition as sr
import pyttsx3
import pyautogui
from pptx import Presentation

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load PowerPoint presentation
presentation = Presentation("your_presentation.pptx")
slide_count = len(presentation.slides)

def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        st.write(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        st.write("Sorry, I didn't catch that.")
        return None

def change_slide(command):
    global current_slide
    if 'next' in command:
        current_slide = min(current_slide + 1, slide_count - 1)
    elif 'previous' in command:
        current_slide = max(current_slide - 1, 0)
    pyautogui.press('right')  # Simulate right arrow key press

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    st.title("Voice Controlled PowerPoint")
    global current_slide
    current_slide = 0

    while True:
        command = recognize_speech()
        if command:
            change_slide(command)
            speak(f"Slide {current_slide + 1} of {slide_count}")

if __name__ == "__main__":
    main()
