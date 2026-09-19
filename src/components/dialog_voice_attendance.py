import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase 
from datetime import datetime
import numpy as np
import pandas as pd
from src.components.dialog_attendance_results import show_attendance_result
import librosa
import librosa.effects

@st.dialog("Voice Attendance")

def voice_attendance_dialog(selected_subject_id):
    st.write('Record your voice sample with -"I am Present"')
    audio_data=None
    audio_data=st.audio_input("Record classroom audio")
    # st.write(audio_data)      ye batayega ki audio rec hua ki nahi by -- None/ Uploaded file

    if st.button("Analyze audio",width='stretch',type='primary'):
        with st.spinner("Processing audio data"):
            enrolled_res= supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()
            enrolled_students= enrolled_res.data

            if not enrolled_students:
                st.warning("No student enrolled in this course")
                return
            candidates_dict={
                s['students']['student_id']:  s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }
# =====================================================
            # for sid, embedding in candidates_dict.items():
            #     st.write("Student ID:", sid)
            #     st.write("Embedding type:", type(embedding))
            #     st.write("Embedding length:", len(embedding))

            # for sid, stored_embedding in candidates_dict.items():
            #     stored_embedding = np.asarray(stored_embedding, dtype=np.float32)

            #     self_similarity = np.dot(
            #         stored_embedding,
            #         stored_embedding
            #     )

            #     st.write("Self similarity for", sid, ":", self_similarity)
            # ================================================================

            if not candidates_dict:   #agar voice k through register nahi kiya hai
                st.error("No enrolled students have voice profiles registered")
                return
            if audio_data is not None:
                audio_bytes= audio_data.read()

                detected_scores= process_bulk_audio(audio_bytes,candidates_dict)
# # ==================================================
#                 st.write("Detected scores:", detected_scores)
#                 st.write("Candidates:", candidates_dict.keys())
            #    ============================================================= # 
                results,attendance_to_log=[],[]

                current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")   #currtmstmp me datetime.now se us inst ka time note kar lenge


                for node in enrolled_students:
                    student = node['students']
                    score=detected_scores.get(student['student_id'],0.0)    #agar score nahi hai to 0.0 
                    is_present=bool(score>0)  # agar 0 se zyada baar present hai to is vaar me store karao

                    results.append({
                        "Name":student['name'],
                        "ID": student['student_id'],
                        "Score": score if is_present else "-",   #"score if is_present else "-"" nahiii                 #score batado agar present hai to warna '-' dikhayega
                        "Status":"✅ Present" if is_present else "❌ Absent"
                    })

                    attendance_to_log.append({
                        'student_id':student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp':current_timestamp,
                        'is_present': bool(is_present)
                        
                    })
                #saving this data in a state
                st.session_state.voice_attendance_results=(pd.DataFrame(results),attendance_to_log)
    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results, logs=st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)