#pip install speechrecognition
#pip install gtts
#pip install openai
#pip install Flask
#pip install flask_cors
#pip install python-dotenv

import speech_recognition as sr
import os
from gtts import gTTS
from openai import OpenAI
from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS, cross_origin
import uuid
from dotenv import load_dotenv 
from transformers import pipeline
from pronouncing import phones_for_word
from panphon.distance import Distance
from phonemes_mapping import arpa_to_ipa, vocales_comp

#whisper = pipeline('automatic-speech-recognition', model = 'dg96/whisper-finetuning-phoneme-transcription-g2p-large-dataset-space-seperated-phonemes')

load_dotenv()

app = Flask(__name__)
#Agregamos las configuraciones CORS
CORS(app)
#Es necesario definir una secret key
app.secret_key = 'tu_clave_secreta'

API_KEY = os.environ.get('API_KEY')

client = OpenAI(api_key=API_KEY)

#seteos, por ahora solo tiene el nivel de inglés
settings = {'skills':'B2'}

#este array contiene las conversaciones. Tengo que modificarlo para que
#guarde conversaciones según usuario. Por ahora no quiero utilizar una
#base de datos.

conversation = []

#función que se comunica con la API de OpenAI
def send_completion(msg):
    #mensaje enviado por el usuario
    message = {"role": 'user', 'content': msg}
    try:
        #seteo y envío del completion
        completion = client.chat.completions.create(
        model ='gpt-3.5-turbo',
        messages = [
            {"role": 'system', 'content': "You're a english learning companion. You have to help the user to maintain a conversation to improve his communicative skills. His skill's level is {settings['skills']}"},
            message
            ],
        temperature = 1.0,
        max_tokens = 50,
        stream = True)
        
        #variable que guarda la respuesta
        response = ''

        #Utilizamos streams en vez de request dado que nos interesa que el bot mantenga
        #una conversación incremental y basada en respuestas acumuladas de la misma.

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response = response + chunk.choices[0].delta.content
                #este print no es necesario
                print(chunk.choices[0].delta.content, end="")
        #Agregamos la conversación entre el usuario y el bot al diccionario:
        conversation.append({'user': msg, 'bot': response})
        return response
    except Exception as e:
        print(f'Error: {e}')

#Función que transcribe el audio enviado por el cliente a texto    
def transcribe(wav_content):
    #módulo recognizer
    recognizer = sr.Recognizer()
    #utilizamos el contexto del recognizer para obtener el audio
    with sr.AudioFile(wav_content) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)
        try:
            #utilizamos el transcriptor de google
            transcription = recognizer.recognize_google(audio, language='en-US')
            return transcription
        except sr.UnknownValueError as une:
            print("no se entiende")
            raise une
        except sr.RequestError as e:
            print(f"Error desconocido: {e}")
            raise e

#método para obtener el audio de esa respuesta
@app.route('/get_audio', methods=['GET'])
#permitir el órigen cruzado del CORS
@cross_origin()
#función que genera el audio a partir del texto
def get_audio():
    try:
        #obtenemos la query param que tiene el mensaje 
        msg = request.args.get('msg')
    except ValueError:
        return jsonify({'success': False, 'error': 'Texto no proporcionado'})
    try: 
        #Enviamos a gtts el mensaje, que nos devuelve el audio
        tts = gTTS(msg, lang='en-us')
        #salvamos el audio temporalmente en el servidor
        #lo ideal sería acá generar un archivo para cada sesión, para cada mensaje
        #del bot
        tts.save('audio.mp3')
        #lo enviamos al cliente
        return send_file('audio.mp3', mimetype="audio/mp3", as_attachment=True)

    except Exception as e:
        print(f'Error generado:{e}')

#endpoint para obtener la respuesta en texto del bot
@app.route('/get_response', methods=['POST'])
def get_response():
    #obtenemos el archivo de audio
    if request.files['audio']:
        audio = request.files['audio']
    else:
        return jsonify({'success': False, 'error': 'audio no presente'})
    try:
    #si el usuario no tiene sesión, la creamos
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        #transcribimos el audio
        user_msg = transcribe(audio)
        #se lo mandamos a openAI
        bot_msg = send_completion(user_msg)
        #enviamos la respuesta
        print(bot_msg)
        return jsonify({'bot_msg': bot_msg, 'user_msg': user_msg})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': str(e)})

def get_phonemes(text):
    #phonemes = whisper('audio.wav')
    text='HH IH L OW  , HH AW  HH AE L  Y UW'
    phonemes = {'text': ''}
    phonemes['text'] = text
    result = ''.join(caracter for caracter in phonemes['text'] if caracter.isalpha() or caracter.isspace())
    result = result.split('  ')
    result = [word.strip() for word in result if word]
    result = [word.split() for word in result]
    return result

def convert_arpa_to_ipa(text):
    return arpa_to_ipa[text]

def convert_arpa(text):
    text = clean_text(text)
    text_good = [phones_for_word(word) for word in text.split()]
    text_good = [phonemes[0].split() for phonemes in text_good]
    #text_good = ' '.join(str(el) for word in text_good for el in word)
    return text_good

def clean_text(text):
    text = ''.join(caracter for caracter in text if caracter.isalpha() or caracter.isspace())
    return text
def calculate_score(right,user):
    final_answers = []
    rs = Distance()
    #print(user)
    for i,word, in enumerate(right):
        print(word)
        final_answers.append([])
        print(final_answers)
        for j,phoneme in enumerate(word):
            if(j<len(user[i])):
                final_answers[i].append([phoneme,user[i][j]])
            else:
                final_answers[i].append([phoneme,''])
    final_answers=[[
        [phoneme_pair[0][0],phoneme_pair[1], phoneme_pair[0][1],rs.feature_edit_distance(convert_arpa_to_ipa(phoneme_pair[0][0]),convert_arpa_to_ipa(phoneme_pair[1]))] 
        for phoneme_pair in word] for word in final_answers]
    
    print(final_answers)
#endpoint que asigna puntajes a la pronunciación
@app.route('/get_scores', methods=['GET'])
def get_scores(phon_vocals=vocales_comp):
    text = request.args.get('msg')
    pronounced = get_phonemes(text) #En realidad es del audio
    arpabet = convert_arpa(text)
    text = text.split()
    vocals = ['a','e','i','o','u']
    arpa_text = []
    i = 0
    for j, phonemes in enumerate(arpabet):
        arpa_text.append([])
        for k, phoneme in enumerate(arpabet[j]):
            arpa_text[j].append([phoneme,''])
            ultimo = False
            if ultimo:
                break
            while True:
                if ultimo:
                    break
                if k== len(arpabet[j])-1:
                    ultimo = True
                if phoneme in phon_vocals:
                    if text[j][i] in vocals:
                        #print(arpa_text)
                        arpa_text[j][k][1] = arpa_text[j][k][1]+text[j][i]
                        i=i+1                   
                        if ultimo:
                            arpa_text[j][k][1]  = arpa_text[j][k][1]+text[j][i:]
                            i=0
                            break
                        continue
                    elif text[j][i]=="w" and arpabet[k]!='W':
                        arpa_text[j][k][1]  = arpa_text[j][k][1]+text[j][i]
                        i=i+1
                        if ultimo:
                            arpa_text[j][k][1]  = arpa_text[j][k][1]+text[j][i:]
                            i=0
                            break
                        break
                    else:
                        break
                elif text[j][i] not in vocals:
                    arpa_text[j][k][1]  = arpa_text[j][k][1]+text[j][i]
                    i=i+1                       
                    if ultimo:
                        arpa_text[j][k][1]  = arpa_text[j][k][1]+text[j][i:]
                        i=0                       
                        break
                    continue
                else:
                    break
    compare = calculate_score(arpa_text,pronounced)
    #print(arpa_text)
    return arpa_text
#iniciamos el servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

'''
Queda por agregar:
-En la variable de conversaciones del servidor, dividir las conversaciones según
la sesión de cada usuario.

-El archivo de audio de momento es un archivo único que se pisa. Lo ideal sería
generar carpetas para cada usuario, donde cada audio de respuesta del bot exista
con un id único.

-Si el ejercicio prospera, podría ver de llevar las conversaciones a una base
de datos en mongo. No estoy muy seguro de qué hacer con el sistema de archivo de 
audios.
'''