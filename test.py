from flask import Flask, render_template, request
import os
import re

app = Flask(__name__)

# Путь к папке с логами
LOG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

@app.route('/')
def index():
    # Получаем список всех .log файлов
    log_files = [f for f in os.listdir(LOG_FOLDER) if f.endswith('.log')]

    # Получаем параметры из запроса
    selected_file = request.args.get('file', log_files[0] if log_files else '')
    level = request.args.get('level', 'ALL')

    logs = []
    if selected_file:
        log_path = os.path.join(LOG_FOLDER, selected_file)
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if level != 'ALL':
                    pattern = re.compile(rf'\b{level}\b', re.IGNORECASE)
                    logs = [line for line in lines if pattern.search(line)]
                else:
                    logs = lines

    return render_template('index.html', logs=logs, log_files=log_files, selected_file=selected_file, level=level)

if __name__ == '__main__':
    app.run(debug=True)
