import os
import requests
from flask import Flask, render_template, request, session, send_file
from dotenv import load_dotenv
from fpdf import FPDF
import logging
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm
import numpy as np

# ロギング設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# 環境変数のロード
load_dotenv()
API_KEY = os.getenv("PAGESPEED_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# Flaskアプリケーション設定
app = Flask(__name__)
app.secret_key = SECRET_KEY

# 日本語フォントのパス
FONT_PATH = './fonts/NotoSansJP-Regular.ttf'

# Matplotlibフォント設定
if os.path.exists(FONT_PATH):
    font_prop = fm.FontProperties(fname=FONT_PATH)
    rcParams['font.family'] = font_prop.get_name()
else:
    rcParams['font.family'] = 'DejaVu Sans'

rcParams['axes.unicode_minus'] = False

# PageSpeedデータを取得する関数
def fetch_pagespeed_data(url):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        server_response_time = data['lighthouseResult']['audits']['server-response-time']['numericValue'] / 1000
        image_size = data['lighthouseResult']['audits']['total-byte-weight']['details']['items'][0]['totalBytes'] / (1024 * 1024)

        return {
            "サーバーレスポンス時間": {
                "value": f"{server_response_time:.2f}",
                "unit": "秒",
                "ideal": "0.2 秒 以下",
                "problem": "サーバー応答時間が遅延しています。",
                "suggestion": "キャッシュやCDNを導入して応答速度を改善してください。",
            },
            "画像サイズ": {
                "value": f"{image_size:.2f}",
                "unit": "MB",
                "ideal": "1.0 MB 以下",
                "problem": "画像のデータ量が多くページ表示に影響します。",
                "suggestion": "画像を圧縮し、WebP形式を使用してください。",
            },
        }
    except requests.RequestException as e:
        logging.error(f"APIリクエストエラー: {e}")
        return None
    except KeyError as e:
        logging.error(f"APIレスポンス解析エラー: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    if not url.startswith(('http://', 'https://')):
        return render_template('error.html', message="URL形式が正しくありません。もう一度入力してください。")

    results = fetch_pagespeed_data(url)
    if not results:
        return render_template('error.html', message="PageSpeed Insights APIでデータを取得できませんでした。URLを確認してください。")

    session['results'] = results
    session['url'] = url

    # グラフ作成
    metrics = list(results.keys())
    values = [float(results[key]["value"]) for key in metrics]
    ideals = [float(results[key]["ideal"].split()[0]) for key in metrics]

    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    x = np.arange(len(metrics))  # 指標のインデックス

    plt.figure(figsize=(10, 6))  # グラフのサイズを指定

    # 複数棒グラフ
    bar_width = 0.35
    plt.bar(x - bar_width / 2, values, bar_width, label="診断結果", color='#FF5252')
    plt.bar(x + bar_width / 2, ideals, bar_width, label="理想値", color='#4CAF50')

    plt.xlabel("指標名", fontsize=14, fontproperties=font_prop)  # X軸のラベル
    plt.ylabel("値", fontsize=14, fontproperties=font_prop)  # Y軸のラベル
    plt.title("診断結果と理想値の比較", fontsize=16, fontproperties=font_prop)  # タイトル
    plt.xticks(x, metrics, fontsize=12, fontproperties=font_prop, rotation=0)  # X軸の値を横向き
    plt.yticks(fontsize=12, fontproperties=font_prop)  # Y軸の値
    plt.legend(prop=font_prop, fontsize=12)  # 凡例を追加

    # グラフを保存
    plot_path = os.path.join(static_dir, 'plot.png')
    plt.tight_layout()
    plt.savefig(plot_path, format='png', bbox_inches='tight')
    plt.close()

    session['plot_path'] = plot_path

    return render_template('result.html', url=url, results=results, plot_path=plot_path)

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    results = session.get('results', None)
    url = session.get('url', None)
    plot_path = session.get('plot_path', None)

    if not results or not url:
        return render_template('error.html', message="セッションデータが不足しています。診断を再実行してください。")

    pdf = FPDF()
    pdf.add_page()

    # 日本語フォントを追加
    if os.path.exists(FONT_PATH):
        pdf.add_font('NotoSansJP', '', FONT_PATH, uni=True)
        pdf.set_font("NotoSansJP", size=12)
    else:
        return render_template('error.html', message="日本語フォントが見つかりませんでした。")

    # PDFコンテンツ
    pdf.cell(200, 10, txt="診断結果", ln=True, align='C')
    pdf.cell(200, 10, txt=f"URL: {url}", ln=True)
    pdf.ln(10)

    for key, value in results.items():
        pdf.cell(200, 10, txt=f"{key}: {value['value']} {value['unit']}", ln=True)
        pdf.cell(200, 10, txt=f"理想値: {value['ideal']}", ln=True)
        pdf.cell(200, 10, txt=f"問題: {value['problem']}", ln=True)
        pdf.cell(200, 10, txt=f"提案: {value['suggestion']}", ln=True)
        pdf.ln(5)

    if plot_path and os.path.exists(plot_path):
        pdf.image(plot_path, x=10, y=pdf.get_y(), w=180)

    pdf_file = "診断結果.pdf"
    pdf.output(pdf_file, dest='F')

    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
