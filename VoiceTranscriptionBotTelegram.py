import speech_recognition as sr
from telegram.ext import Updater, MessageHandler, Filters

# Función para transcribir el audio
def transcribe_audio(audio):
    r = sr.Recognizer()

    try:
        text = r.recognize_google(audio, language='es')  # Utiliza el servicio de reconocimiento de Google
        return text
    except sr.UnknownValueError:
        return "No se pudo reconocer el audio"
    except sr.RequestError:
        return "Error en la solicitud al servicio de reconocimiento de voz"

# Función para manejar los mensajes de voz
def handle_voice_message(update, context):
    file_id = update.message.voice.file_id
    new_file = context.bot.get_file(file_id)
    audio_file = new_file.download_as_bytearray()

    audio = sr.AudioData(audio_file, sample_rate=16000, sample_width=2)
    transcription = transcribe_audio(audio)

    update.message.reply_text(transcription)

# Token de acceso al bot de Telegram
TOKEN = 'TU_TOKEN_DE_TELEGRAM'

# Crea el objeto Updater y el Dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Manejador de mensajes de voz
voice_handler = MessageHandler(Filters.voice, handle_voice_message)

# Agrega el manejador al dispatcher
dispatcher.add_handler(voice_handler)

# Inicia el bot
updater.start_polling()
