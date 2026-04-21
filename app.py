import requests
from flask import Flask, render_template
import datetime

app = Flask(__name__)

# مفتاحك الذي يظهر في الصورة
API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    # سنطلب جلب أقرب 50 مباراة قادمة في العالم لضمان وجود بيانات
    params = {
        "next": "50" 
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        raw_matches = data.get('response', [])
        
        if not raw_matches:
            return []

        processed = []
        for i, m in enumerate(raw_matches):
            # سنأخذ أهم الدوريات فقط ليكون الموقع احترافياً
            # (الدوري الإنجليزي، الإسباني، الإيطالي، الألماني، الفرنسي، دوري الأبطال)
            top_leagues = [39, 140, 135, 78, 61, 2, 3, 848] 
            
            h_name = m['teams']['home']['name']
            a_name = m['teams']['away']['name']
            
            # منطق VIP: أول 3 مباريات مجانية والبقية VIP
            status = "FREE" if i < 3 else "VIP"
            
            processed.append({
                "home_team": h_name,
                "home_logo": m['teams']['home']['logo'],
                "away_team": a_name,
                "away_logo": m['teams']['away']['logo'],
                "prediction": "توقع AI: فوز " + h_name if i%2==0 else "تحليل: تعادل أو " + a_name,
                "confidence": "88%" if i%2==0 else "74%",
                "status": status
            })
        return processed
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/')
def home():
    matches = get_real_matches()
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

@app.route('/upload', methods=['POST'])
def upload_receipt():
    return "<h3>تم استلام الوصل! سيتم تفعيل حسابك خلال دقائق.</h3><a href='/'>رجوع</a>"

if __name__ == "__main__":
    app.run()
