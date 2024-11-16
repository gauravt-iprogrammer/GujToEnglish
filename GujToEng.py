import streamlit as st
import hindi_transcribe
from deep_translator import GoogleTranslator
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import mysql.connector
from uuid import uuid4
import os


# FE part

st.title("Audio Transcriptor")

if 'response' not in st.session_state:
    st.session_state.response = False

# Streamlit app title
# st.title("Conditional Audio Recorder with Submit Button")

# Input for duration
duration = st.slider("Select duration (seconds)", 1, 30, 5)
sample_rate = 44100

def on_submit_action(uploaded_file):
    # Simulate transcription
    st.write("Transcribing...")
    transcription = hindi_transcribe.get_transcribe(uploaded_file)

    # Display the transcription
    st.write("Transcription:")
    # print(transcription["text"])
    # st.write(transcription["text"])

    # final_prompt = PromptTemplate.from_template(prompt_template)
    # Create an LLMChain using the prompt template
    # print(final_prompt)
    # form_filling_chain = final_prompt | llm

    # filled_form = form_filling_chain.invoke(transcription["text"]).dict()
    st.write(transcription)
    # result = auto_form.get_filled_form(transcription["english"])
    # translated = GoogleTranslator(source='auto', target='gu').translate(result.content)
    connection = mysql.connector.connect(host='localhost',
                                            database='GujToEng',
                                            user='root',
                                            password='Password*123')
    cursor = connection.cursor()
    sql_insert_blob_query = """ INSERT INTO articles
                        (id,gujtrans,engtrans) VALUES (%s,%s,%s)"""
    articleid = uuid4()
    gujtrans = transcription["gujrati"]
    engtrans = transcription["english"]
    insert_tuple = (str(articleid)[:20],gujtrans,engtrans)
    cursor.execute(sql_insert_blob_query, insert_tuple)
    connection.commit()

    # st.write(result.content)
    # st.write(translated)

# Start Recording Button
base_dir = "/home/gauravt/sound_record/transfer/recorded_file/"
output_file_name = "recorded_audio.wav"
if st.button("Start Recording"):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    st.write("Recording completed.")

    # Save audio file and set response to True in session state
    write(os.path.join(base_dir,output_file_name), sample_rate, np.int16(audio_data * 32767))  # Convert float32 to int16
    st.write(f"Audio saved as {output_file_name}")
    
    # Update response in session state
    st.session_state.response = True

# transcription = ""

if st.session_state.response:
    if st.button("Submit"):
        # st.write("audio file transcripted")
        # Call the additional function
        on_submit_action(os.path.join(base_dir,output_file_name))


# Upload MP3 file
# uploaded_file = st.text_input(label="Write the path to mp3 file")


# print(uploaded_file)




