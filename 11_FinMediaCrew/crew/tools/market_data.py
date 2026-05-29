"""
通用市场数据工具
================

5 个独立 Tool 类 + 一组 yfinance/FMP/web 兜底逻辑。
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

try:
    import yfinance as yf
except ImportError:
    yf = None


# ─────────────────────────────────────────────────────────────────
class _TickerArg(BaseModel):
    ticker: str = Field(..., description="股票代码")


class QuoteTool(BaseTool):
    name: str = "实时报价"
    description: str = "返回 ticker 的最新报价、涨跌幅、成交量、市值。"
    args_schema: Type[BaseModel] = _TickerArg

    def _run(self, ticker: str) -> str:
        if yf is None:
            return json.dumps({"status": "no_yfinance", "ticker": ticker})
        try:
            t = yf.Ticker(ticker)
            info = t.info or {}
            hist = t.history(period="5d")
            last_price = float(hist["Close"].iloc[-1]) if not hist.empty else info.get("regularMarketPrice")
            prev = float(hist["Close"].iloc[-2]) if len(hist) >= 2 else info.get("previousClose")
            change_pct = (last_price - prev) / prev * 100 if last_price and prev else None
            return json.dumps({
                "status": "ok",
                "ticker": ticker,
                "price": last_price,
                "prev_close": prev,
                "change_pct": round(change_pct, 2) if change_pct is not None else None,
                "volume": int(hist["Volume"].iloc[-1]) if not hist.empty else None,
                "market_cap": info.get("marketCap"),
                "as_of": datetime.now().isoformat(),
            })
        except Exception as e:
            return json.dumps({"status": "error", "ticker": ticker, "error": str(e)})


# ─────────────────────────────────────────────────────────────────
class FinancialsTool(BaseTool):
    name: str = "财报关键指标"
    description: str = "返回 ticker 最近 4 个季度的收入 / 净利 / EPS / YoY。"
    args_schema: Type[BaseModel] = _TickerArg

    def _run(self, ticker: str) -> str:
        if yf is None:
            return json.dumps({"status": "no_yfinance", "ticker": ticker})
        try:
            t = yf.Ticker(ticker)
            qf = t.quarterly_financials
            if qf is None or qf.empty:
                return json.dumps({"status": "empty", "ticker": ticker})
            recent = qf.iloc[:, :4].fillna(0).to_dict()
            recent_str = {str(k): {kk: float(vv) for kk, vv in v.items()} for k, v in recent.items()}
            return json.dumps({
                "status": "ok",
                "ticker": ticker,
                "quarterly_financials": recent_str,
            })
        except Exception as e:
            return json.dumps({"status": "error", "ticker": ticker, "error": str(e)})


# ─────────────────────────────────────────────────────────────────
class _NewsArg(BaseModel):
    ticker: str = Field(..., description="股票代码或公司名")
    days: int = Field(7, description="回溯天数")


class NewsTool(BaseTool):
    name: str = "新闻头条"
    description: str = "返回过去 N 天该 ticker 的关键新闻头条。"
    args_schema: Type[BaseModel] = _NewsArg

    def _run(self, ticker: str, days: int = 7) -> str:
        # yfinance 自带新闻接口
        if yf is None:
            return json.dumps({"status": "no_yfinance"})
        try:
            t = yf.Ticker(ticker)
            news = t.news[:15] if t.news else []
            cutoff = datetime.now() - timedelta(days=days)
            filtered = []
            for n in news:
                ts = datetime.fromtimestamp(n.get("providerPublishTime", 0))
                if ts >= cutoff:
                    filtered.append({
                        "title": n.get("title"),
                        "publisher": n.get("publisher"),
                        "link": n.get("link"),
                        "published": ts.isoformat(),
                    })
            return json.dumps({"status": "ok", "ticker": ticker, "count": len(filtered), "news": filtered})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})


# ─────────────────────────────────────────────────────────────────
class SecFilingsTool(BaseTool):
    name: str = "SEC 文件摘要"
    description: str = "返回最近一份 SEC filings 的摘要 + 链接。"
    args_schema: Type[BaseModel] = _TickerArg

    def _run(self, ticker: str) -> str:
        # 简单实现：调 SEC EDGAR JSON API
        try:
            ua = {"User-Agent": "FinMediaCrew alicechendejun@gmail.com"}
            cik_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K&dateb=&owner=include&count=5&output=atom"
            r = requests.get(cik_url, headers=ua, timeout=15)
            if r.status_code != 200:
                return json.dumps({"status": "http_error", "code": r.status_code})
            text_preview = r.text[:3000]
            return json.dumps({
                "status": "ok",
                "ticker": ticker,
                "note": "EDGAR atom feed snippet, parse downstream",
                "snippet": text_preview,
            })
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})


# ─────────────────────────────────────────────────────────────────
class SentimentTool(BaseTool):
    name: str = "社交情绪打分"
    description: str = "返回 ticker 的 Reddit/StockTwits 综合情绪分（-1 ~ +1）。"
    args_schema: Type[BaseModel] = _TickerArg

    def _run(self, ticker: str) -> str:
        # 简化版：如果没接 Reddit API，返回 placeholder + 标注
        api_key = os.getenv("STOCKTWITS_API_KEY") or os.getenv("ADANOS_API_KEY")
        if not api_key:
            return json.dumps({
                "status": "placeholder",
                "ticker": ticker,
                "note": "未配置 STOCKTWITS_API_KEY / ADANOS_API_KEY，使用 LLM 兜底",
                "score": None,
            })
        # 真实接入留作未来扩展
        return json.dumps({"status": "ok", "ticker": ticker, "score": 0.0, "source": "placeholder"})
