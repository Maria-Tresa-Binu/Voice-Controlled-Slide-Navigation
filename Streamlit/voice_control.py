import streamlit as st
import os
import time
import threading
import speech_recognition as sr
import win32com.client

def control_powerpoint(ppt_path):
    if os.path.exists(ppt_path):
        app = win32com.client.Dispatch("PowerPoint.Application")
        presentation = app.Presentations.Open(FileName=ppt_path, ReadOnly=1)
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            command = recognizer.recognize_google(audio, language="en-US")
            st.write("You said:", command)
            if 'next' in command:
                presentation.SlideShowWindow.View.Next()
                st.write("Moving to the next slide...")
            elif 'previous' in command:
                presentation.SlideShowWindow.View.Previous()
                st.write("Moving to the previous slide...")
            else:
                st.write("No valid command recognized.")
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand. Please try again.")
    else:
        st.error("Error: Presentation file does not exist at the specified location.")

def open_ppt(ppt_path):
    threading.Thread(target=control_powerpoint, args=(ppt_path,), daemon=True).start()

def main():
    st.title("PowerPoint Presentation Controller")
    ppt_path = st.file_uploader("Upload PowerPoint Presentation", type=["pptx"])
   
    if ppt_path:
        file_name=ppt_path.name
        if not os.path.exists("temp_files"):
            os.makedirs("temp_files")
        #os.path.join("temp_files",file_name)
        if not os.path.exists(file_name):
            with open(os.path.join("temp_files", file_name), "wb") as f:
                f.write(ppt_path.getvalue())
                file_path=os.path.join("temp_files",file_name)
        else:
            file_path=os.path.join("temp_files",file_name)

        print(file_path)
        reversed_path = file_path.replace("/", "\\")
        open_ppt(reversed_path)

if __name__ == "__main__":
    main()

