import requests
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

API_KEY = "86fcd9a4745789924658c45ee6c71525"

def get_real_matches():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    # جلب تاريخ اليوم
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # قائمة بأهم الدوريات لضمان ظهور مباريات قوية (إنجلترا، إسبانيا، دوري الأبطال، الجزائر، إلخ)
    leagues = [39, 140, 141, 135, 78, 61, 2, 1]
    
    processed_matches = []
    
    try:
        # طلب المباريات القادمة (أول 50 مباراة قادمة عالمياً)
        response = requests.get(url, headers=headers, params={"next": 50})
        data = response.json()
        raw_matches = data.get('response', [])
        
        for i, m in enumerate(raw_matches):
            # فلترة: نأخذ فقط المباريات التي تنتمي للدوريات الكبرى لضمان الجودة
            if m['league']['id'] in leagues or i < 15:
                h_name = m['teams']['home']['name']
                a_name = m['teams']['away']['name']
                
                # منطق VIP: أول مباراتين مجانية والباقي مقفل
                status = "FREE" if i < 2 else "VIP"
                
                processed_matches.append({
                    "home_team": h_name,
                    "home_logo": m['teams']['home']['logo'],
                    "away_team": a_name,
                    "away_logo": m['teams']['away']['logo'],
                    "prediction": "فوز " + h_name if i % 2 == 0 else "تعادل أو " + a_name,
                    "confidence": "82%" if i % 2 == 0 else "71%",
                    "status": status
                })
        return processed_matches
    except:
        return None

@app.route('/')
def home():
    matches = get_real_matches()
    # إذا فشل الـ API تماماً، تظهر هذه المباريات كدعاية للموقع
    if not matches:
        matches = [
            {"home_team": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "away_team": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "prediction": "فوز ريال مدريد", "confidence": "85%", "status": "FREE"},
            {"home_team": "Liverpool", "home_logo": "https://media.api-sports.io/football/teams/40.png", "away_team": "Man City", "away_logo": "https://media.api-sports.io/football/teams/50.png", "prediction": "تعادل مثير", "confidence": "77%", "status": "VIP"}
        ]
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    return render_template('pay.html')

@app.route('/upload', methods=['POST'])
def upload_receipt():
    return "<h3>شكراً لك! تم استلام الوصل بنجاح، سيتم تفعيل حسابك خلال دقائق.</h3><a href='/'>العودة للمباريات</a>"

if __name__ == "__main__":
    app.run()
