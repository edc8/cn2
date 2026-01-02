import requests
import os
from datetime import datetime, timedelta, timezone
import random

# --- 配置信息 (明文) ---
PUID = "10413702"
COIN_TYPE = "btc"
TOKEN = "wowaMdEoleJHdEOrcVtNiJ5JQKPJwKCUB5EMSaLrW0bumD9ulTu8NxzdskKiCsGw"

def fetch_and_generate():
    headers = {
        "authorization": f"Bearer {TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    params = {"puid": PUID, "coin_type": COIN_TYPE}
    
    stats = {"total": 0, "online": 0, "offline": 0}
    y_earn = 0.0
    balance = "0.00"
    hashrate = "0.00"
    status_msg = "数据更新成功"

    try:
        # 1. 获取矿机统计
        stats_url = "https://api-prod.poolin.com/api/public/v2/worker/stats"
        s_res = requests.get(stats_url, headers=headers, params=params, timeout=15).json()
        
        if s_res.get('err_no') == 0:
            d = s_res.get('data', {})
            stats["online"] = d.get('workers_active', 0)
            stats["offline"] = d.get('workers_dead', 0)
            stats["total"] = d.get('workers_total', 0)
            unit = d.get('shares_unit', 'T')
            hashrate = f"{d.get('shares_15m', 0)} {unit}"
        else:
            status_msg = f"统计失败: {s_res.get('err_msg')}"

        # 2. 获取收益信息
        pay_url = "https://api-prod.poolin.com/api/public/v2/payment/stats"
        p_res = requests.get(pay_url, headers=headers, params=params, timeout=15).json()
        if p_res.get('err_no') == 0:
            pd = p_res.get('data', {})
            y_earn = float(pd.get('yesterday_amount', 0))
            if y_earn > 1: y_earn /= 100000000 
            balance = pd.get('balance', '0.00')

    except Exception as e:
        status_msg = f"连接异常: {str(e)}"

    # 时区修正：强制转为北京时间 (UTC+8)
    utc_now = datetime.now(timezone.utc)
    beijing_now = utc_now.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

    # UI 逻辑：离线时红色
    off_style = "color: #ef4444; font-weight: 900;" if stats["offline"] > 0 else "color: #94a3b8;"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BTC实时监控</title>
        <style>
            :root {{ --bg: #0f172a; --card: #1e293b; --primary: #f59e0b; --text: #f8fafc; }}
            body {{ background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; display: flex; justify-content: center; padding: 20px; margin: 0; }}
            .card {{ background: var(--card); padding: 1.5rem; border-radius: 1.2rem; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); width: 100%; max-width: 360px; border: 1px solid #334155; }}
            h2 {{ color: var(--primary); text-align: center; margin-bottom: 1.2rem; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 1px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }}
            .stat-box {{ background: #0f172a; padding: 12px; border-radius: 0.8rem; text-align: center; border: 1px solid #1e293b; }}
            .label {{ color: #94a3b8; font-size: 0.7rem; margin-bottom: 4px; }}
            .val {{ font-size: 1rem; font-weight: bold; color: #fff; font-family: monospace; }}
            .worker-list {{ background: #0f172a; border-radius: 0.8rem; padding: 10px 15px; margin-top: 10px; border: 1px solid #1e293b; }}
            .row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #1e293b; font-size: 0.9rem; }}
            .row:last-child {{ border: none; }}
            .footer {{ font-size: 0.7rem; color: #64748b; margin-top: 1.5rem; text-align: center; line-height: 1.6; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>BTC 矿机监控</h2>
            <div class="grid">
                <div class="stat-box">
                    <div class="label">昨日收益</div>
                    <div class="val">{y_earn:.8f}</div>
                </div>
                <div class="stat-box">
                    <div class="label">当前算力</div>
                    <div class="val" style="color:#10b981;">{hashrate}</div>
                </div>
            </div>
            <div class="worker-list">
                <div class="row"><span>总矿机数</span><span class="val">{stats['total']}</span></div>
                <div class="row"><span>在线运行</span><span class="val" style="color: #10b981;">{stats['online']}</span></div>
                <div class="row"><span>离线报警</span><span class="val" style="{off_style}">{stats['offline']}</span></div>
                <div class="row"><span>当前余额</span><span class="val">{balance}</span></div>
            </div>
            <div class="footer">
                更新时间: {beijing_now}<br>
                状态: {status_msg}<br>
                PUID: {PUID}
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 执行成功！生成的 index.html 时间: {beijing_now}")

if __name__ == "__main__":
    fetch_and_generate()
