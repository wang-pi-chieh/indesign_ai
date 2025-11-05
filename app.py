from flask import Flask, request, render_template, jsonify, send_from_directory
import subprocess
import os

import sys

print("🔥 Flask 正在使用的 Python 解譯器：", sys.executable)
print("🐍 Python 版本：", sys.version)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Flask 會自動去 templates/index.html 找檔案
    return render_template('index.html')

# -------------------------------
# 📤 接收 PDF 檔案上傳
# -------------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '沒有檔案'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未選擇檔案'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    print(f"✅ 已上傳檔案：{file.filename} -> {save_path}")
    return jsonify({
        'message': f'上傳成功：{file.filename}',
        'filename': file.filename  # 👈 加上這行
    })


# -------------------------------
# ⚙️ 接收轉換規則並執行 test_reducto.py
# -------------------------------
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    rules = data.get('rules', '')
    filename = data.get('filename', '')

    if not filename:
        return jsonify({'error': '沒有提供檔名'}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(pdf_path):
        return jsonify({'error': f'找不到檔案：{pdf_path}'}), 404

    try:
        # 可選：把 rules 寫入 txt 檔案
        with open('rules.txt', 'w', encoding='utf-8') as f:
            f.write(rules)

        # 🚀 執行 test_reducto.py
        reducto_result = subprocess.run(
            ['python', 'test_reducto.py', pdf_path],
            capture_output=True, text=True
        )

        print("test_reducto.py 輸出：", reducto_result.stdout)
        print("test_reducto.py 錯誤：", reducto_result.stderr)

        # ✅ 根據原始檔名推算 JSON 檔案位置
        json_name = os.path.splitext(filename)[0] + '.json'
        src_json_path = os.path.join('uploads', json_name)
        dst_json_path = os.path.join('downloads', json_name)

        # 確保 downloads 資料夾存在
        os.makedirs('downloads', exist_ok=True)

        # ✅ 如果輸出在 uploads/，自動搬到 downloads/
        if os.path.exists(src_json_path):
            os.replace(src_json_path, dst_json_path)
            print(f"📦 已搬移 JSON：{src_json_path} → {dst_json_path}")
        elif not os.path.exists(dst_json_path):
            print("⚠️ 找不到任何輸出 JSON 檔案")
            return jsonify({'error': f'找不到輸出檔案：{json_name}'}), 404

        # ✅ 回傳給前端正確檔名
        return jsonify({
            'message': '✅ test_reducto.py 執行完成！',
            'json_filename': json_name  # ⚠️ 與前端一致
        })

    except Exception as e:
        print("❌ 錯誤：", e)
        return jsonify({'error': f'程式執行錯誤：{e}'})


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
