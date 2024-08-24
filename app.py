from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)

# Путь для загрузки файлов
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Функция для генерации субтитров
def generate_subtitles(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["text"]

# Главная страница сервиса
@app.route('/')
def index():
    return "Subtitle Generation Service"

# Маршрут для генерации субтитров
@app.route('/generate_subtitles', methods=['POST'])
def generate_subtitles_route():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files['video']
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)

    subtitles = generate_subtitles(video_path)

    return jsonify({"subtitles": subtitles})

# Запуск сервиса
if __name__ == '__main__':
    app.run(debug=True)
