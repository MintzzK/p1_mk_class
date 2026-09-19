import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    # is se sabse upar link ki jagah app ka title aur logo dikhega
    st.set_page_config(
        page_title="MK Class- Making Attendance faster using AI",
        page_icon="https://i.pinimg.com/736x/82/92/d7/8292d7783cec70bd9e0671f9230eb1c0.jpg"
    )

    if "login_type" not in st.session_state: #"If we haven't created the login_type variable yet, create it now and set it to None (nobody logged in).
        st.session_state['login_type'] = None
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

    join_code=st.query_params.get("join_code")
    if join_code:
        if st.session_state.login_type!= 'student':            #agar student bankar login nahi hai 
            st.session_state.login_type='student'              # to student ki taraah login karo
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role')=='student':    #agar logged in hi hai as as a student
            auto_enroll_dialog(join_code)                       #to auto subject me enroll ka khul jayega face recognition karte se hi

main()            
