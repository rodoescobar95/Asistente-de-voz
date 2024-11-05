import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# Opciones de voz/idioma
id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'
id3 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'
id4 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0'


# Escuchar microfono y devolver audio como texto
def transformar_audio_en_texto():
    # Almacenar recognizer en una variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(origen, duration=1)
        # informar que comenzo la grabacion
        print("ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-mx")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver a pedido
            return pedido
        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendio el audio
            print("Oops, no entendi")

            # Devolver error
            return "Sigo esperando"
        # En caso de no resolver el pedido
        except sr.RequestError:
            # Prueba de que no comprendio el audio
            print("Oops, no hay servicio")

            # Devolver error
            return "Sigo esperando"
        # Error inesperado
        except:
            # Prueba de que no comprendio el audio
            print("Oops, algo ha salido mal")

            # Devolver error
            return "Sigo esperando"


# Funcion para que el asistente sea escuchado
def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id4)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario que contiene los nombres de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # Decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar que hora es
def pedir_hora():

    # pedir variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 4 or hora.hour > 20:
        momento = '¡Buenas noches!'
    elif 4 <= hora.hour < 12:
        momento = '¡Buenos días!'
    else:
        momento = '¡Buenas tardes!'
    # decir el saludo
    hablar(f'{momento}, soy Luna, tu asistente personal. Por favor, dime en qué te puedo ayudar')


# Funcion central del asistente
def pedir_cosas():

    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    while comenzar:
        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()
        
        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Entendido, ya estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' or 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Disculpa, no la he encontrado')
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break

pedir_cosas()
