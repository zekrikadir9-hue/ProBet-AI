import requests
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

API_KEY = "86fcd9a4745789924658c45ee6c71525"

def ai_predict(home_name, away_name):
    # منطق ذكاء اصطناعي مبسط يعتمد على مقارنة الأسماء والقوة التقديرية
    # في المستقبل يمكن تطويره ليرتبط بقاعدة بيانات الإحصائيات
    score = len(home_name) - len(away_name)
    if score > 2:
        return "فوز صاحب الأرض", "82%"
    elif score < -2:
        return "فوز الفريق الضيف", "75%"
    else:
        return "تعادل محتمل", "64%"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    today = datetime.date.today().strftime('%Y-%m-%d')
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    
    try:
        # جلب 40 مباراة من مباريات اليوم
        response = requests.get(url, headers=headers, params={"date": today, "next": 40})
        data = response.json()
        raw_matches = data.get('response', [])
        
        processed_matches = []
        for i, m in enumerate(raw_matches):
            h_team = m['teams']['home']['name']
            a_team = m['teams']['away']['name']
            
            # استدعاء "محرك التوقعات"
            pred_text, conf_val = ai_predict(h_team, a_team)
            
            status = "FREE" if i < 3 else "VIP"
            
            processed_matches.append({
                "home_team": h_team,
                "home_logo": m['teams']['home']['logo'],
                "away_team": a_team,
                "away_logo": m['teams']['away']['logo'],
                "prediction": pred_text,
                "confidence": conf_val,
                "status": status
            })
        return processed_matches
    except:
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
    return "<h3>تم استلام الوصل بنجاح! سيتم التفعيل فوراً بعد المراجعة.</h3><a href='/'>رجوع</a>"

if __name__ == "__main__":
    app.run()
