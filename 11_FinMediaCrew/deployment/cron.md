# 定时任务配置

> FinMediaCrew 不是手动跑的工具 — 它是**每天自动产出的内容工厂**。

---

## 1. 推荐 cron 时间表

### 每日固定时段

| 时间 (UTC+8) | 任务 | 命令 |
|---|---|---|
| 06:30 | 抓昨日美股收盘 + 隔夜新闻 | `python crew/main.py --ticker NVDA --mode brief_only` |
| 07:00 | 跑 3 只重点 ticker 的简报 | `python scripts/daily_brief.py` |
| 08:30 | 推送早简报到飞书群 + 公众号 | `python scripts/distribute_morning.py` |
| 12:30 | 跑中午 1 篇小红书 | `python crew/main.py --ticker AAPL --mode content_only` |
| 17:00 | 跑美股盘前预告 | `python scripts/us_premarket.py` |
| 21:00 | 推送晚简报 | `python scripts/distribute_evening.py` |

### 每周固定任务

| 周几 | 时间 | 任务 |
|---|---|---|
| **周一 09:00** | 周选题会（自动生成 7 天选题） | `python scripts/weekly_topic_plan.py` |
| **周三 19:00** | 深度长文（公众号） | `python crew/main.py --ticker $WEEKLY_PICK --mode full` |
| **周五 19:00** | 视频脚本（YouTube） | `python crew/main.py --ticker $WEEKLY_PICK --mode video_only` |
| **周日 21:00** | 周复盘简报 + 下周预告 | `python scripts/weekly_recap.py` |

### 每月固定任务

| 时间 | 任务 |
|---|---|
| 月 1 日 09:00 | 月度数据复盘 + MonetizationAgent 报告 |
| 月 15 日 09:00 | 月中收入 + 漏斗体检 |
| 月底 21:00 | Gumroad 月度深度报告发布 |

---

## 2. Windows 任务计划程序示例

### 创建早间简报任务

```powershell
# PowerShell 管理员模式
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "crew/main.py --ticker NVDA --mode brief_only" `
  -WorkingDirectory "G:\我的云端硬盘\01-obsidian\04 AI知识库\09 金融记录共享\FinMediaCrew"

$trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM

Register-ScheduledTask `
  -TaskName "FinMediaCrew_MorningBrief" `
  -Action $action -Trigger $trigger `
  -RunLevel Highest `
  -Description "FinMediaCrew 每日早简报"
```

### 启动 / 停止 / 删除

```powershell
Start-ScheduledTask -TaskName "FinMediaCrew_MorningBrief"
Stop-ScheduledTask -TaskName "FinMediaCrew_MorningBrief"
Unregister-ScheduledTask -TaskName "FinMediaCrew_MorningBrief" -Confirm:$false
```

---

## 3. Linux/macOS crontab 示例

```bash
# 编辑
crontab -e

# 加入以下条目（每天早 7:00 跑简报，晚 21:00 推送晚简报）
0 7 * * * cd "/path/to/FinMediaCrew" && /usr/bin/python3 crew/main.py --ticker NVDA --mode brief_only >> logs/morning.log 2>&1
0 21 * * * cd "/path/to/FinMediaCrew" && /usr/bin/python3 scripts/distribute_evening.py >> logs/evening.log 2>&1

# 周三晚 19:00 跑深度长文
0 19 * * 3 cd "/path/to/FinMediaCrew" && /usr/bin/python3 crew/main.py --ticker $WEEKLY_PICK --mode full >> logs/weekly.log 2>&1
```

---

## 4. 容错 + 监控

### 关键规则

| 失败场景 | 行为 |
|---|---|
| LLM API 超时 / 限流 | 飞书发告警，5 分钟后自动重试，最多 3 次 |
| 上游 SKILL 调用失败 | 跳过该 SKILL，记录到 logs/，AnalystAgent 用其他 SKILL 兜底 |
| 内容质量 < 70 分 | 不分发，进 `drafts/` 等人工审 |
| 飞书 webhook 失败 | 写到本地 `pending_distribution/`，下次自动重试 |

### 监控指标

每天检查：
- 06:55 早任务是否启动？（飞书心跳）
- 09:00 早简报是否发出？（飞书群可见）
- 21:00 晚简报是否发出？
- 各任务执行时间是否 < 15 分钟？

每周检查：
- 任务成功率 ≥ 95%？
- LLM 成本是否在预算内（建议 < $200/月）？
- 内容质量评分稳定 ≥ 75 分？

---

## 5. 飞书心跳

每个定时任务执行前 / 后向飞书发心跳：

```python
# scripts/heartbeat.py
import requests, os, datetime

webhook = os.getenv("FEISHU_HEARTBEAT_URL")

def heartbeat(task_name: str, status: str, detail: str = ""):
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"🤖 FinMediaCrew\n任务: {task_name}\n状态: {status}\n时间: {datetime.datetime.now().isoformat()}\n{detail}"
        }
    }
    requests.post(webhook, json=payload, timeout=10)
```

在每个定时任务前后调用，避免"任务挂掉一天才发现"。

---

## 6. 周末模式

周六周日**自动降频**：
- 不跑早晚简报
- 只发周日 21:00 周复盘
- 节省 LLM 成本 + 给读者节假日感

---

## 7. 节假日处理

- 中国节假日（春节 / 国庆等）：自动跳过 A 股相关内容
- 美国节假日（独立日 / 感恩节等）：自动跳过美股相关内容
- 圣诞元旦：全停 1 周（提前 1 个月发"放假公告"）

---

## 8. 复盘

每月最后 1 天**手动跑一次完整复盘**：

```bash
python scripts/monthly_review.py --month 2026-05
```

输出：
- 内容质量评分趋势
- 漏斗 5 阶段月度变化
- 上下月对比
- 下月优化建议
- 推送到飞书群 + 公众号订户邮件
