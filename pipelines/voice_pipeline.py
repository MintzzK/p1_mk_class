from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io    #helps audio file to import in librosa
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder=load_voice_encoder()

        # UploadedFile → bytes
        # audio_bytes = audio_file.read()

        # bytes → audio waveform
        audio,sr =librosa.load(io.BytesIO(audio_bytes),sr=16000)

        # Resemblyzer preprocessing
        wav=preprocess_wav(audio)

        # Generate 256-dimensional voice embedding
        embedding =encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as  e:
        st.error("Voice recognition error")
        st.error(e)     #voice enrollment k time ye error aa raha hai==== a bytes-like object is required, not 'UploadedFile'
        return None
    

def identify_speaker(new_embedding,candidates_dict,threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None ,0.0

    # st.write("NEW embedding:")
    # st.write(type(new_embedding))
    # st.write(new_embedding.shape)
    # new_embedding = np.asarray(
    # new_embedding,
    # dtype=np.float32
    # )
    
    best_sid=None
    best_score= -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity =np.dot(new_embedding, stored_embedding)
            if similarity> best_score:
                best_score= similarity
                best_sid =sid
    
    if best_score>= threshold:
        return best_sid, best_score
    
    return None, best_score


# def identify_speaker(new_embedding, candidates_dict, threshold=0.55):

#     if new_embedding is None or not candidates_dict:
#         return None, 0.0

#     # new_embedding = np.asarray(
#     #     new_embedding,
#     #     dtype=np.float32
#     # )

#     # new_embedding = new_embedding / np.linalg.norm(new_embedding)

#     # best_sid = None
#     # best_score = -1.0

#     for sid, stored_embedding in candidates_dict.items():

#         if stored_embedding is None:
#             continue

#         # stored_embedding = np.asarray(
#         #     stored_embedding,
#         #     dtype=np.float32
#         # )

#         if new_embedding.shape != stored_embedding.shape:
#             continue

#         stored_embedding = stored_embedding / np.linalg.norm(
#             stored_embedding
#         )

#         similarity = np.dot(
#             new_embedding,
#             stored_embedding
#         )
#         st.write(similarity)
#         if similarity > best_score:
#             best_score = similarity
#             best_sid = sid

#     if best_score >= threshold:
#         return best_sid, best_score

#     return None, best_score



def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.55):
    try:
        encoder= load_voice_encoder()

        audio,sr= librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments = librosa.effects.split(audio, top_db=30)
        # st.write("Segments:", segments)
        identified_results={}

        for  start , end in segments:
            if (end-start)<sr * 0.5:
                continue
            segment_audio= audio[start:end]
            wav= preprocess_wav(segment_audio)
            embedding=encoder.embed_utterance(wav)

            sid,score= identify_speaker(embedding,candidates_dict,threshold)
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid]=score
        
        return identified_results
    except Exception as e:
        st.error("Bulk process error")
        st.error(e)
        # return {}