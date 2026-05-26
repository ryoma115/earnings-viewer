# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

日本の新規上場企業の決算資料（決算短信・有価証券報告書等）を取得・表示する Web アプリケーション。

## 現状（Phase1 完了）

EDINET DB API を使った 1 銘柄の財務データ取得・表示を実装済み。

## ディレクトリ構成

```
earnings-viewer/
├── backend/
│   ├── main.py          # FastAPI アプリ（APIプロキシ）
│   ├── requirements.txt
│   └── .venv/           # ローカル仮想環境（gitignore 済）
├── frontend/
│   └── index.html       # HTML + CSS + バニラ JS
└── .env                 # EDINET_API_KEY（gitignore 済）
```

## 起動方法

```bash
cd backend
# 初回のみ
python3.9 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 起動
.venv/bin/uvicorn main:app --reload --port 8000
```

ブラウザで http://localhost:8000/ を開く。

## データソース

### EDINET DB API
- ベース URL: `https://edinetdb.jp`
- 認証: ヘッダー `X-API-Key: <key>`
- レート制限: Free プランで 100 回/日
- 主要エンドポイント:
  - `GET /v1/search?q={query}` — 企業名・証券コード・EDINETコードで検索（レスポンス: `{data: [...], meta: {...}}`）
  - `GET /v1/companies/{edinet_code}/financials` — 年度別財務時系列（最大数十年分、レスポンス: `{data: [...], meta: {...}}`）
- 財務フィールド（主要）:
  - P/L: `revenue`, `operating_income`, `ordinary_income`, `profit_before_tax`, `net_income`, `comprehensive_income`
  - B/S: `total_assets`, `net_assets`, `shareholders_equity`, `total_liabilities`, `cash`
  - CF: `cf_operating`, `cf_investing`, `cf_financing`
  - 1株: `eps`, `bps`, `dividend_per_share`, `payout_ratio`, `roe_official`, `equity_ratio_official`, `per`
  - `payout_ratio` / `roe_official` / `equity_ratio_official` は小数（0.31 = 31%）

## 技術スタック

- バックエンド: Python 3.9 / FastAPI 0.103 / uvicorn / httpx / python-dotenv
- フロントエンド: バニラ HTML・CSS・JavaScript（フレームワークなし）
- フロントエンドは FastAPI の StaticFiles で同一オリジン配信
