import requests
from datetime import datetime

# 配置信息
PUID = "10413702"
COIN_TYPE = "btc"
TOKEN = "wowaMdEoleJHdEOrcVtNiJ5JQKPJwKCUB5EMSaLrW0bumD9ulTu8NxzdskKiCsGw"

def fetch():
    url = "https://api-prod.poolin.com/api/public/v2/payment/stats"
    headers = {
        "authorization": f"Bearer {TOKEN}",
        "User-Agent": "Mozilla/5.0"
    }
    params = {"puid": PUID, "coin_type": COIN_TYPE}
    
    try:
        res = requests.get(url, headers=headers, params=params, timeout=15)
        data = res.json()
        if data.get('err_no') == 0:
            d = data.get('data', {})
            y_earn = float(d.get('yesterday_amount', 0)) / 100000000
            balance = d.get('balance', '0.00')
            msg = "Success"
        else:
            y_earn, balance, msg = 0.0, "0.00", "API Error"
    except:
        y_earn, balance, msg = 0.0, "0.00", "Net Error"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor</title>
    <style>
        body {{ background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:50px; }}
        .box {{ border:1px solid #333; display:inline-block; padding:20px; border-radius:10px; }}
        .val {{ font-size:1.5rem; color:#f59e0b; font-weight:bold; }}
    </style>
</head>
<body>
    <div class="box">
        <h3>BTC Monitor</h3>
        <p>Yesterday: <span class="val">{y_earn:.8f}</span></p>
        <p>Balance: <span class="val">{balance}</span></p>
        <hr style="border:0; border-top:1px solid #222;">
        <p style="font-size:0.8rem; color:#666;">Update: {now}<br>Status: {msg}</p>
    </div>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    fetch()
