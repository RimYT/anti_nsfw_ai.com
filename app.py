import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from anti_nsfw_handler import process_image  # Замените на вашу функцию нейросети

# Инициализация приложения Flask
app = Flask(__name__)

# Папка для загрузки изображений
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Убедитесь, что папка для загрузки изображений существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Главная страница с формой загрузки
@app.route('/')
def index():
    return render_template('index.html')

# Обработка загрузки изображения
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Обрабатываем изображение через нейросеть
        result = process_image(filepath)

        # Удаляем изображение после обработки
        os.remove(filepath)

        # Возвращаем результат обратно на страницу
        return render_template('index.html', result=result)

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=8080)
