# 🌟 MyWebApp - ウェブパフォーマンス診断ツール

**MyWebApp** は、ウェブサイトのパフォーマンスを簡単かつ効率的に診断できるオープンソースのツールです。Google PageSpeed Insights API を活用し、診断結果を視覚化し、改善提案をわかりやすく提示します。エンジニアやウェブサイト管理者、SEO担当者など、多岐にわたるユーザーのニーズに対応しています。

---

## ✨ 特徴

- **詳細な診断レポート**
  - サーバーレスポンス時間、画像サイズなど、重要なパフォーマンス指標を測定。
- **視覚的な分析結果**
  - 棒グラフによる診断結果と理想値の比較で、問題点を簡単に特定。
- **改善提案の提示**
  - 診断結果に基づき、具体的な改善提案を提供。
- **PDFレポート生成**
  - 診断結果をPDF形式で保存し、チームで共有可能。
- **直感的なUI**
  - 初心者からプロフェッショナルまで、誰でも簡単に利用可能。

---

## 🛠 必要な環境

- **Python**: バージョン3.8以上
- **主要ライブラリ**:
  - Flask
  - Matplotlib
  - FPDF

---

## 📦 セットアップ

### 1️⃣ リポジトリのクローン
以下のコマンドを実行してリポジトリを取得します：
```bash
git clone https://github.com/pontandayo/MyWebApp.git
cd MyWebApp
```

### 2️⃣ 必要なパッケージのインストール
以下のコマンドで依存関係をインストールします：
```bash
pip install -r requirements.txt
```

### 3️⃣ 環境変数の設定
プロジェクトルートに `.env` ファイルを作成し、以下を記載します：
```env
PAGESPEED_API_KEY=あなたのpagespeed APIキー
SECRET_KEY=ランダムな文字列
```
---pagespeed APIのドキュメント
https://developers.google.com/speed/docs/insights/v5/get-started

### 4️⃣ アプリケーションの起動
以下のコマンドでローカルサーバーを起動します：
```bash
python app.py
```

ブラウザで `http://127.0.0.1:5000` にアクセスしてください。

---

## 🚀 デプロイ

### Heroku を利用する場合

1. **Heroku CLI のインストール**:
   [Heroku CLI公式サイト](https://devcenter.heroku.com/articles/heroku-cli) からダウンロード。

2. **アプリケーションのデプロイ**:
   ```bash
   heroku create
   git push heroku main
   heroku open
   ```

### Render を利用する場合

1. **Render アカウントの作成**:
   [Render公式サイト](https://render.com/) にサインアップ。

2. **デプロイ設定**:
   リポジトリを接続し、Python環境を選択後「Deploy」をクリック。

---

## 📊 使用例

### 1️⃣ URLを入力
診断対象のウェブサイトURLをフォームに入力します。

### 2️⃣ 診断結果を確認
- 棒グラフで診断結果と理想値を比較。
- 問題点と改善提案をテーブル形式で表示。

### 3️⃣ PDFで保存
診断結果をPDF形式でダウンロード可能です。

---

## 💡 想定される利用シナリオ

- **ウェブ開発者**:
  - パフォーマンス改善の基準として使用。
- **SEOスペシャリスト**:
  - 高速で最適化されたウェブサイトを構築するための指標として活用。
- **企業のIT担当者**:
  - サイトの定期診断と改善の報告書作成に利用。

---

## 🎨 プロジェクトの構成

- **`app.py`**: アプリケーションのメインロジック。
- **`templates/`**: HTMLテンプレート。
- **`static/`**: 静的ファイル（CSS、画像など）。
- **`fonts/`**: 日本語フォント。
- **`.env`**: APIキーやシークレットキーを管理。

---

## 🤝 クレジット

- **Google PageSpeed Insights** API によるデータ提供。
- **Noto Sans JP** フォントによる日本語対応。

---

## 📬 問い合わせ

- [GitHub Issues](https://github.com/pontandayo/MyWebApp/issues) でご質問・提案をお寄せください。

---

✨ **MyWebApp は、あなたのウェブサイトを最適化するための最良のパートナーです！**
