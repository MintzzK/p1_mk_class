#list of all the queries to call the database
#all the database relate operations are in this file
import streamlit as st
from src.database.config import supabase
import bcrypt #for hashing te register and login id

def hash_pass(pswd):
    return bcrypt.hashpw(pswd.encode(), bcrypt.gensalt()).decode() #<<<<<<<<decode k baad  "()" >>>>>>>>> #hash the password . created a password, generated a salt and decoded


def chk_pswd(pswd,hashed):
    return bcrypt.checkpw(pswd.encode(),hashed.encode())   #<<<<<<<<<<ckeckpw>>>>>>>typo ho gaya tha


def chk_tr_exst(username):
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data) >0


def create_tr(username, password, name):
    print("username:", username, type(username))
    print("password:", password, type(password))
    print("hashed:", hash_pass(password), type(hash_pass(password)))
    print("name:", name, type(name))

    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    print(data)

    response = supabase.table("teachers").insert(data).execute()
    return response.data



def create_st(new_name,face_embedding=None, voice_embedding=None):
    data= {"name": new_name,
            "face_embedding":face_embedding,
            "voice_embedding":voice_embedding}
    response= supabase.table("students").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response= supabase.table("teachers").select("*").eq("username",username).execute() # '*' se saare jitne bhi teachers ne entry kari hai wo sab ek saath 
                                                                            #check hoga detabase  me jab bhi koi website pe login karega, eq se hum already existing username se check karenge
    if response.data:
        teacher= response.data[0]   #ye respone array ke form me show hota hai to hum array ke 1st element ko check karenge kyuunki ek hi response aagta hai ki ye user exist karta hai  ya nahi
        if chk_pswd(password,teacher['password']):
            return teacher
    return None


def get_all_st():
    response=supabase.table("students").select("*").execute()
    return response.data


def create_subject(sub_code,name,section,teacher_id):
    data={"subject_code":sub_code,
          'name':name,
          "section":section,
          "teacher_id":teacher_id
          }
    response= supabase.table('subjects').insert(data).execute()
    return response.data

def get_tr_sub(teacher_id):
    response=supabase.table("subjects").select("*,subject_students(count),attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute() #--------subjects ke bajaye students table me daal diya tha 
    subjects=response.data

    for sub in subjects:
        sub['total_students'] =sub.get("subject_students",[{}])[0].get("count",0) if sub.get("subject_students") else 0
        attendance= sub.get('attendance_logs')
        unique_sessions=len(set(log['timestamp'] for log in attendance))
        sub['total_classes']=unique_sessions

         
        sub.pop("subject_students",None)
        sub.pop("attendance_logs",None)

    return subjects

def enroll_st_to_sub(student_id, subject_id):
    data={'student_id':student_id,
          'subject_id':subject_id}
    response=supabase.table('subject_students').insert(data).execute()
    return response.data

def unenroll_st_to_sub(student_id, subject_id):
         #<<<<<<< deete mein koi arg nahi daalte>>>>>>>
    response=supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response=supabase.table("subject_students").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response=supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

def create_attendance(logs):
    response= supabase.table("attendance_logs").insert(logs).execute()    #supabse me attlogs table me logs insert kar ke execute kar do 
    return response.data #aur us se data lelo

# def create_attendance(logs):
#     print("Type:", type(logs))
#     print("Logs:", logs)

#     response = supabase.table("attendance_logs").insert(logs).execute()
#     return response.data
# def create_attendance(logs):
#     st.write("Type:", type(logs))
#     st.write("Logs:", logs)
#     st.write("Length:", len(logs) if hasattr(logs, "__len__") else "No length")

def get_attendance_for_tr(teacher_id):
    response=supabase.table('attendance_logs').select("*,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data