# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 00:52:22 2021

@author: Pipe San Martín
"""

import os
import base64
import streamlit as st
from ibm_watson import TextToSpeechV1
from PIL import Image
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



def get_binary_file_downloader_html(bin_file, file_label='tu_audio_generado'):
    
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descarga {file_label}</a>'
    
    return href

def crea_audio(texto,voz,archivo='tu_audio_generado.wav'):
    
    with open(archivo, 'wb') as archivo_audio:
        
        archivo_audio.write(
                text_to_speech.synthesize(
                    texto,
                    voice=voz,
                    accept='audio/wav'        
                ).get_result().content)
        
    
    return archivo

favicon = Image.open("favicon.ico")
st.set_page_config(page_title='TTS Tester', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')
st.header("TTS IBM testing")


apikey = st.text_input('Ingresa tu apikey', value="", type="password")
url = st.text_input('y tu url', value="", type="password")


voces = ('es-US_SofiaV3Voice', 'es-LA_SofiaV3Voice', 'es-ES_EnriqueV3Voice', 'es-ES_LauraV3Voice')

voice = st.sidebar.selectbox(
    "Qué voz en español deseas usar?",
    voces
)

text = st.text_area("Texto a convertir en voz (soporta SSML)")

if st.button('Generar audio'):
    
    if not apikey or not url:
    
        st.warning("Por favor ingresa tu apikey o url para autentificarme y poder usar el modelo tts")
        st.stop()
    
    
    with st.spinner('Haciendo autentificación..'):
        
        try:
            
            authenticator = IAMAuthenticator(apikey)
            text_to_speech = TextToSpeechV1(authenticator=authenticator)
            text_to_speech.set_service_url(url)
        
        except Exception as e: 
            
            st.error("No se logró la autentificación")
            st.warning(f"Revisa que la apikey: {apikey} y url: {url}, sean correctas")
            st.info("Abajo los detalles")
            st.exception(e)
            st.stop()
    
    with st.spinner("Generando audio"):
            
        try:
            audio = crea_audio(text, voice)
            
        except Exception as e:
                
            st.error("No se logró generar el audio")
            st.info("Abajo los detalles")
            st.exception(e)
            st.stop()
    
    st.success('¡Audio generado!')
    st.balloons()
    
    audio_file = open(audio, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    
    st.markdown(get_binary_file_downloader_html(audio),unsafe_allow_html=True)
    
