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
        return jsonify(bot_msg)
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': str(e)})

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