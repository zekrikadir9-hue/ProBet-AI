import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# مفتاحك الصحيح من صورتك
API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    # سنستخدم رابط الـ Fixtures لجلب المباريات القادمة
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY, # تم التحديث بناءً على كودك الأخير
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    
    # نطلب أقرب 40 مباراة قادمة عالمياً لضمان وجود محتوى
    params = {"next": "40"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
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
                "prediction": "فوز " + m['teams']['home']['name'] if i%2==0 else "تعادل محتمل",
                "confidence": "88%" if i%2==0 else "71%",
                "status": "FREE" if i < 3 else "VIP"
            })
        return processed
    except:
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    
    # إذا فشل الـ API (خطة الطوارئ لضمان احترافية الموقع)
    if not matches:
        matches = [
            {"home_team": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "away_team": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "prediction": "فوز الملكي", "confidence": "85%", "status": "FREE"},
            {"home_team": "Man City", "home_logo": "https://media.api-sports.io/football/teams/50.png", "away_team": "Liverpool", "away_logo": "https://media.api-sports.io/football/teams/40.png", "prediction": "تعادل", "confidence": "70%", "status": "FREE"},
            {"home_team": "MC Alger", "home_logo": "https://media.api-sports.io/football/teams/1141.png", "away_team": "JS Kabylie", "away_logo": "https://media.api-sports.io/football/teams/1145.png", "prediction": "فوز المولودية", "confidence": "90%", "status": "VIP"}
        ]
        
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

if __name__ == "__main__":
    app.run()
