import os
from flask import Flask, request, render_template, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import requests
from bs4 import BeautifulSoup
from io import BytesIO

app = Flask(__name__)

# 日本語フォントの登録 (Noto Sans JP を使用)
FONT_NAME = 'NotoSansJP'
FONT_PATH = 'NotoSansJP-Regular.ttf'

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"フォントファイルが見つかりません: {FONT_PATH}")

pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')

    if not url:
        return jsonify({"error": "URLが入力されていません"}), 400

    try:
        # URLのデータを取得
        response = requests.get(url)
        response.raise_for_status()

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'タイトルなし'
        word_count = len(soup.get_text().split())
        link_count = len(soup.find_all('a'))

        # 簡易診断結果
        result = {
            "URL": url,
            "タイトル": title,
            "単語数": word_count,
            "リンク数": link_count,
            "診断結果": "サイトは正常に解析されました。"
        }

        # PDF生成
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        c.setFont(FONT_NAME, 12)
        c.drawString(100, 800, f"URL: {url}")
        c.drawString(100, 780, f"タイトル: {title}")
        c.drawString(100, 760, f"単語数: {word_count}")
        c.drawString(100, 740, f"リンク数: {link_count}")
        c.drawString(100, 720, "診断結果: サイトは正常に解析されました。")
        c.save()

        pdf_buffer.seek(0)

        # PDFをレスポンスとして送信
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="diagnosis_report.pdf",
            mimetype="application/pdf"
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"URLの取得に失敗しました: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"予期しないエラーが発生しました: {str(e)}"}), 500

if __name__ == '__main__':
    # ローカルで実行する場合
    app.run(debug=True)
