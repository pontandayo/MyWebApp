from flask import Flask, request, render_template, send_from_directory
import requests
import html
import time
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import io
import base64
import japanize_matplotlib  # 日本語フォントを自動設定
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

# Flaskアプリケーションの初期化
app = Flask(__name__)

# 日本語フォントの設定
pdfmetrics.registerFont(TTFont('NotoSansJP', './NotoSansJP-Regular.ttf'))

# ホームページ（フォームを表示）
@app.route('/')
def home():
    return render_template('index.html')

# データの視覚化（グラフ作成）
def generate_chart(image_count, script_count, css_count):
    labels = ['画像', 'スクリプト', 'CSSファイル']
    values = [image_count, script_count, css_count]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'orange', 'green'])
    ax.set_title('リソース分析結果')
    ax.set_ylabel('数')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)
    return chart_url

# ページ速度ランク付け
def rank_page_speed(load_time):
    if load_time < 1:
        return "速い"
    elif load_time < 3:
        return "普通"
    else:
        return "遅い"

# PDFレポート生成
def generate_pdf_report(url, load_time, html_size, image_count, script_count, css_count):
    filename = "performance_report.pdf"
    c = canvas.Canvas(filename)

    # 日本語フォントを使用
    c.setFont('NotoSansJP', 12)
    c.drawString(100, 750, f"パフォーマンスレポート: {url}")
    c.drawString(100, 730, f"ページ読み込み時間: {load_time:.2f} 秒")
    c.drawString(100, 710, f"HTMLサイズ: {html_size} バイト")
    c.drawString(100, 690, f"画像数: {image_count}")
    c.drawString(100, 670, f"スクリプト数: {script_count}")
    c.drawString(100, 650, f"CSSファイル数: {css_count}")
    c.save()
    return filename

# URLを受け取って処理
@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        end_time = time.time()

        load_time = end_time - start_time
        html_size = len(response.content)

        soup = BeautifulSoup(response.text, 'html.parser')

        images = soup.find_all('img')
        scripts = soup.find_all('script')
        css_links = soup.find_all('link', rel='stylesheet')
        image_count = len(images)
        script_count = len(scripts)
        css_count = len(css_links)

        speed_rank = rank_page_speed(load_time)
        chart_url = generate_chart(image_count, script_count, css_count)

        improvement_suggestions = []
        if image_count > 20:
            improvement_suggestions.append("画像の数を減らすか、圧縮してください。")
        if script_count > 10:
            improvement_suggestions.append("JavaScriptファイルの数を減らすことを検討してください。")
        if css_count > 5:
            improvement_suggestions.append("CSSファイルを統合または最小化してください。")

        pdf_file = generate_pdf_report(url, load_time, html_size, image_count, script_count, css_count)

        html_sample = html.escape(response.text[:500])

        result = f"""
        <h2>{url}の分析結果</h2>
        <p><strong>ページ読み込み時間:</strong> {load_time:.2f} 秒</p>
        <p><strong>速度ランク:</strong> {speed_rank}</p>
        <p><strong>HTMLサイズ:</strong> {html_size} バイト</p>
        <p><strong>画像数:</strong> {image_count}</p>
        <p><strong>スクリプト数:</strong> {script_count}</p>
        <p><strong>CSSファイル数:</strong> {css_count}</p>
        <h3>HTML内容のサンプル:</h3>
        <pre>{html_sample}</pre>
        <h3>リソース分析グラフ:</h3>
        <img src="data:image/png;base64,{chart_url}" alt="リソース分析グラフ">
        """
        
        if improvement_suggestions:
            result += "<h3>改善提案:</h3><ul>"
            for suggestion in improvement_suggestions:
                result += f"<li>{suggestion}</li>"
            result += "</ul>"
        else:
            result += "<p>特に改善の必要はありません。</p>"

        result += f"<p>PDFレポートをダウンロード: <a href='/{pdf_file}' target='_blank'>ダウンロード</a></p>"
        return result

    except requests.exceptions.RequestException as e:
        return f"{url}からデータを取得できませんでした: {e}"

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory(".", filename)

if __name__ == '__main__':
    app.run(debug=True)
