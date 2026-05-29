# 飞书集成

> FinMediaCrew 的**默认主分发渠道是飞书** — 因为飞书的自动化能力比微信好 100 倍。

---

## 1. 准备工作

### 创建飞书自定义机器人

1. 飞书群 → 设置 → 群机器人 → 添加机器人 → 自定义机器人
2. 命名：`FinMediaCrew`
3. 复制 Webhook URL，形如：
   ```
   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
4. **建议开启签名校验**（更安全）

### 写入 .env

```bash
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/...
FEISHU_GROUP_ID=oc_da1ba12165aa160e5b24b68ffaaa8d0d
FEISHU_HEARTBEAT_URL=https://open.feishu.cn/open-apis/bot/v2/hook/... (可选，独立心跳群)
```

---

## 2. 发送文本消息

```python
import requests, os

def send_text(text: str):
    requests.post(os.getenv("FEISHU_WEBHOOK_URL"), json={
        "msg_type": "text",
        "content": {"text": text}
    }, timeout=15)
```

---

## 3. 发送富文本（推荐用于简报）

```python
def send_brief(title: str, summary: str, link: str):
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {"tag": "text", "text": summary},
                        ],
                        [
                            {"tag": "a", "text": "完整版", "href": link},
                            {"tag": "text", "text": "  ·  by FinMediaCrew"},
                        ]
                    ]
                }
            }
        }
    }
    requests.post(os.getenv("FEISHU_WEBHOOK_URL"), json=payload, timeout=15)
```

---

## 4. 发送 Interactive Card（最强）

```python
def send_card(title: str, content: str, button_url: str):
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"📊 {title}"},
                "template": "green"
            },
            "elements": [
                {"tag": "markdown", "content": content},
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "查看完整版 →"},
                            "type": "primary",
                            "url": button_url
                        }
                    ]
                }
            ]
        }
    }
    requests.post(os.getenv("FEISHU_WEBHOOK_URL"), json=payload, timeout=15)
```

---

## 5. DistributionAgent 完整集成示例

```python
# crew/tools/distribution_feishu.py
import json, os, requests
from pathlib import Path
from datetime import datetime

class FeishuDistributor:
    def __init__(self):
        self.webhook = os.getenv("FEISHU_WEBHOOK_URL")
        if not self.webhook:
            raise RuntimeError("FEISHU_WEBHOOK_URL 未配置")

    def push_brief(self, brief_md: str, ticker: str = ""):
        """把 brief.md 推到飞书群"""
        title = f"{ticker} · 早简报" if ticker else "金融早简报"
        # 截取前 800 字（飞书消息上限）
        content = brief_md[:800] + ("\n\n[完整版 → 公众号]" if len(brief_md) > 800 else "")
        return self._send_card(title, content)

    def push_article_link(self, article_url: str, title: str, hook: str):
        """推送公众号长文链接"""
        return self._send_card(title, hook + f"\n\n👉 [阅读全文]({article_url})", article_url)

    def push_alert(self, msg: str):
        """异常告警"""
        return self._send_text(f"⚠️ FinMediaCrew 告警\n{msg}\n时间: {datetime.now().isoformat()}")

    def _send_text(self, text: str):
        return requests.post(self.webhook, json={
            "msg_type": "text",
            "content": {"text": text}
        }, timeout=15)

    def _send_card(self, title: str, content_md: str, url: str = ""):
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": f"📊 {title}"},
                    "template": "green"
                },
                "elements": [
                    {"tag": "markdown", "content": content_md}
                ]
            }
        }
        if url:
            payload["card"]["elements"].append({
                "tag": "action",
                "actions": [{
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "查看完整版 →"},
                    "type": "primary",
                    "url": url
                }]
            })
        return requests.post(self.webhook, json=payload, timeout=15)
```

---

## 6. 飞书 Bitable 集成（数据追踪）

把每天的内容产物 + 分发结果写到 Bitable：

```python
import requests, os, time, hashlib, base64, hmac

class FeishuBitable:
    """简化版 Bitable 写入"""

    def __init__(self, app_id: str, app_secret: str, base_id: str, table_id: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_id = base_id
        self.table_id = table_id
        self._token = None
        self._token_expire = 0

    def _get_token(self):
        if self._token and time.time() < self._token_expire - 60:
            return self._token
        r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", json={
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        }, timeout=15).json()
        self._token = r["tenant_access_token"]
        self._token_expire = time.time() + r["expire"]
        return self._token

    def add_record(self, fields: dict):
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.base_id}/tables/{self.table_id}/records"
        headers = {"Authorization": f"Bearer {self._get_token()}", "Content-Type": "application/json"}
        r = requests.post(url, json={"fields": fields}, headers=headers, timeout=15)
        return r.json()
```

### 推荐表结构

| 字段 | 类型 | 说明 |
|---|---|---|
| date | 日期 | YYYY-MM-DD |
| ticker | 单选 | 主要标的 |
| article_url | 链接 | 公众号链接 |
| xiaohongshu_status | 单选 | 已发 / 草稿 / 失败 |
| video_status | 单选 | 已发 / 待录 / 草稿 |
| brief_sent | 是/否 | 飞书简报是否发出 |
| ctr | 数字 | 当日 CTR |
| 完读率 | 数字 | 完读率 |
| 关注数 | 数字 | 关注转化 |
| 付费转化 | 数字 | 付费数 |
| LLM 成本 | 货币 | 当日 API 成本 |
| 质量评分 | 数字 | 1-100 |
| 备注 | 文本 | 复盘备注 |

---

## 7. 飞书机器人发图

飞书 webhook 不直接支持图片，需要先上传到飞书云空间 → 拿 image_key → 发送。

简化做法：把图片**上传到 GitHub / 腾讯云 COS / 阿里云 OSS**，然后在 markdown 里引用：

```python
def send_image_link(image_url: str, caption: str = ""):
    requests.post(os.getenv("FEISHU_WEBHOOK_URL"), json={
        "msg_type": "interactive",
        "card": {
            "elements": [
                {"tag": "img", "img_key": image_url, "alt": {"tag": "plain_text", "content": caption}}
            ]
        }
    }, timeout=15)
```

---

## 8. 限流 + 错误处理

飞书 webhook 限流：**500 条 / 分钟**（实际生产远远用不到）。

但要处理：

```python
import time

def safe_send(payload, max_retry=3):
    for i in range(max_retry):
        try:
            r = requests.post(os.getenv("FEISHU_WEBHOOK_URL"), json=payload, timeout=15)
            data = r.json()
            if data.get("code") == 0:
                return True
            elif data.get("code") == 19024:   # 频率限制
                time.sleep(2 ** i)
                continue
            else:
                print(f"飞书发送失败: {data}")
                return False
        except Exception as e:
            print(f"飞书异常: {e}")
            time.sleep(2 ** i)
    return False
```

---

## 9. 多群分发策略

不同内容发不同飞书群：

| 群 | 内容类型 |
|---|---|
| **德家族群** | 系统级告警 + 心跳 |
| **小爱日报群** | 每日早晚简报 |
| **付费简报群**（独立） | 付费订户独享内容 |
| **客户咨询群**（按客户） | 1对1 内容 |

通过**多个 webhook URL** 实现，每个群一个机器人。

---

## 10. 安全

- ❌ **绝不把 webhook URL 提交到 git**。
- ✅ 所有 URL 通过 `.env` 加载。
- ✅ 开启签名校验。
- ✅ 定期换 webhook URL（每季度）。
- ✅ 监控异常调用（每分钟 > 10 次自动告警）。
