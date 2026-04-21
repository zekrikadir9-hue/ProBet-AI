import requests
from flask import Flask, render_template

app = Flask(__name__)

# مفتاحك الذي يظهر في الصورة
API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    
    # جربنا استخدام العنوانين معاً لضمان فك القفل عن البيانات
    headers = {
        "x-apisports-key": API_KEY,
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    
    # نطلب أقرب 40 مباراة قادمة عالمياً
    params = {"next": "40"}

    try:
        # قمنا بزيادة وقت الانتظار (timeout) لضمان عدم فشل الاتصال في الجزائر
        response = requests.get(url, headers=headers, params=params, timeout=15)
        data = response.json()
        raw_matches = data.get('response', [])
        
        if not raw_matches:
            return None

        processed = []
        for i, m in enumerate(raw_matches):
            processed.append({
                "home_team": m['teams']['home']['name'],
                "home_logo": m['teams']['home']['logo'],
                "away_team": m['teams']['away']['name'],
                "away_logo": m['teams']['away']['logo'],
                "prediction": "توقع AI: فوز " + m['teams']['home']['name'] if i%2==0 else "تحليل: تعادل",
                "confidence": "89%" if i%2==0 else "72%",
                "status": "FREE" if i < 3 else "VIP"
            })
        return processed
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    
    # 🛡️ "صمام الأمان" لكي لا تظهر الصفحة سوداء أبداً
    if not matches:
        matches = [
            {"home_team": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "away_team": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "prediction": "فوز ريال مدريد", "confidence": "85%", "status": "FREE"},
            {"home_team": "MC Alger", "home_logo": "https://media.api-sports.io/football/teams/1141.png", "away_team": "CR Belouizdad", "away_logo": "https://media.api-sports.io/football/teams/1143.png", "prediction": "تعادل محتمل", "confidence": "70%", "status": "FREE"},
            {"home_team": "Man City", "home_logo": "https://media.api-sports.io/football/teams/50.png", "away_team": "Liverpool", "away_logo": "https://media.api-sports.io/football/teams/40.png", "prediction": "فوز السيتي", "confidence": "91%", "status": "VIP"}
        ]
        
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

if __name__ == "__main__":
    app.run()
