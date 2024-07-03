import streamlit as sl
sl.title("Hi! this is Streamlit Web page")
sl.markdown("---")
sl.header("this is a header")
sl.subheader("this is a subheader")
sl.text("Hi this is for random text ")
sl.markdown("""
<style>
    .css-14xtw13.e8zbici0
    {
            visibility: hidden;
    } 
    .css-1lsmgbg.egzxvld0 
    {
            visibility: hidden;
    }
</style>            
""",unsafe_allow_html=True)
def change():
    print(sl.session_state.checker)
state=sl.checkbox("Checkbox",value=True,on_change=change,key="checker")
if state:
    sl.write("hi")
else:
    pass
radio_btn=sl.radio("where do you live",("US","UK","India"))
if radio_btn=="US":
    sl.write("Hope to see hyou soon there")
print(radio_btn)
def btn_click():
    radio_btn2=sl.radio("Please mention your gender",options=("male","female","others"))
btn=sl.button("Click Me")
if btn:
    btn_click()
sl.slider("this is slider",min_value=0,max_value=100)
v=sl.text_input("enter your college")
if v=="lbsitw":
    sl.text_input("enter your semester")

