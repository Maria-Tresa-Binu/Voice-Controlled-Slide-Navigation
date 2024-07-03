from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth =GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
file1c = drive.CreateFile({'title': 'Hello.txt'})
file1.SetContentString('Hello World! this is a file')
file1.Upload()
