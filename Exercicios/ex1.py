import speech_recognition as sr

reconnaisseur = sr.Recognizer()
with sr.Microphone() as fonte:
    print("Dit quelque chose :")
    audio = reconnaisseur.listen(fonte)

    try:
        texto = reconnaisseur.recognize_google(audio, language="fr-FR")
        print('Vous Avez dit :', texto)
    except sr.UnknownValueError:
        print("Não entendi...")
