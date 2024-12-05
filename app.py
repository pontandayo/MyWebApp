from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4
import tempfile
import os

app = Flask(__name__)

# 日本語フォントの登録
pdfmetrics.registerFont(TTFont('IPA', 'ipaexg.ttf'))  # IPAexゴシックを使用（フォントファイルが必要）

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url:
        return "URLが入力されていません。", 400

    try:
        # URLへのリクエスト
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        status_code = response.status_code
        content_length = len(response.content)

        # HTML解析
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "タイトルが見つかりません"
        headings = {f"h{i}": len(soup.find_all(f"h{i}")) for i in range(1, 7)}

        # レポート内容
        report_data = {
            "URL": url,
            "ステータスコード": status_code,
            "応答時間（秒）": response_time,
            "コンテンツサイズ（バイト）": content_length,
            "タイトル": title,
            "見出しの数": headings,
        }

        # PDFレポート生成
        pdf_path = generate_pdf_report(report_data)
        return send_file(pdf_path, as_attachment=True, download_name="レポート.pdf")

    except Exception as e:
        return f"URLの解析中にエラーが発生しました: {str(e)}", 500

def generate_pdf_report(data):
    # 一時ファイルにPDFを生成
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)

    # 日本語フォントをセット
    c.setFont("IPA", 12)

    # レポート内容をPDFに記載
    c.drawString(100, 800, "ウェブサイト パフォーマンス レポート")
    c.drawString(100, 780, f"URL: {data['URL']}")
    c.drawString(100, 760, f"ステータスコード: {data['ステータスコード']}")
    c.drawString(100, 740, f"応答時間: {data['応答時間（秒）']} 秒")
    c.drawString(100, 720, f"コンテンツサイズ: {data['コンテンツサイズ（バイト）']} バイト")
    c.drawString(100, 700, f"タイトル: {data['タイトル']}")

    y_position = 680
    c.drawString(100, y_position, "見出しの数:")
    y_position -= 20
    for heading, count in data['見出しの数'].items():
        c.drawString(120, y_position, f"{heading}: {count}")
        y_position -= 20

    c.save()
    return temp_file.name

if __name__ == '__main__':
    # Heroku用のポート設定
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
