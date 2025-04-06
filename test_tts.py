from flask import Flask, request, jsonify
import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.utils import which
import simpleaudio as sa
import io
import wave  # ✅ nécessaire pour lire le wav_io

# Forcer pydub à utiliser ffmpeg
AudioSegment.converter = which("ffmpeg")

# 💡 Créer l'app Flask AVANT d'utiliser @app.route
app = Flask(__name__)

async def synthese_audio(texte, voix="fr-FR-DeniseNeural"):
    communicate = edge_tts.Communicate(text=texte, voice=voix)
    audio_bytes = b""

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    # Convertir MP3 → WAV en mémoire
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io

@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.json
        texte = data.get("texte", "")
        voix = data.get("voix", "fr-FR-DeniseNeural")

        if not texte:
            return jsonify({"error": "Aucun texte fourni"}), 400

        # Lancer la synthèse
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        wav_io = loop.run_until_complete(synthese_audio(texte, voix))

        # ✅ Lecture directe depuis flux mémoire
        wav_io.seek(0)
        wave_read = wave.open(wav_io, 'rb')
        wave_obj = sa.WaveObject.from_wave_read(wave_read)
        wave_obj.play().wait_done()

        return jsonify({"status": "voix jouée"}), 200

    except Exception as e:
        print(f"[ERREUR SERVEUR] {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005)
