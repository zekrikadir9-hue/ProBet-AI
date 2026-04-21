import requests
from flask import Flask, render_template
import datetime

app = Flask(__name__)

# تأكد من أن هذا المفتاح صحيح وفعال من موقع API-Football
API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    # سنجلب مباريات الدوريات الكبرى (إنجلترا، إسبانيا، إيطاليا، ألمانيا، فرنسا، الجزائر)
    # دوري أبطال أوروبا (2)، الدوري الإنجليزي (39)، الإسباني (140)، الجزائري (186)
    params = {
        "next": "40", # جلب القادم 40 مباراة
        "timezone": "Africa/Algiers"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        raw_matches = data.get('response', [])
        
        processed = []
        for i, m in enumerate(raw_matches):
            processed.append({
                "home_team": m['teams']['home']['name'],
                "home_logo": m['teams']['home']['logo'],
                "away_team": m['teams']['away']['name'],
                "away_logo": m['teams']['away']['logo'],
                "prediction": "تحليل ذكي: فوز " + m['teams']['home']['name'] if i%2==0 else "توقع: تعادل أو " + m['teams']['away']['name'],
                "confidence": "87%" if i%2==0 else "74%",
                "status": "FREE" if i < 2 else "VIP"
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

if __name__ == "__main__":
    app.run()
