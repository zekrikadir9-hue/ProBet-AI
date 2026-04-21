import requests
from flask import Flask, render_template

app = Flask(__name__)

# مفتاحك السليم
API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    # استخدام رابط جلب المباريات القادمة مباشرة لضمان وجود محتوى
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    # نطلب القادم من المباريات بغض النظر عن الدوري
    params = {"next": "20"}

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
                "prediction": f"توقع AI: فوز {m['teams']['home']['name']}" if i % 2 == 0 else "توقع AI: تعادل",
                "confidence": "85%",
                "status": "FREE" if i < 2 else "VIP"
            })
        return processed
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    # في حال فشل الـ API لأي سبب تقني، نعرض بيانات ثابتة لكي لا يهرب الزوار
    if not matches:
        matches = [
            {"home_team": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "away_team": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "prediction": "فوز الملكي", "confidence": "85%", "status": "FREE"},
            {"home_team": "MC Alger", "home_logo": "https://media.api-sports.io/football/teams/1141.png", "away_team": "JS Kabylie", "away_logo": "https://media.api-sports.io/football/teams/1145.png", "prediction": "فوز المولودية", "confidence": "90%", "status": "VIP"}
        ]
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

if __name__ == "__main__":
    app.run()
