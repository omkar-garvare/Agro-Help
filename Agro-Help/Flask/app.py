from flask import Flask, render_template, request, send_file
from markupsafe import Markup
from model import predict_image
import utils
from gtts import gTTS
import os

app = Flask(__name__)

# Supported languages (Only English, Marathi, Hindi)
LANGUAGES = {
    "English": "en",
    "Marathi": "mr",
    "Hindi": "hi"
}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', languages=LANGUAGES)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            res = Markup(utils.disease_dic[prediction])

            return render_template('display.html', result=res, languages=LANGUAGES)
        except Exception as e:
            print(e)

    return render_template('index.html', status=500, res="Internal Server Error")


@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    try:
        text = request.form.get("text")
        lang = request.form.get("language", "en")

        if lang not in LANGUAGES.values():
            lang = "en"  # Default to English if an unsupported language is chosen

        # Generate speech using gTTS
        tts = gTTS(text=text, lang=lang)
        audio_path = "static/prediction.mp3"
        tts.save(audio_path)

        return send_file(audio_path, as_attachment=False)
    except Exception as e:
        print("Error generating audio:", e)
        return "Error generating audio", 500


if __name__ == "__main__":
    app.run(debug=True)
