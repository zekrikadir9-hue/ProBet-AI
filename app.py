from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # بيانات تجريبية تشبه ما يأتي من الـ API لتجربة التصميم
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
            "prediction": "تعادل",
            "confidence": "65%",
            "status": "FREE"
        }
    ]
    return render_template('index.html', matches=matches)

if __name__ == "__main__":
    app.run()
