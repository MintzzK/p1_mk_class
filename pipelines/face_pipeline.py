import streamlit as st
import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC

from src.database.db import get_all_st

@st.cache_resource 
def load_dlib_models():    #we  use these modules with dlib to increase its effeciency
    detector =dlib.get_frontal_face_detector()    #dlib will provide a detector that detects the overall face

    sp= dlib.shape_predictor(                      #landmark detection
        face_recognition_models.pose_predictor_model_location()       #pose_predictor_model_location is a module used to detect all the landmark location
    )

    facerec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
     )
    return detector, sp ,facerec

# is se hum face ko numbers me convert kaar rahe hai aur wo no.s binary me convert ho jayenge
def get_face_embeddings(image_np):    #pass an img as a parameter
    detector, sp, facerec= load_dlib_models()  #load the dlib models
    faces= detector(image_np,1)  #image kko ek hi baar process karo , jitni zyada times karenge utna better

    encodings= []   # is array me ek ek karke embeddings bharte jayenge

    for face in faces:    #basically face is 'i' in for loop 
        shape=sp(image_np,face)
        face_descriptor= facerec.compute_face_descriptor(image_np,shape,1)

        encodings.append(np.array(face_descriptor))    #numpy array me calculate karne se mathematical calns easy ho jati hai as compared  to python list 
    return encodings


@st.cache_resource #  baar baar heavy functions ko rerun nahi karte unless kabhi data update karna ho 
def get_trained_model():  #data base me existing students ke data ko provided image se compare karega aur check karega ki ye wo student hai ki nahi
    X=[] #eg 15 embedding  ye dono khali list hai isme ek ek karke data daalenge embedding ka
    Y=[] # eg 15 ids          aue st id ka


    student_db= get_all_st() #student data from database

    if not student_db:     #agar koi data nahi nahi hai student ka to none return karo
        return None
    
    for student in student_db:
        embedding=student.get("face_embedding")   # student is basicalli 'i' in for loop and hum ek ek st k face embedding data ko chk kr rahe hai 
        if embedding:
            X.append(np.array(embedding))           #ek eke karke st embedding aur st id ka data bhar rahe hai
            Y.append(student.get("student_id"))

    if len(X)==0:   #agar kuchh bhi data nahi bharaya  to return none
        return 0
    
    #classification through "support vector clasifier" -ML algo used for clsfn tasks that finds an optimal hyperplane to separate data points into different classes
    clf= SVC(kernel='linear',probability=True,class_weight="balanced")
#  linear is the easiest method to classify,  prob true provides kitna %match kar raha hai photo  , balance se saare photos(provided us insaan ke) ko ek scale pe le aata hai

    #try block me error daalte hai
    try:
        clf.fit(X,Y)
    except ValueError:
        pass
    return{"clf":clf,"X":X,"Y":Y}
    


def train_classifier():
        st.cache_resource.clear()    #jab kabhi data update karna ho like naye st ki entry to purane unrefreshed data ko clr krnge kyunki usmen to ye info haii hi nahi
        model_data=get_trained_model()
        return bool(model_data)
    

def predict_attendance(class_image_np):    #group pic of class using np array
        encodings=get_face_embeddings(class_image_np)   #saare students ki face embeddings ko detect karega 

        detected_student={} #empty dictionary  
        model_data=get_trained_model()
        if not model_data:
            return detected_student ,[], len(encodings)
        
        clf =model_data['clf']
        X_train= model_data['X']
        Y_train= model_data['Y']
 

        all_st= sorted(list(set(Y_train)))


        for encoding in encodings:
            if len(all_st)>=2:
                predicted_id=int(clf.predict([encoding])[0])
            else:
                predicted_id=int(all_st[0])
            
            student_embedding =X_train[Y_train.index(predicted_id)]

            best_match_score= np.linalg.norm(student_embedding - encoding)

            resemblence_threshold=0.6 #dono faces me 0.6 se zyada dist hui to dono faces same hone k chamces kam hai

            if best_match_score<= resemblence_threshold:
                detected_student[predicted_id]=True
        

        return detected_student, all_st, len(encodings)