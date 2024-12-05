# MyWebApp

## プロジェクト概要

MyWebAppは、ウェブサイトのパフォーマンスを診断し、改善提案を提供するツールです。ユーザーが診断対象のURLを入力すると、以下の機能を実行します：

1. **パフォーマンス解析**: サーバーレスポンス時間やリソースサイズ（画像、JavaScript、CSS）を収集・分析します。
2. **AI分析**: 遅延要因を特定し、影響度を分析します。
3. **改善提案生成**: 分析結果をもとに改善案をランク付けして提示します。
4. **結果の可視化**: グラフや表形式で診断結果をわかりやすく表示します。

## セットアップ方法

### ローカル環境でのセットアップ

1. **リポジトリのクローン**
    ```bash
    git clone https://github.com/pontandayo/MyWebApp.git
    cd MyWebApp
    ```

2. **仮想環境の作成と有効化**
    ```bash
    python -m venv venv
    source venv/bin/activate   # Windowsの場合は venv\Scripts\activate
    ```

3. **依存関係のインストール**
    ```bash
    pip install -r requirements.txt
    ```

4. **ローカルサーバーの起動**
    ```bash
    python app.py
    ```
    ブラウザで `http://127.0.0.1:5000` にアクセスします。

### Herokuへのデプロイ

1. **Heroku CLIにログイン**
    ```bash
    heroku login
    ```

2. **Herokuアプリの作成**
    ```bash
    heroku create <your-app-name>
    ```

3. **Gitリモートを追加**
    ```bash
    git remote add heroku https://git.heroku.com/<your-app-name>.git
    ```

4. **デプロイの実行**
    ```bash
    git push heroku main
    ```

5. **アプリの起動**
    ブラウザで `https://<your-app-name>.herokuapp.com` にアクセスします。

## 使用した技術

- **Flask**: Webアプリケーションフレームワーク。
- **BeautifulSoup**: HTML解析ライブラリ。
- **Matplotlib**: グラフ生成ツール。
- **ReportLab**: PDFレポート生成ツール。
- **Heroku**: デプロイプラットフォーム。

## 使用例

### 入力画面
ユーザーがウェブサイトのURLを入力する画面。
![入力画面](https://via.placeholder.com/800x400?text=URL+Input+Screen)

### 診断結果
解析結果をグラフや表形式で表示。
![診断結果](https://via.placeholder.com/800x400?text=Analysis+Results)

### 改善提案
改善提案をランク付けしてリスト表示。
![改善提案](https://via.placeholder.com/800x400?text=Improvement+Suggestions)

## 今後の改善点

- UI/UXの改善（レスポンシブデザイン対応）。
- 解析精度向上のためのAIモデルの改良。
- 多言語対応機能の追加。

---

プロジェクトに関するフィードバックや提案は、[Issues](https://github.com/pontandayo/MyWebApp/issues) でお待ちしています！
