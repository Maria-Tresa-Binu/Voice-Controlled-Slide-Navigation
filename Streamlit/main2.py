import streamlit as st

file=st.file_uploader('Upload your file here',type='jpg')
if file is not None:
    st.image(file)

text=st.text_input("Cource description",max_chars=100)
print(text)
text2=st.text_area("Extracurricular",max_chars=200)
val2=st.date_input("DOB")
print(val2)
