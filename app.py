import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- إعدادات البيانات (يمكنك وضع مفتاح API-Football هنا لاحقاً) ---
API_KEY ="86fcd9a4745789924658c45ee6c71525"

@app.route('/')
def home():
    # بيانات تجريبية لعرض التصميم الجذاب (شعارات الأندية + حالات VIP)
    matches = [
        {
            "home_team": "Real Madrid",
            "home_logo": "https://media.api-sports.io/football/teams/541.png",
            "away_team": "Barcelona",
            "away_logo": "https://media.api-sports.io/football/teams/529.png",
            "prediction": "فوز ريال مدريد",
            "confidence": "78%",
            "status": "VIP"
        },
        {
            "home_team": "Man City",
            "home_logo": "https://media.api-sports.io/football/teams/50.png",
            "away_team": "Arsenal",
            "away_logo": "https://media.api-sports.io/football/teams/42.png",
            "prediction": "تعادل أو فوز السيتي",
            "confidence": "65%",
            "status": "FREE"
        },
        {
            "home_team": "Liverpool",
            "home_logo": "https://media.api-sports.io/football/teams/40.png",
            "away_team": "Man United",
            "away_logo": "https://media.api-sports.io/football/teams/33.png",
            "prediction": "فوز ليفربول",
            "confidence": "82%",
            "status": "VIP"
        }
    ]
    return render_template('index.html', matches=matches)

@app.route('/pay')
def payment():
    # عرض صفحة الدفع التي تحتوي على رقم حسابك (00799999002210390713)
    return render_template('pay.html')

@app.route('/upload', methods=['POST'])
def upload_receipt():
    # هنا سيتم لاحقاً إضافة كود إرسال الصورة إلى تلغرام الخاص بك
    if 'receipt' in request.files:
        return "<h3>تم استلام طلبك بنجاح! سيتم مراجعة الوصل وتفعيل الباقة خلال دقائق.</h3><br><a href='/'>العودة للرئيسية</a>"
    return "خطأ في الرفع، يرجى المحاولة مرة أخرى."

if __name__ == "__main__":
    app.run(debug=True)
