import speech_recognition as sr

reconhecedor = sr.Recognizer()
with sr.Microphone() as fonte:
    print("Fala aí:")
    audio = reconhecedor.listen(fonte)

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print("Você disse:", texto)
    except sr.UnknownValueError:
        print("Não entendi...")
