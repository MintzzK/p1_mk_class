import streamlit as st
from src.database.db import enroll_st_to_sub
from src.database.config import supabase

import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id=st.session_state.student_data['student_id']
    res= supabase.table('subjects').select('subject_id,name').eq('subject_code',subject_code).execute()
    #supabase ki 'subjects' table me se subid aur name nikaal lo aur subcode ko wo hamare enrolled sub code se equate kar do 
    if not res.data:
        st.error("Subject Code not Found!")
        if st.button("Close"):    #agar 'close' btn pr clk kr dia 
            st.query_params.clear      #clr query   
            st.rerun()
        
    subject=res.data[0]     #pehla col nikaal lete hai

    check=supabase.table("subject_students").select("*").eq("subject_id",subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:      #check.data se tables ka data nikala, aga humare data se match kar gaya (.eq) 
        st.info("You are already enrolled") # to u are enrolled
        if st.button("Got it!"):    #phir hum got it button pe clik kar denge
            st.query_params.clear()
            st.rerun()
        
        st.markdown(f"Would you linke to enroll in **{subject['name']}**?")

    col1,col2= st.columns(2)
    with col1:
        if st.button("No thanks"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Sure",type='primary',width='stretch'):  # yes then 
            enroll_st_to_sub('student_id',subject['subject_id']) # enroll in that sub
            st.success("Joined successfully")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()  
