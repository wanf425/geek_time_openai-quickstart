import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_translator.utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator
from flask import Flask, render_template, request, jsonify, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ALLOWED_EXTENSIONS = {'pdf'}
TRANSLATE_LANGUAGES = {
    'English': 'en',
    '中文': 'zh-cn',
    '日本語': 'ja'
}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 定义首页路由，用于显示翻译页面
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# 定义首页路由
@app.route('/translate', methods=['POST'])
def translate():
    # Check if POST request has file part
    if 'file' not in request.files:
        flash('No file part')
        return render_template('index.html')

    file = request.files['file']

    # Check if file is uploaded
    if file.filename == '':
        flash('No selected file')
        return render_template('index.html')

    # Check if file type is allowed
    if file and allowed_file(file.filename):
        source_lang = request.form.get('source_lang')
        target_lang = request.form.get('target_lang')
        target_format = request.form.get('target_format')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # argument_parser = ArgumentParser()
        # args = argument_parser.parse_arguments()
        # config_loader = ConfigLoader()
        # config = config_loader.load_config()
        model = OpenAIModel(model='OpenAIModel', api_key=os.getenv("OPENAI_API_KEY"))
        pdf_file_path = file_path
        file_format = target_format
        # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
        translator = PDFTranslator(model)
        output_file_path = translator.translate_pdf(pdf_file_path, file_format)

        flash('Translation successful. File saved as ' + os.path.dirname(os.path.abspath(__file__)) + '/' + output_file_path)
        return render_template('index.html')

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(host='0.0.0.0', debug=True, port=5000)
