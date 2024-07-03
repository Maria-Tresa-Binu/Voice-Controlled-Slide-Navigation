import streamlit as st
import os
import speech_recognition as sr
import win32com.client
import time
import pythoncom
import qrcode
from google.Google import Create_Service
from PIL import Image
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import cv2
import time
import pyautogui
pythoncom.CoInitialize()
global reversed_path

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=2)
    try:
        command = r.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        st.warning("Sorry, couldn't understand. Please try again.")
        return None

def set_clickedQR():
        st.session_state.clicked=True
def upload_to_drive(project_name,ppt):
            # Replace the CLIENT_SECRET_FILE path with your own client secret file
            CLIENT_SECRET_FILE = 'client-secret.json'
            API_NAME = 'drive'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/drive']

            # Create Google Drive service
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

            # Extract file name from path
            #file_name = os.path.basename(ppt)

            # Create file metadata
            file_metadata = {'name': project_name}

            # Upload the file to Google Drive
            media = MediaFileUpload(ppt, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            file_id = file.get("id")

            # Set permission for file (optional)
            request_body = {
                'role': 'reader',
                'type': 'anyone'
            }
            response_permission = service.permissions().create(
                fileId=file_id,
                body=request_body
            ).execute()

            # Get webViewLink of the uploaded file
            rlink = service.files().get(
                fileId=file_id,
                fields='webViewLink'
            ).execute()
            link = rlink.get('webViewLink')
            return link
def slideControl(reversed_path):
        

    st.session_state.clicked=True
    

    if st.session_state.clicked:
            app = win32com.client.Dispatch("PowerPoint.Application")
            presentation = app.Presentations.Open(reversed_path, ReadOnly=1)
            st.info("Speak commands to control the presentation.")
            st.warning("Say 'Next' to go to the next slide or 'Previous' to go to the previous slide.")
            while True:
                command = recognize_speech()
                if command is not None:
                    if command == 'next':
                        presentation.SlideShowWindow.View.Next()
                        st.write('Moving to the next slide...')
                    elif command == 'previous':
                        presentation.SlideShowWindow.View.Previous()
                        st.write('Moving to the previous slide...')
                    elif command == 'thank you':
                        st.success("Thank you! Presentation control ended.")
                        break
                    else:
                        st.write("Unknown command:", command)
    else:
        st.warning("Please upload a PowerPoint presentation file.")
    st.session_state.clicked=False

     
def QRCode(project_name,reversed_path):
     st.session_state.clicked=True
     if st.session_state.clicked:
        link = upload_to_drive(project_name,reversed_path)
        qr = qrcode.make(link)
        print(link)
        x=project_name.split(".")
        pname=x[0]
        image_name = pname+'.png'
        image_path = os.path.join('imageqr', image_name)
        os.makedirs('imageqr', exist_ok=True)
        qr.save(image_path)
        final_img = cv2.imread(image_path)
        cv2.imwrite("ppt_qrcode.png", final_img)
        final_img = Image.open("ppt_qrcode.png")
        st.image(final_img, caption='Scan this QR code to get your presentation')
     st.session_state.clicked=False

def Timer():
    #st.write("Enter the time in minutes ")
    total_mins = st.number_input("Enter time (in minutes):",min_value=3, step=1)
    total_seconds=total_mins*60
    if total_seconds < 0:
        st.error("Please enter a positive integer for time")
        return
    for remaining_time in range(total_seconds, 0, -1):
        minutes, seconds = divmod(remaining_time, 60)
        timer_text = f"Time remaining: {minutes:02d}:{seconds:02d}"
        pyautogui.alert(timer_text, title="Countdown Timer", timeout=1)  # Display timer as an alert
        time.sleep(1)
        if minutes<2:
            break
    pyautogui.alert("2 minute remaining!", title="Countdown Timer")  # Display time's up message

        
def main():
    st.title("Slide Sync")
    
    project_file = st.file_uploader("Upload PowerPoint Presentation", type=["pptx"])
    cwd=os.getcwd()
    if project_file:
            #prs=Presentation(project_file)
            project_name = project_file.name
            file_path=os.path.join(cwd,"temp_files",project_name)
            reversed_path = file_path.replace("/", "\\")
            check_file = os.stat(reversed_path).st_size
            if check_file==0:
                with open(os.path.join("temp_files", project_name), "wb") as f:
                    f.write(project_file.getvalue())
            st.success(f"Presentation '{project_name}' uploaded successfully.")
            #file_path=os.path.join(cwd,"temp_files",project_name)
            #reversed_path = file_path.replace("/", "\\")
            print(reversed_path)
            but1=st.button("PowerPoint Presentation Controller") #on_click=slideControl(reversed_path)
            if but1:
                 slideControl(reversed_path)
            but3=st.button("QR Code Generation")  #on_click=QRCode(project_name,reversed_path)
            if but3:
                QRCode(project_name,reversed_path)
            but2=st.button("Timer")
            if but2:
                 Timer()
    
            
        



if __name__ == "__main__":
    if not os.path.exists("temp_files"):
        os.makedirs("temp_files")
    main()
