from flask import Flask, request, render_template, send_file
import matplotlib.pyplot as plt
import japanize_matplotlib  # 日本語フォント設定
import numpy as np
from reportlab.pdfgen import canvas
from io import BytesIO
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-plot', methods=['POST'])
def generate_plot():
    # サンプルのプロット生成
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, label='サイン波')
    plt.title('サンプルプロット')
    plt.xlabel('X軸')
    plt.ylabel('Y軸')
    plt.legend()

    # プロットを画像として返す
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='plot.png')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # PDFの生成
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "サンプルPDF")
    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='sample.pdf')

@app.route('/scrape', methods=['POST'])
def scrape():
    # URLからデータをスクレイピング
    url = request.form.get('url')
    if not url:
        return "URLが入力されていません", 400

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "タイトルが見つかりません"
        return f"ページタイトル: {title}"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
