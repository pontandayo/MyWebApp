import os
import requests
from flask import Flask, request, render_template, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bs4 import BeautifulSoup

app = Flask(__name__)

# フォントの登録 (NotoSansJP)
pdfmetrics.registerFont(TTFont('NotoSansJP', 'NotoSansJP-Regular.ttf'))

@app.route('/')
def index():
    """トップページを表示"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_website():
    """URLの解析処理"""
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URLが指定されていません。'}), 400

    try:
        # ウェブサイトのHTMLを取得
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # BeautifulSoupを使用して解析
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else "タイトルが見つかりません"

        # パフォーマンス診断の簡易データ（例として文字数を使用）
        word_count = len(html_content.split())
        return jsonify({
            'url': url,
            'title': title,
            'word_count': word_count,
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"ウェブサイトの取得中にエラーが発生しました: {e}"}), 500

@app.route('/generate', methods=['POST'])
def generate_report():
    """解析結果をPDFとして出力"""
    url = request.form.get('url')
    title = request.form.get('title')
    word_count = request.form.get('word_count')

    # PDF生成
    pdf_path = "static/report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont('NotoSansJP', 12)

    c.drawString(100, 750, f"URL: {url}")
    c.drawString(100, 730, f"タイトル: {title}")
    c.drawString(100, 710, f"総文字数: {word_count}")
    c.drawString(100, 690, "これはサンプルのパフォーマンスレポートです。")
    c.save()

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Heroku環境変数PORTを使用
    app.run(host='0.0.0.0', port=port)
