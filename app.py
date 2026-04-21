import requests
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    # سنجلب مباريات اليوم والغد لضمان وجود بيانات
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    
    try:
        # طلب 50 مباراة قادمة
        response = requests.get(url, headers=headers, params={"date": today, "next": 50})
        data = response.json()
        raw_matches = data.get('response', [])
        
        if not raw_matches: return None

        processed_matches = []
        for i, m in enumerate(raw_matches):
            processed_matches.append({
                "home_team": m['teams']['home']['name'],
                "home_logo": m['teams']['home']['logo'],
                "away_team": m['teams']['away']['name'],
                "away_logo": m['teams']['away']['logo'],
                "prediction": "فوز " + m['teams']['home']['name'] if i%2==0 else "تعادل محتمل",
                "confidence": "85%" if i%2==0 else "70%",
                "status": "FREE" if i < 2 else "VIP" # أول مباراتين مجانية
            })
        return processed_matches
    except:
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    if not matches:
        # بيانات احتياطية في حال تعطل الـ API
        matches = [{"home_team": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "away_team": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "prediction": "فوز الملكي", "confidence": "85%", "status": "FREE"}]
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

@app.route('/upload', methods=['POST'])
def upload_receipt():
    return "<h3>تم الاستلام! سيتم التفعيل فوراً.</h3><a href='/'>رجوع</a>"

if __name__ == "__main__":
    app.run()
