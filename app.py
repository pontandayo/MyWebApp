from flask import Flask, render_template, request, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# NotoSansJP フォントの登録
FONT_PATH = 'fonts/NotoSansJP-Regular.ttf'
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"フォントファイルが見つかりません: {FONT_PATH}")
pdfmetrics.registerFont(TTFont('NotoSansJP', FONT_PATH))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "URLが指定されていません"}), 400

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # サイトの簡易診断
        title = soup.title.string if soup.title else "タイトルなし"
        word_count = len(soup.get_text().split())
        link_count = len(soup.find_all('a'))

        # レポートデータ作成
        report = {
            "URL": url,
            "タイトル": title,
            "単語数": word_count,
            "リンク数": link_count
        }

        # レポートPDF生成
        pdf_buffer = BytesIO()
        generate_pdf(report, pdf_buffer)
        pdf_buffer.seek(0)

        # PDFファイルを返す
        return send_file(pdf_buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_pdf(report, buffer):
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("NotoSansJP", 12)

    text = c.beginText(50, 800)
    text.setFont("NotoSansJP", 12)
    text.textLine("ウェブサイト診断レポート")
    text.textLine("")
    text.textLine(f"URL: {report['URL']}")
    text.textLine(f"タイトル: {report['タイトル']}")
    text.textLine(f"単語数: {report['単語数']}")
    text.textLine(f"リンク数: {report['リンク数']}")
    c.drawText(text)

    c.showPage()
    c.save()

if __name__ == '__main__':
    # 開発環境では debug=True
    app.run(debug=False)
