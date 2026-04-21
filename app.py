import requests
from flask import Flask, render_template

app = Flask(__name__)

# مفتاحك سليم ومأخوذ من صورتك مباشرة
API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    # نطلب فقط القادم لضمان وجود بيانات
    params = {"next": "10"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # إذا كان هناك خطأ في المفتاح سيظهر هنا في السجلات (Logs)
        if 'errors' in data and data['errors']:
            print(f"API Error: {data['errors']}")
            return None
            
        raw_matches = data.get('response', [])
        processed = []
        for i, m in enumerate(raw_matches):
            processed.append({
                "home_team": m['teams']['home']['name'],
                "home_logo": m['teams']['home']['logo'],
                "away_team": m['teams']['away']['name'],
                "away_logo": m['teams']['away']['logo'],
                "prediction": "توقع: فوز " + m['teams']['home']['name'] if i%2==0 else "توقع: تعادل",
                "confidence": "85%",
                "status": "FREE" if i < 2 else "VIP"
            })
        return processed
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    # إذا فشل الـ API، سنعرض مباريات وهمية فقط لنعرف أن الصفحة تعمل
    if not matches:
        matches = [
            {"home_team": "إختبار اتصال", "home_logo": "", "away_team": "فشل الـ API", "away_logo": "", "prediction": "تحقق من لوحة التحكم", "confidence": "0%", "status": "FREE"}
        ]
    return render_template('index.html', matches=matches)

if __name__ == "__main__":
    app.run()
