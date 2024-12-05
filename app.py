ffrom flask import Flask, request, render_template, send_file
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.pdfgen import canvas
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# プロット生成
@app.route('/generate-plot', methods=['POST'])
def generate_plot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure()
    plt.plot(x, y)
    plt.title('サイン波プロット')
    plt.xlabel('X軸')
    plt.ylabel('Y軸')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png', as_attachment=True, download_name='plot.png')

# PDF生成
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "これはサンプルPDFです！")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='sample.pdf')

# ウェブページタイトル取得
@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "タイトルが見つかりません"
    except Exception as e:
        title = f"エラー: {e}"

    return f"取得したタイトル: {title}"

# カスタムグラフ生成
@app.route('/custom-plot', methods=['POST'])
def custom_plot():
    equation = request.form.get('equation', 'sin(x)')
    x = np.linspace(0, 10, 100)

    try:
        y = eval(equation)
    except Exception as e:
        return f"エラー: 数式が無効です ({e})"

    plt.figure()
    plt.plot(x, y)
    plt.title(f'カスタムプロット: {equation}')
    plt.xlabel('X軸')
    plt.ylabel('Y軸')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png', as_attachment=True, download_name='custom_plot.png')

# カスタムPDF生成
@app.route('/custom-pdf', methods=['POST'])
def custom_pdf():
    text = request.form.get('text', 'カスタムPDFのデフォルトテキストです')

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, text)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='custom.pdf')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
