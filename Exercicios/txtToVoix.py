import pyttsx3

# Initialisation de pyttsx3
engine = pyttsx3.init()

# Récupération des voix disponibles
voices = engine.getProperty('voices')

# Recherche de la voix en français
for voice in voices:
    # Vérifier si 'languages' n'est pas vide et si la langue contient 'fr'
    if voice.languages and 'fr' in voice.languages[0]:
        engine.setProperty('voice', voice.id)
        break

# Texte que vous souhaitez convertir en voix
texte = "Bonjour, comment ça va ?"

engine.setProperty('rate', 260)  # Velocidade da fala
engine.setProperty('volume', 1)  # Volume (0.0 a 1.0)

# Conversion du texte en parole
engine.say(texte)

# Exécution de la parole
engine.runAndWait()