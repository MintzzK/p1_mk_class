import streamlit as st
from src.database.db import create_subject
from src.database.config import supabase
from src.database.db import enroll_st_to_sub
import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code to enroll")
    join_code =st.text_input("Subject Code", placeholder='CS101')   #>>>>>>>code enter kiya

    if st.button("Enroll now",type='primary',width='stretch'):
        if join_code:     #agar code diya
            res =supabase.table("subjects").select("subject_id,name,subject_code").eq("subject_code",join_code).execute()
             # .eq se equate kar diya subject code ko us code se  jo humne enter kiya tha
            if res.data:     #agar data hai supabase me      #agar subject mila
                subject=res.data[0]   #to use subject var me daal do
                student_id =st.session_state.student_data['student_id']

                check=supabase.table("subject_students").select('*').eq("subject_id", subject['subject_id']).eq("student_id",student_id).execute()
                if  check.data:     #chack karenge already enrolled?
                    st.warning("You are already enrolled in this programm")
                else:
                    enroll_st_to_sub(student_id, subject['subject_id'])
                    st.success("Successfully Enrolled")
                    time.sleep(1)
                    st.rerun()

            else:
                st.warning("Subject not found!")
        else:
            st.warning("Please enter the Subject code")


