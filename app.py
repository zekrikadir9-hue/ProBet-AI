import requests
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

API_KEY = "86fcd9a4745789924658c45ee6c71525"

def ai_predict(home_name, away_name):
    # محرك توقعات مبني على طول اسم الفريق (كمثال برمجي)
    diff = len(home_name) - len(away_name)
    if diff > 1:
        return "فوز الفريق المضيف", "88%"
    elif diff < -1:
        return "فوز الفريق الضيف", "74%"
    else:
        return "تعادل محتمل", "60%"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    # نجلب تاريخ اليوم تلقائياً
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    try:
        # سنحاول جلب 50 مباراة من أهم الدوريات
        response = requests.get(url, headers=headers, params={"date": today, "next": 50})
        data = response.json()
        raw_matches = data.get('response', [])
        
        if not raw_matches:
            return None # لنقوم بعرض البيانات التوضيحية في حالة فراغ الـ API

        processed_matches = []
        for i, m in enumerate(raw_matches):
            h_name = m['teams']['home']['name']
            a_name = m['teams']['away']['name']
            pred, conf = ai_predict(h_name, a_name)
            
            processed_matches.append({
                "home_team": h_name,
                "home_logo": m['teams']['home']['logo'],
                "away_team": a_name,
                "away_logo": m['teams']['away']['logo'],
                "prediction": pred,
                "confidence": conf,
                "status": "FREE" if i < 3 else "VIP"
            })
        return processed_matches
    except:
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    
    # إذا كانت القائمة فارغة، سنعرض هذه المباريات لكي لا يظهر الموقع معطلاً
    if not matches:
        matches = [
            {"home_team": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "away_team": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "prediction": "فوز ريال مدريد", "confidence": "85%", "status": "FREE"},
            {"home_team": "Man City", "home_logo": "https://media.api-sports.io/football/teams/50.png", "away_team": "Arsenal", "away_logo": "https://media.api-sports.io/football/teams/42.png", "prediction": "تعادل", "confidence": "70%", "status": "FREE"},
            {"home_team": "MC Alger", "home_logo": "https://media.api-sports.io/football/teams/1141.png", "away_team": "JS Kabylie", "away_logo": "https://media.api-sports.io/football/teams/1145.png", "prediction": "فوز المولودية", "confidence": "90%", "status": "VIP"},
        ]
    
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

@app.route('/upload', methods=['POST'])
def upload_receipt():
    return "<h3>شكراً لك! تم إرسال الوصل. سيتم تفعيل حسابك خلال دقائق.</h3><a href='/'>العودة للرئيسية</a>"

if __name__ == "__main__":
    app.run()
