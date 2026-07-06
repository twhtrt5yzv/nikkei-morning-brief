# 日経モーニングブリーフ

毎朝の支社メンバー向け情報連携用アプリ。日経（nikkei.com）の記事見出しをGoogleニュース経由で自動収集し、カテゴリ別（トップ／株価／為替／金利／外貨・ドル建て／円建て・保険）に表示。記事を選んでコメントを付け、LINE・メールにそのまま貼れる連携文を生成できる。

## 仕組み

- `fetch_news.py` … GoogleニュースRSSから記事を取得し `data.json` を生成
- `.github/workflows/update-news.yml` … 毎朝 5:30 / 7:45（JST）に自動実行して `data.json` を更新
- `index.html` … `data.json` を読み込んで表示するアプリ本体（GitHub Pagesで公開）

## 使い方（毎朝のルーティン）

1. アプリを開く（iPhoneはホーム画面に追加しておく）
2. 連携したい記事にチェック → 必要ならひとことコメントを入力
3. 「連携文を作成」→「コピーする」→ LINE / メールに貼り付け

※ 記事リンクはGoogleニュース経由のURL。タップすると日経の記事ページに転送される。

## 手動更新

GitHubの Actions タブ →「記事データ自動更新」→ Run workflow。
またはローカルで `python3 fetch_news.py` を実行して push。
