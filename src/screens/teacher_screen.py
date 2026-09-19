# session_state is the python inbuilt memory(dictionary) ,whereas teacher_login_type and teacher_register_type we use dict.key to get all the values associated with that key inside that dict

import librosa
import librosa.effects
import librosa

# y, sr = librosa.load("audio.wav")
# y_trim, _ = librosa.effects.trim(y)
import streamlit as st
from src.ui.bg import tr_bg 
from src.components.header import header_tr
from src.ui.bg import home_layout  #----------------ye general layout hai sari fonts, buttons ko overwrite kiya hua hai
from src.components.footer import footer_tr
from src.database.db import chk_tr_exst,create_tr,teacher_login, get_tr_sub
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from datetime import datetime
import numpy as np
from src.database.config import supabase
import pandas as pd
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import get_attendance_for_tr 

def teacher_screen():
    home_layout()
    tr_bg()

#ab humne directky tr screen se hi dono ko call kar diya 
# tr se tr logn ko call karo phir  ->> tr logn se tr reg ko call karo ->>  aur tr reg se tr login ko ----------ye sab jhanjhat khatam
    if "teacher_data" in st.session_state:
        tr_dshbd()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":      #agar login pe click nahi kiya ya login pe click kiya to login page pe hi raho
        teacher_screen_login()
    elif st.session_state.teacher_login_type =='register':       #======agar register pe click kiya to session state change ho kar register page ho jayegi
        teacher_screen_register()


def tr_dshbd():
    teacher_data= st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_tr()
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button("Logout",type='secondary',key='loginbkbtn',shortcut='control+backspace'):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()

    st.space()
    st.space()
    st.space()

    if "current_tr_tab" not in st.session_state:     #is method se hum var ko define karte se hi innclude(use) karlete hai
        st.session_state.current_tr_tab='take_attendance'        #agar koi bhi button selected nahi hai to  take attendance wale tab pe raho by default
    tab1, tab2, tab3= st.columns(3)

    #jese hi buttons ko click kiya session_state change ho jayegi

    with tab1:
        type1 = 'primary' if st.session_state.current_tr_tab =='take_attendance'else 'tertiary'

        if st.button("Take Attendance",type=type1, width='stretch',icon=":material/ar_on_you:"):
            st.session_state.current_tr_tab='take_attendance'
            st.rerun()
    
    with tab2:
        type2= 'primary' if st.session_state.current_tr_tab =='manage_subjects' else 'tertiary'
        if st.button("Manage Subject",type=type2, width='stretch',icon=":material/book_ribbon:"):
            st.session_state.current_tr_tab='manage_subjects'
            st.rerun()
    
    with tab3:
        type3= 'primary' if st.session_state.current_tr_tab =='attendance_records'else 'tertiary'
        if st.button("Attendance Records",type=type3, width='stretch',icon=":material/cards_stack:"):
            st.session_state.current_tr_tab='attendance_records'
            st.rerun()

    st.divider()



    #jo bhi btn clk kiya shn state to change hui hi saath me wo fn bhi call ho gaya  jis se naya tab khulega

    if st.session_state.current_tr_tab=='take_attendance':
        tr_tab_take_attendance()     #jese hi take_attendance wale button pe click kiya  is fn ko call kar denge 
    
    if st.session_state.current_tr_tab=='manage_subjects':
        tr_tab_manage_sub()

    if st.session_state.current_tr_tab=='attendance_records':
        tr_tab_attendance_rec()


    footer_tr()
     



# phir un fns ko bana bhi liya
#1==============================================================================================================================================
def tr_tab_take_attendance():
    teacher_id =st.session_state.teacher_data['teacher_id']
    st.header("Take AI attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]


    subjects=get_tr_sub(teacher_id)

    if not subjects:
        st.warning("You haven't created any subjects yet! Please create one to begin")
        return # return isliye taki ye cheez aage flow me na jaye
        
    subject_options ={f"{s['name']} - {s['subject_code']}":s['subject_id'] for s in subjects}
    col1,col2=st.columns(2)
    with col1:
        selected_sub_label= st.selectbox("Select Subject", options=list(subject_options.keys()))

    with col2:
        if st.button("Add Photos",icon=':material/photo_prints:',width='stretch'):
            add_photos_dialog()
        
    selected_subject_id= subject_options[selected_sub_label]
    
    st.divider()

    if st.session_state.attendance_images:
        st.header("added Photos")
        gallery_cols=st.columns(4)

        for idx,img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img,width='stretch',caption=f'Photo{idx+1}')
        has_photos=bool(st.session_state.attendance_images)
        c1,c2,c3=st.columns(3)

        with c1:
            if st.button("Clear all Photos",width='stretch',icon=':material/delete:', disabled=not has_photos):
                st.session_state.attendance_images=[]   #is se att img clear ho jayega
                st.rerun()


        with c2:
            
            if st.button("Run Face Analysis",width='stretch',type='secondary',icon=':material/analytics:'):
                with st.spinner('Deep scanning classroom photos...'):
                    all_detected_id={}
                    
                    for idx,img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB'))    #image ko rgb format me convert kar diya fo easy analysis 

                        detected,_,_=predict_attendance(img_np)

                        if detected:
                            for sid in detected.keys():
                                student_id=int(sid)

                                all_detected_id.setdefault(student_id,[]).append(f"Photo{idx+1}")
                    
                    enrolled_res = supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()
                    enrolled_students= enrolled_res.data

                    results,attendance_to_log=[],[]

                    if not enrolled_students:
                        st.warning('No students enrolled in this course')

                    else:
                        current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")   #currtmstmp me datetime.now se us inst ka time note kar lenge


                        for node in enrolled_students:
                            student = node['students']
                            sources= all_detected_id.get(int(student['student_id']),[])   # empty array isliye kia agar mltpl srcs se dikha wo insaan to wo wala count is array me aata jayega  
                            is_present=len(sources)>0  # agar 0 se zyada baar present hai to is vaar me store karao

                            results.append({
                                "Name":student['name'],
                                "ID": student['student_id'],
                                "Source":", ".join(sources) if is_present else "-",   #join karne ke sources batayega(kaun se pics me se) aur nahi kiya join to '-' dikhayega
                                "Status":"✅ Present" if is_present else "❌ Absent"
                            })

                            attendance_to_log.append({
                                'student_id':student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp':current_timestamp,
                                'is_present': bool(is_present)
                                
                            })
                    attendance_result_dialog(pd.DataFrame(results),attendance_to_log)
        with c3:
            if st.button("Use Voice Attendance", type='primary',width='stretch',icon=":material/mic:"):
                voice_attendance_dialog(selected_subject_id)


#2============================================================================================================================================================
def tr_tab_manage_sub():
    teacher_id=st.session_state.teacher_data['teacher_id']
    c1,c2=st.columns(2)
    with c1:
        st.header("Manage Subjects", width='stretch')

    with c2:
        if st.button("Create new subject", type='primary',width='stretch'):
            create_subject_dialog(teacher_id)

    #List of all subjects
    subjects=get_tr_sub(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("👥","Students",sub['total_students']),
                ("🕰️","Classes",sub['total_classes']),
            ]
        
        def share_btn():
            if st.button(f"Share Code:{sub['name']}",key=f"share_{sub['subject_code']}",icon=':material/share:'):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()

        # def share_btn():
        #     if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
        #         share_subject_dialog(sub['name'], sub['subject_code'])
        #     st.space()

        subject_card(
            name=sub['name'],
            code= sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("NO SUBJECTS FOUND. CREATE  ONE ABOVE")





#3 ===============================================================================================================================================
def tr_tab_attendance_rec():
    st.header("Attendance Records")
    teacher_id= st.session_state.teacher_data['teacher_id']
    records =get_attendance_for_tr(teacher_id)



    # st.write("Teacher ID:", teacher_id)

    # records = get_attendance_for_tr(teacher_id)

    # st.write(records)

    if not records:
        return
    


    
    data=[]
    # st.write(records)
    for r in records:
        ts=r.get('timestamp')

        data.append({
            'ts_group':ts.split(".")[0] if ts else None,
            'Time':datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",    #is is 'iso' format not 'is' format
            'Subject':r['subjects']['name'],
            'Subject Code':r['subjects']['subject_code'],
            'is_present':bool(r.get('is_present',False))
        })

    df= pd.DataFrame(data)      #pandas me data compute karenge -kitni classes lagi, kitne present the 

    summary=(
        df.groupby(['ts_group','Time','Subject','Subject Code'])
        .agg(
            Present_Count=('is_present','sum'),
            Total_Count=('is_present','count')
        ).reset_index()     #taki grouby ki wajah se jo bhi kuchh table ka str change hua wo fix ho jaye
    )

    summary['Attendance Stats']=(
        "✅" + summary['Present_Count'].astype(str)+"/"
        +summary['Total_Count'].astype(str)+'Students'
    )

    display_df= (summary.sort_values(by='ts_group',ascending=False)
                [['Time','Subject','Subject Code','Attendance Stats']]
                )
    st.dataframe(display_df,width='stretch',hide_index=True)












def login_tr(tr_usrnm,tr_pswd):
    if not tr_usrnm or not tr_pswd:
        return False
    
    teacher= teacher_login(tr_usrnm, tr_pswd)
    if teacher:
        st.session_state.user_role="teacher"   #abhi teacher login kar  raha hai to user role is tr
        st.session_state.teacher_data=teacher  #<<<<<"teacher" nahi sirf teacher (string nahi dict)>>>>>#jo bhi hume database se data mil raha hai use teacher me daal denge
        st.session_state.is_logged_in=True
        return True
    return False



def teacher_screen_login():   #upar 2 col usme header aur back btn -> header-> divider-> 2 col login/register

#tr_scr_login me humne registr_scr ko call kiya . tr_sc me nahi kiya kyunnki by defaulty login ke neeche register ka saction bhi aa jaataa
    

    c1,c2=st.columns(2, vertical_alignment="center", gap='xxlarge')
    with c1:
        header_tr()
    with c2:
        if st.button("Go back to Home", type="secondary",key="loginbackbutton", shortcut="CTRL+backspace",width="stretch"): #==========button ko keys dena padhti hai taki wo apni value lose na kare
            st.session_state['login_type']=None
            st.rerun()                             #jab bhi state change hota hai rerun(refresh) karte hai
    
    st.header("Login using password", text_alignment='center')
    
    st.space() #---------header aur usrnm k beech me gap  
    st.space()

    tr_usrnm = st.text_input("Enter username", placeholder="@MintzzK", key='usrnm') #===========placeholder basically is the text which will show when nothing is typed
    tr_pswd=st.text_input("Enter your password", type="password", placeholder="Enter password", key='pswd')   #password type is imp in order to apply 'hide' feature

    st.divider() #-------------this is basically a line (upar aur neeche wale part ko separate karne k liye)
    
 
    col1, col2 =st.columns(2)
    with col1:
        if st.button("Login", icon=':material/passkey:', shortcut="control+enter", width="stretch"):  #button name, its icon and its shortcut
            if login_tr(tr_usrnm, tr_pswd):
                st.toast("welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun
            else:
                st.error("Invalid username and password")
    

    with col2:
        if st.button("Register Instead", type="secondary", icon=":material/passkey:", width="stretch"):   # USE '::' ALWAYS WHILE MENTIONING ICON of a button
            st.session_state.teacher_login_type='register'
            st.rerun()
    footer_tr()








def register_teacher(trnm,tr_usrnm,tr_pswd,tr_cnfrm_pswd):
    if not tr_usrnm or not tr_pswd or not trnm:     #agar humne in sections  ko nahi bhara to ye msg aayega
        return False, "All fields are required"
    if chk_tr_exst(tr_usrnm):
        return False, "Username already exists"
    if tr_pswd != tr_cnfrm_pswd:
        return False, "Password doesn't match"

    try:                                          #kisi bhi reason se fail ho gaya , high traffic of database or pooling of database etc
        create_tr(tr_usrnm,tr_pswd,trnm)
        return True, "Successfully Created! Login Now"
    except Exception as e:                      # <<<<<'Exception' with capital E >>>> kisi bhi wajah se agar nahi ban paya to ye  error dikha  dega
        return False, f"Unexpected error {str(e)}"



def teacher_screen_register():         #upar 2 col usme header aur back btn -> header


    c1,c2=st.columns(2, vertical_alignment="center", gap='xxlarge')
    with c1:
        header_tr()
    with c2:
        if st.button("Go back to home page", key='hi'):
            st.session_state['login_type']=None
            st.rerun()                               #jab bhi state change hota hai rerun(refresh) karte hai
     
    
    st.header("Register yout teacher profile")

    st.space() #---------header aur usrnm k beech me gap  
    st.space()

    tr_usrnm = st.text_input("Enter username", placeholder="@MintzzK") #===========placeholder basically is the text which will show when nothing is typed
    trnm=st.text_input("Enter your name",placeholder="MK" )
    tr_pswd=st.text_input("Enter your password", type="password", placeholder="Enter password")   #password type is imp in order to apply 'hide' feature
    tr_cnfrm_pswd=st.text_input("Confirm your password",type="password" ,placeholder="re-enter your password")

    st.divider() #-------------this is basically a line (upar aur neeche wale part ko separate karne k liye)
    
 
    col1, col2 =st.columns(2)
    with col1:
        if st.button("Register Now", icon=':material/passkey:', shortcut="control+enter", width="stretch"):  #button name, its icon and its shortcut
            success,message = register_teacher(trnm,tr_usrnm,tr_pswd,tr_cnfrm_pswd)
            if success:
                st.success(message)    #is fn se ek gren ka colour ka pop up ata hai ki successful login  smth smth
                import time  #importing time module
                time.sleep(2) # ye pop up hum 2 sec ke liye daal rehe hai
                st.session_state.teacher_login_type ="login"
                st.rerun()
            else:
                st.error(message)

    with col2:
        if st.button("Login Instead", type="secondary", icon=":material/passkey:", width="stretch"):   # USE '::' ALWAYS WHILE MENTIONING ICON of a button
            st.session_state.teacher_login_type='login'
            st.rerun()
    footer_tr()

    
