import streamlit as st

from src.ui.bg import st_bg
from src.ui.bg import home_layout
from src.components.header import header_st
from src.components.footer import footer_st
from PIL import Image   #short for  pillow
import numpy as np
from src.database.db import get_all_st , create_st    #create_st aur create_student me diff aa  gaya
from src.pipelines.face_pipeline import get_face_embeddings, predict_attendance , train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
import time
from src.database.db import get_all_st, create_st, get_student_subjects,get_student_attendance, unenroll_st_to_sub 
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card 
# from src.components.dialog_auto_enroll import auto_enroll_dialog




def st_dshbd():

    student_data= st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_st()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout",type='secondary',key='loginbkbtn',shortcut='control+backspace'):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1,c2=st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    
    with c2:
        if st.button("Enroll in subject",type='primary',width='stretch'):
            enroll_dialog()

    st.divider()
    with st.spinner("Loading your enrolled subjects"):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendance(student_id)

    stats_map={}

    for log in logs:
        sid=log['subject_id']

        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
        stats_map[sid]['total']+=1

        if log.get('is_present'):
            stats_map[sid]['attended']+=1

    cols=st.columns(2) #<<<<<<<<<<<<<<<<<<<<single var me hi dono col define kar diye>>>>>>>
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub['subject_id']

        stats=stats_map.get(sid,{"total":0,"attended":0})

        def unenroll_btn():
            if st.button("Unenroll from this course",type='tertiary', width='stretch'):
                unenroll_st_to_sub(student_id,sid)
                st.toast(f"Unenroll from {sub['name']} successfully")
        with cols[i % 2]:
            subject_card(   
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("🗓️","Total",stats['total']),
                    ("✅","Attended",stats['attended']),
                ],
                footer_callback=unenroll_btn 
            )
                    
    footer_st()

def student_screen():
    st_bg()
    home_layout()

    if "student_data" in st.session_state:
        st_dshbd()
        return

    c1,c2= st.columns(2,vertical_alignment="center", gap='xxlarge')
    with c1:
        header_st()
    
    with c2:
        if st.button("Go back to Home", type="secondary",key="loginbackbutton", shortcut="CTRL+backspace",width="stretch"): #==========button ko keys dena padhti hai taki wo apni value lose na kare
            st.session_state['login_type']=None
            st.rerun()                             #jab bhi state change hota hai rerun(refresh) karte hai
    
    st.header("Login using Face ID",text_alignment='center')
    st.space()
    st.space()
    
    show_registration= False #by default ise non working rakhennge

#keeeeeeeeeeeeeeeeeeeeeeeeeeeoppppppppppppjio
    students = get_all_st()
    # st.write(students)
    # st.write("hello")

    photo=st.camera_input("Position your face at the center")
    if photo:
        img=np.array(Image.open(photo))  #while dealing with image in python , always use image.open()
        with st.spinner("AI is scanning.."):
            detected, all_ids, num_faces= predict_attendance(img)

            if num_faces==0:
                st.warning("Face not found!")
            elif num_faces>1:
                st.warning("Multiple faces found")
            else:
                # student=None
                if detected:
                    student_id=list(detected.keys())[0]
                    all_st =get_all_st()
                    student= next((s for s in all_st if s['student_id']== student_id),None)
                
                    if student:
                        st.session_state.is_logged_in= True
                        st.session_state.user_role='student'
                        st.session_state.student_data= student
                        st.toast(f"Welcome Back {student['name']}")
                        import time
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("New face recognised! Register your profile!")
                    show_registration= True 

    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile")
            new_name=st.text_input("Enter your name", placeholder='MK')

            st.subheader("Optional: Voice Enrollment")
            st.info("Enroll for voice only attendance")

            audio_data= None #by def koi audio nahi hai

            try:
                audio_data=  st.audio_input("Record your voice for Eg say 'I am present, my name is  MK' ") #then audio is recorded
                if audio_data is not None:     #agar kuchh value hai audio ki
                    audio_data = audio_data.read()      # ************* to .read() se hum audio ko object se bytes me convert kar denge
            except Exception as e:
                # st.error("Audio  data failed")
                st.error(e)

            if st.button("Create Account", type="primary"):
                if new_name:
                    with st.spinner("Create new profile"): #jab tak profile  naahi  ban jati tab tak ye spinner ghoomta rahega
                        img=np.array(Image.open(photo))
                        encodings= get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()
                            voice_emb= None
                            if audio_data:
                                voice_emb =get_voice_embedding(audio_data)
                                response_data=create_st(new_name,
                                                     face_embedding=face_emb,
                                                     voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in= True
                                st.session_state.user_role='student'
                                st.session_state.student_data =response_data[0]
                                st.toast(f"Profile Created! Hi {new_name}!")
                                import time
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Couldn't capture your facial features for registation")

                else:
                    st.warning("Please enter your name")
    footer_st() 
