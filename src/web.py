import os
import uuid
from flask import Flask, render_template_string, request, send_file, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import threading

from .converter import Converter
from .batch_processor import BatchProcessor
from .config import logger

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'web_output'

Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

TASKS = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电子书转MP3</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .container { background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 40px; width: 100%; max-width: 500px; }
        h1 { color: #333; margin-bottom: 30px; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
        input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
        input:focus, select:focus { outline: none; border-color: #4a90d9; }
        .file-drop { border: 2px dashed #ddd; border-radius: 8px; padding: 30px; text-align: center; cursor: pointer; transition: all 0.3s; }
        .file-drop:hover { border-color: #4a90d9; background: #f8f9fa; }
        .file-drop.dragover { border-color: #4a90d9; background: #e8f4fd; }
        .btn { width: 100%; padding: 14px; background: #4a90d9; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background: #357abd; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .progress { margin-top: 20px; display: none; }
        .progress-bar { height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden; }
        .progress-fill { height: 100%; background: #4a90d9; width: 0%; transition: width 0.3s; }
        .status { margin-top: 10px; color: #666; font-size: 14px; text-align: center; }
        .result { margin-top: 20px; display: none; }
        .result a { display: block; padding: 15px; background: #d4edda; color: #155724; text-align: center; border-radius: 6px; text-decoration: none; }
        .result a:hover { background: #c3e6cb; }
        .error { margin-top: 20px; padding: 15px; background: #f8d7da; color: #721c24; border-radius: 6px; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📖 电子书转MP3</h1>
        <form id="convertForm" enctype="multipart/form-data">
            <div class="form-group">
                <label>上传文件 (EPUB, MOBI, TXT)</label>
                <div class="file-drop" id="fileDrop">
                    <span id="fileName">点击选择文件或拖拽到此处</span>
                    <input type="file" id="fileInput" name="file" accept=".epub,.mobi,.txt" style="display:none">
                </div>
            </div>
            <div class="form-group">
                <label>语音</label>
                <select name="voice">
                    <option value="zh-CN-XiaoxiaoNeural">晓晓 (女声)</option>
                    <option value="zh-CN-YunxiNeural">云希 (男声)</option>
                    <option value="zh-CN-YunyangNeural">云扬 (男声)</option>
                    <option value="zh-CN-XiaoyiNeural">小艺 (女声)</option>
                </select>
            </div>
            <div class="form-group">
                <label>音频比特率</label>
                <select name="bitrate">
                    <option value="128k">128 kbps</option>
                    <option value="192k" selected>192 kbps</option>
                    <option value="256k">256 kbps</option>
                    <option value="320k">320 kbps</option>
                </select>
            </div>
            <div class="form-group">
                <label>分段长度</label>
                <input type="number" name="segment_length" value="500" min="100" max="2000">
            </div>
            <button type="submit" class="btn" id="submitBtn">开始转换</button>
        </form>
        <div class="progress" id="progress">
            <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
            <div class="status" id="status">处理中...</div>
        </div>
        <div class="error" id="error"></div>
        <div class="result" id="result">
            <a id="downloadLink" href="#">下载 MP3</a>
        </div>
    </div>
    <script>
        const fileDrop = document.getElementById('fileDrop');
        const fileInput = document.getElementById('fileInput');
        const fileName = document.getElementById('fileName');
        const form = document.getElementById('convertForm');
        const submitBtn = document.getElementById('submitBtn');
        const progress = document.getElementById('progress');
        const progressFill = document.getElementById('progressFill');
        const status = document.getElementById('status');
        const result = document.getElementById('result');
        const downloadLink = document.getElementById('downloadLink');
        const error = document.getElementById('error');

        fileDrop.onclick = () => fileInput.click();
        fileDrop.ondragover = (e) => { e.preventDefault(); fileDrop.classList.add('dragover'); };
        fileDrop.ondragleave = () => fileDrop.classList.remove('dragover');
        fileDrop.ondrop = (e) => {
            e.preventDefault();
            fileDrop.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                fileName.textContent = e.dataTransfer.files[0].name;
            }
        };
        fileInput.onchange = () => {
            if (fileInput.files.length) fileName.textContent = fileInput.files[0].name;
        };

        form.onsubmit = async (e) => {
            e.preventDefault();
            if (!fileInput.files.length) {
                alert('请选择文件');
                return;
            }
            submitBtn.disabled = true;
            progress.style.display = 'block';
            result.style.display = 'none';
            error.style.display = 'none';
            progressFill.style.width = '0%';
            status.textContent = '上传中...';

            const formData = new FormData(form);
            try {
                const res = await fetch('/api/convert', { method: 'POST', body: formData });
                const data = await res.json();
                if (data.error) {
                    error.textContent = data.error;
                    error.style.display = 'block';
                } else {
                    downloadLink.href = '/api/download/' + data.task_id;
                    result.style.display = 'block';
                }
            } catch (err) {
                error.textContent = '转换失败: ' + err.message;
                error.style.display = 'block';
            }
            submitBtn.disabled = false;
        };
    </script>
</body>
</html>
'''

def run_server(host='0.0.0.0', port=5000):
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)

    @app.route('/api/convert', methods=['POST'])
    def convert():
        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400
        
        file = request.files['file']
        if not file.filename:
            return jsonify({'error': '没有选择文件'}), 400
        
        ext = Path(file.filename).suffix.lower()
        if ext not in ['.epub', '.mobi', '.txt']:
            return jsonify({'error': '不支持的文件格式'}), 400

        task_id = str(uuid.uuid4())
        upload_dir = Path(app.config['UPLOAD_FOLDER']) / task_id
        output_dir = Path(app.config['OUTPUT_FOLDER']) / task_id
        upload_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        input_path = upload_dir / secure_filename(file.filename)
        file.save(str(input_path))

        voice = request.form.get('voice', 'zh-CN-XiaoxiaoNeural')
        bitrate = request.form.get('bitrate', '192k')
        segment_length = int(request.form.get('segment_length', 500))

        def convert_task():
            try:
                converter = Converter(voice=voice, bitrate=bitrate, segment_length=segment_length)
                output_path = converter.convert(str(input_path), str(output_dir))
                TASKS[task_id] = {'status': 'completed', 'output': output_path}
            except Exception as e:
                logger.error(f"Conversion failed: {e}")
                TASKS[task_id] = {'status': 'error', 'error': str(e)}

        thread = threading.Thread(target=convert_task)
        thread.start()
        
        return jsonify({'task_id': task_id})

    @app.route('/api/status/<task_id>')
    def status(task_id):
        task = TASKS.get(task_id)
        if not task:
            return jsonify({'error': '任务不存在'}), 404
        return jsonify(task)

    @app.route('/api/download/<task_id>')
    def download(task_id):
        task = TASKS.get(task_id)
        if not task or task['status'] != 'completed':
            return '文件不存在', 404
        return send_file(task['output'], as_attachment=True, download_name='output.mp3')

    app.run(host=host, port=port, debug=False)
