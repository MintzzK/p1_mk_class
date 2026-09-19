import streamlit as st
from src.database.db import enroll_st_to_sub
from src.database.config import supabase 
import time
from src.database.db import create_attendance
import pandas as pd


def show_attendance_result(df,logs):
    st.write('Please review attendance before confirming')
    st.dataframe(df,hide_index=True,width='stretch')

    col1,col2=st.columns(2)

    with col1:
        if st.button("Discard",width='stretch'):
            st.session_state.voice_attendance_results=None
            st.rerun()                        #apne aap rerun hp jayga to attendance daal hi nahi payenge
    with col2:
        if st.button("Confirm & Save",width='stretch',type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images=[]
                st.session_state.voice_attendance_results= None
                st.rerun()

            # except Exception as e:
            #     st.error("Sync Failed!")
            # try:
            #     response = create_attendance(logs)
            #     st.write(response)
            except Exception as e:
                st.exception(e)     #in order to find what the exact prob is -----
                # Eg APIError: {'message': "Could not find the 'timespamp' column of 'attendance_logs' in the schema cache", 'code': 'PGRST204', 'hint': None, 'details': None}
                # matlab timespamp likh diya timestamp ke bajaye
@st.dialog("Attendance reports")
def attendance_result_dialog(df,logs):
    show_attendance_result(df,logs)